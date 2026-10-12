"""Máquina de estados de la simulación y sus temporizadores (FR-009 a FR-012b, Gate 3).

Lógica pura: no conoce la base de datos ni HTTP. Cada operación recibe la hora del servidor
(`at`), de modo que las pruebas controlan el tiempo de forma determinista.

Convenciones de tiempo:
- Todos los plazos son exclusivos: en el instante exacto del vencimiento la regla ya aplicó
  (por ejemplo, una extensión pedida justo a los 15 s de la ventana se rechaza).
- Las transiciones por tiempo (fin de pregunta, fin de ventana de extensión, fin del tiempo
  total, fin de la pausa voluntaria) se consolidan solo hasta la última señal del cliente
  (latido o comando). Así, una desconexión detectada después pausa el reloj de forma
  retroactiva desde el último latido sin tener que deshacer transiciones.
- Las operaciones del cliente llevan `request_id`: repetir una solicitud ya aceptada devuelve
  el mismo resultado sin efectos nuevos. La concurrencia real (dos procesos a la vez) se
  resuelve en la capa de persistencia con un bloqueo por sesión.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Any

from app.domain.simulation.clock import Stopwatch
from app.domain.simulation.policy import SessionPolicy, SimulationTimeConfig


class SessionState(StrEnum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    PAUSED_DISCONNECTED = "paused_disconnected"
    AWAITING_CURRENT_QUESTION_COMPLETION = "awaiting_current_question_completion"
    COMPLETED = "completed"
    EXPIRED = "expired"
    ABANDONED = "abandoned"


class AttemptState(StrEnum):
    IN_PROGRESS = "in_progress"
    AWAITING_EXTENSION = "awaiting_extension"
    SUBMITTED = "submitted"
    EVALUATING = "evaluating"
    EVALUATED = "evaluated"
    TIMED_OUT = "timed_out"
    CANCELLED = "cancelled"


ACTIVE_SESSION_STATES = {
    SessionState.IN_PROGRESS,
    SessionState.AWAITING_CURRENT_QUESTION_COMPLETION,
}
TERMINAL_SESSION_STATES = {SessionState.COMPLETED, SessionState.EXPIRED, SessionState.ABANDONED}
# Pregunta en curso: su reloj corre.
ANSWERING_STATES = {AttemptState.IN_PROGRESS, AttemptState.AWAITING_EXTENSION}
# Respuesta recibida y en procesamiento: el reloj total está detenido.
PROCESSING_STATES = {AttemptState.SUBMITTED, AttemptState.EVALUATING}
FINAL_ATTEMPT_STATES = {AttemptState.EVALUATED, AttemptState.TIMED_OUT, AttemptState.CANCELLED}


class SessionRuleError(Exception):
    """Operación rechazada por una regla de negocio. `code` es estable para la API."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class SessionEvent:
    """Evento auditable de sesión (modelo de dominio: SessionEvent)."""

    type: str
    at: datetime
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class QuestionAttempt:
    order: int
    started_at: datetime
    limit: timedelta
    state: AttemptState = AttemptState.IN_PROGRESS
    clock: Stopwatch = field(default_factory=Stopwatch)
    extensions_granted: int = 0
    answer_received_at: datetime | None = None


@dataclass(frozen=True)
class SessionSnapshot:
    """Vista calculada para la interfaz. El frontend la muestra, pero no decide con ella."""

    state: SessionState
    total_remaining: timedelta
    attempt_state: AttemptState | None
    question_remaining: timedelta | None
    extension_offer_remaining: timedelta | None
    recovery_remaining: timedelta | None


def _require_aware(at: datetime) -> None:
    if at.tzinfo is None or at.utcoffset() is None:
        raise ValueError("las horas deben incluir zona horaria (UTC)")


class SimulationSession:
    def __init__(self, config: SimulationTimeConfig, policy: SessionPolicy) -> None:
        # Configuración y política congeladas para toda la sesión.
        self.config = config
        self.policy = policy
        self.state = SessionState.CREATED
        self.resume_state: SessionState | None = None
        self.attempts: list[QuestionAttempt] = []
        self.events: list[SessionEvent] = []
        self.total_clock = Stopwatch()
        self.last_seen: datetime | None = None
        self.paused_at: datetime | None = None
        self.voluntary_pause_started_at: datetime | None = None
        self.voluntary_pauses_used = 0
        # Estado interno persistido: solo lo modifica esta clase (y el mapeo al restaurar).
        # Hasta dónde se consolidaron las transiciones por tiempo.
        self.committed_at: datetime | None = None
        # Última hora recibida, para exigir orden temporal.
        self.last_operation_at: datetime | None = None
        # Resultado de cada request_id aceptado (idempotencia).
        self.request_results: dict[str, Any] = {}

    # ------------------------------------------------------------------ consultas

    @property
    def active_attempt(self) -> QuestionAttempt | None:
        if self.attempts and self.attempts[-1].state not in FINAL_ATTEMPT_STATES:
            return self.attempts[-1]
        return None

    def total_remaining(self, at: datetime) -> timedelta:
        return max(timedelta(0), self.config.total_limit - self.total_clock.used(at))

    def snapshot(self, now: datetime) -> SessionSnapshot:
        """Proyección a `now` suponiendo que el cliente sigue conectado. No modifica la sesión."""
        projected = copy.deepcopy(self)
        projected._refresh(now)
        if projected.state in ACTIVE_SESSION_STATES:
            projected._advance_to(now)
        attempt = projected.active_attempt
        question_remaining = None
        offer_remaining = None
        if attempt is not None and attempt.state in ANSWERING_STATES:
            used = attempt.clock.used(now)
            question_remaining = max(timedelta(0), attempt.limit - used)
            if attempt.state is AttemptState.AWAITING_EXTENSION:
                window_end = attempt.limit + self.policy.extension_offer_window
                offer_remaining = max(timedelta(0), window_end - used)
        recovery_remaining = None
        if projected.state is SessionState.PAUSED_DISCONNECTED and projected.paused_at:
            deadline = projected.paused_at + self.policy.recovery_window
            recovery_remaining = max(timedelta(0), deadline - now)
        return SessionSnapshot(
            state=projected.state,
            total_remaining=projected.total_remaining(now),
            attempt_state=attempt.state if attempt else None,
            question_remaining=question_remaining,
            extension_offer_remaining=offer_remaining,
            recovery_remaining=recovery_remaining,
        )

    # ------------------------------------------------------- comandos del cliente

    def start(self, at: datetime) -> None:
        self._check_time(at)
        if self.state is not SessionState.CREATED:
            raise SessionRuleError("session_already_started", "La sesión ya fue iniciada")
        self.state = SessionState.IN_PROGRESS
        self.last_seen = at
        self.committed_at = at
        self._sync_clocks(at)
        self._record("session_started", at)

    def heartbeat(self, at: datetime) -> None:
        self._client_touch(at)

    def start_question(self, at: datetime, request_id: str) -> int:
        if request_id in self.request_results:
            return self.request_results[request_id]
        self._client_touch(at)
        if self.state is not SessionState.IN_PROGRESS:
            raise SessionRuleError(
                "no_new_questions", "No se pueden iniciar preguntas en el estado actual"
            )
        if self.active_attempt is not None:
            raise SessionRuleError("question_active", "Ya hay una pregunta activa o en proceso")
        if len(self.attempts) >= self.config.question_count:
            raise SessionRuleError("no_questions_left", "No quedan preguntas en la simulación")
        if self.voluntary_pause_started_at is not None:
            self._end_voluntary_pause(at, reason="question_started")
        attempt = QuestionAttempt(
            order=len(self.attempts) + 1, started_at=at, limit=self.config.question_limit
        )
        self.attempts.append(attempt)
        self._sync_clocks(at)
        self._record("question_started", at, order=attempt.order)
        self.request_results[request_id] = attempt.order
        return attempt.order

    def request_extension(self, at: datetime, request_id: str) -> timedelta:
        """Concede la extensión y devuelve el nuevo límite total de la pregunta."""
        if request_id in self.request_results:
            return self.request_results[request_id]
        self._client_touch(at)
        attempt = self.active_attempt
        if attempt is None or attempt.state is not AttemptState.AWAITING_EXTENSION:
            raise SessionRuleError(
                "extension_not_available", "No hay una extensión disponible en este momento"
            )
        # La ventana solo se abre si quedan extensiones, pero se revalida aquí.
        if attempt.extensions_granted >= self.policy.max_extensions_per_question:
            raise SessionRuleError("extension_limit_reached", "Se alcanzó el máximo de extensiones")
        attempt.extensions_granted += 1
        # Límite = hora de concesión + extensión (decisión del 2026-10-12, docs/correcciones G).
        attempt.limit = attempt.clock.used(at) + self.policy.extension
        attempt.state = AttemptState.IN_PROGRESS
        self._record(
            "extension_granted",
            at,
            order=attempt.order,
            extensions_granted=attempt.extensions_granted,
        )
        self.request_results[request_id] = attempt.limit
        return attempt.limit

    def submit_answer(self, at: datetime, request_id: str) -> datetime:
        """Registra la recepción de la respuesta; detiene el reloj de la pregunta y el total."""
        if request_id in self.request_results:
            return self.request_results[request_id]
        self._client_touch(at)
        attempt = self.active_attempt
        if attempt is None or attempt.state is not AttemptState.IN_PROGRESS:
            raise SessionRuleError(
                "answer_not_accepted", "No hay una pregunta abierta a respuestas"
            )
        attempt.state = AttemptState.SUBMITTED
        attempt.answer_received_at = at
        self._sync_clocks(at)
        self._record("answer_received", at, order=attempt.order)
        self.request_results[request_id] = at
        return at

    def start_voluntary_pause(self, at: datetime, request_id: str) -> None:
        if request_id in self.request_results:
            return
        self._client_touch(at)
        if self.state is not SessionState.IN_PROGRESS or self.active_attempt is not None:
            raise SessionRuleError(
                "pause_not_allowed", "Solo se puede pausar entre preguntas, sin pregunta activa"
            )
        if self.voluntary_pause_started_at is not None:
            raise SessionRuleError("pause_already_active", "La pausa ya está activa")
        if self.voluntary_pauses_used >= self.policy.voluntary_pauses_per_session:
            raise SessionRuleError("pause_limit_reached", "Ya se usó la pausa de esta simulación")
        self.voluntary_pauses_used += 1
        self.voluntary_pause_started_at = at
        self._sync_clocks(at)
        self._record("voluntary_pause_started", at)
        self.request_results[request_id] = None

    def end_voluntary_pause(self, at: datetime, request_id: str) -> None:
        if request_id in self.request_results:
            return
        self._client_touch(at)
        if self.voluntary_pause_started_at is None:
            raise SessionRuleError("pause_not_active", "No hay una pausa activa")
        self._end_voluntary_pause(at, reason="student")
        self.request_results[request_id] = None

    def resume(self, at: datetime, request_id: str) -> None:
        """Reanuda tras una desconexión, con el tiempo restante guardado."""
        if request_id in self.request_results:
            return
        self._check_time(at)
        self._refresh(at)
        if self.state is SessionState.EXPIRED:
            raise SessionRuleError("session_expired", "Venció la ventana de recuperación")
        if self.state is not SessionState.PAUSED_DISCONNECTED:
            raise SessionRuleError("session_not_paused", "La sesión no está pausada")
        assert self.resume_state is not None
        self.state = self.resume_state
        self.resume_state = None
        self.paused_at = None
        self.last_seen = at
        self.committed_at = at
        self._sync_clocks(at)
        self._record("session_resumed", at, state=self.state.value)
        self.request_results[request_id] = None

    def abandon(self, at: datetime, request_id: str) -> None:
        """Cierre voluntario sin terminar: lo evaluado se conserva; lo pendiente no puntúa."""
        if request_id in self.request_results:
            return
        self._check_time(at)
        self._refresh(at)
        if self.state in ACTIVE_SESSION_STATES:
            self._advance_to(max(at, self.committed_at or at))
        self._ensure_not_closed()
        if self.state is SessionState.CREATED:
            raise SessionRuleError("session_not_started", "La sesión no ha comenzado")
        for attempt in self.attempts:
            if attempt.state not in FINAL_ATTEMPT_STATES:
                attempt.clock.stop(at)
                attempt.state = AttemptState.CANCELLED
        self.resume_state = None
        self.paused_at = None
        self._close(SessionState.ABANDONED, at)
        self.request_results[request_id] = None

    # ------------------------------------------- comandos del sistema (procesamiento)

    def start_evaluation(self, at: datetime, order: int) -> None:
        attempt = self._processing_attempt(at, order, {AttemptState.SUBMITTED})
        attempt.state = AttemptState.EVALUATING
        self._record("evaluation_started", at, order=order)

    def complete_evaluation(self, at: datetime, order: int) -> None:
        """Fin del procesamiento: el reloj total se reanuda desde `at`."""
        attempt = self._processing_attempt(at, order, PROCESSING_STATES)
        attempt.state = AttemptState.EVALUATED
        self._record("evaluation_completed", at, order=order)
        self._after_attempt_final(at)

    def sweep(self, at: datetime) -> None:
        """Tarea periódica: detecta desconexiones y vence sesiones no recuperadas."""
        self._check_time(at)
        self._refresh(at)

    # ------------------------------------------------------------------ internos

    def _check_time(self, at: datetime) -> None:
        _require_aware(at)
        if self.last_operation_at is not None and at < self.last_operation_at:
            raise ValueError("las operaciones de una sesión deben llegar en orden temporal")
        self.last_operation_at = at

    def _ensure_not_closed(self) -> None:
        if self.state in TERMINAL_SESSION_STATES:
            raise SessionRuleError("session_closed", f"La sesión está cerrada ({self.state})")

    def _client_touch(self, at: datetime) -> None:
        self._check_time(at)
        self._refresh(at)
        self._ensure_not_closed()
        if self.state is SessionState.PAUSED_DISCONNECTED:
            raise SessionRuleError("session_paused", "La sesión está pausada; debe reanudarse")
        if self.state is SessionState.CREATED:
            raise SessionRuleError("session_not_started", "La sesión no ha comenzado")
        # La señal del cliente prueba conexión hasta `at`: se consolidan las transiciones.
        self._advance_to(at)
        self.last_seen = at
        if self.state in TERMINAL_SESSION_STATES:
            # La sesión se cerró por tiempo antes de este comando.
            raise SessionRuleError("session_closed", f"La sesión está cerrada ({self.state})")

    def _processing_attempt(
        self, at: datetime, order: int, allowed: set[AttemptState]
    ) -> QuestionAttempt:
        self._check_time(at)
        self._refresh(at)
        if not 1 <= order <= len(self.attempts):
            raise SessionRuleError("attempt_not_found", "No existe ese intento")
        attempt = self.attempts[order - 1]
        if attempt.state not in allowed:
            raise SessionRuleError(
                "invalid_attempt_state", f"El intento está en estado {attempt.state}"
            )
        return attempt

    def _refresh(self, at: datetime) -> None:
        """Aplica la detección de desconexión y el vencimiento de la recuperación."""
        if self.state in ACTIVE_SESSION_STATES:
            assert self.last_seen is not None
            if at - self.last_seen >= self.policy.heartbeat_timeout:
                self._advance_to(self.last_seen)
                if self.state in ACTIVE_SESSION_STATES:
                    self._pause_disconnected(self.last_seen)
        if self.state is SessionState.PAUSED_DISCONNECTED:
            assert self.paused_at is not None
            deadline = self.paused_at + self.policy.recovery_window
            if at >= deadline:
                for attempt in self.attempts:
                    if attempt.state in ANSWERING_STATES:
                        attempt.state = AttemptState.CANCELLED
                self.resume_state = None
                self._close(SessionState.EXPIRED, deadline)

    def _pause_disconnected(self, at: datetime) -> None:
        if self.voluntary_pause_started_at is not None:
            self._end_voluntary_pause(at, reason="disconnected")
        self.resume_state = self.state
        self.state = SessionState.PAUSED_DISCONNECTED
        self.paused_at = at
        self._sync_clocks(at)
        self._record("paused_disconnected", at, resume_state=self.resume_state.value)

    def _end_voluntary_pause(self, at: datetime, reason: str) -> None:
        self.voluntary_pause_started_at = None
        self._sync_clocks(at)
        self._record("voluntary_pause_ended", at, reason=reason)

    def _next_timed_event(self) -> tuple[datetime, str] | None:
        candidates: list[tuple[datetime, str]] = []
        since = self.total_clock.running_since
        if since is not None:
            remaining = self.config.total_limit - self.total_clock.used(since)
            candidates.append((since + remaining, "total_exhausted"))
        attempt = self.active_attempt
        if attempt is not None and attempt.clock.running_since is not None:
            q_since = attempt.clock.running_since
            used = attempt.clock.used(q_since)
            if attempt.state is AttemptState.IN_PROGRESS:
                candidates.append((q_since + (attempt.limit - used), "question_exhausted"))
            elif attempt.state is AttemptState.AWAITING_EXTENSION:
                window_end = attempt.limit + self.policy.extension_offer_window
                candidates.append((q_since + (window_end - used), "offer_window_ended"))
        if self.voluntary_pause_started_at is not None:
            end = self.voluntary_pause_started_at + self.policy.voluntary_pause_max
            candidates.append((end, "voluntary_pause_expired"))
        return min(candidates, default=None)

    def _advance_to(self, until: datetime) -> None:
        """Aplica, en orden, las transiciones por tiempo con instante <= `until`."""
        while self.state in ACTIVE_SESSION_STATES:
            event = self._next_timed_event()
            if event is None or event[0] > until:
                break
            at, kind = event
            if kind == "question_exhausted":
                self._on_question_exhausted(at)
            elif kind == "offer_window_ended":
                self._time_out_attempt(at)
            elif kind == "total_exhausted":
                self._on_total_exhausted(at)
            else:
                self._end_voluntary_pause(at, reason="expired")
        if self.committed_at is None or until > self.committed_at:
            self.committed_at = until

    def _on_question_exhausted(self, at: datetime) -> None:
        attempt = self.active_attempt
        assert attempt is not None
        if attempt.extensions_granted < self.policy.max_extensions_per_question:
            attempt.state = AttemptState.AWAITING_EXTENSION
            self._record("extension_offered", at, order=attempt.order)
        else:
            self._time_out_attempt(at)

    def _time_out_attempt(self, at: datetime) -> None:
        attempt = self.active_attempt
        assert attempt is not None
        attempt.state = AttemptState.TIMED_OUT
        self._record("question_timed_out", at, order=attempt.order)
        self._after_attempt_final(at)

    def _on_total_exhausted(self, at: datetime) -> None:
        self._record("total_time_exhausted", at)
        attempt = self.active_attempt
        if attempt is not None and attempt.state in ANSWERING_STATES:
            self.state = SessionState.AWAITING_CURRENT_QUESTION_COMPLETION
            self._sync_clocks(at)
        else:
            self._close(SessionState.COMPLETED, at)

    def _after_attempt_final(self, at: datetime) -> None:
        if self.state in TERMINAL_SESSION_STATES:
            # Una evaluación tardía no reabre ni cambia el cierre de la sesión.
            return
        # Si la evaluación termina durante una desconexión, decide el estado al que se volverá.
        effective = self.resume_state if self.paused_at is not None else self.state
        all_done = len(self.attempts) >= self.config.question_count and self.active_attempt is None
        if effective is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION or all_done:
            self.resume_state = None
            self.paused_at = None
            self._close(SessionState.COMPLETED, at)
        else:
            self._sync_clocks(at)

    def _close(self, state: SessionState, at: datetime) -> None:
        self.state = state
        self.voluntary_pause_started_at = None
        self._sync_clocks(at)
        self._record(f"session_{state.value}", at)

    def _sync_clocks(self, at: datetime) -> None:
        """Arranca o detiene los relojes según el estado. Única fuente de esa regla."""
        attempt = self.active_attempt
        session_running = self.state in ACTIVE_SESSION_STATES
        total_runs = (
            self.state is SessionState.IN_PROGRESS
            and self.voluntary_pause_started_at is None
            and not (attempt is not None and attempt.state in PROCESSING_STATES)
        )
        if total_runs:
            self.total_clock.start(at)
        else:
            self.total_clock.stop(at)
        for a in self.attempts:
            if session_running and a is attempt and a.state in ANSWERING_STATES:
                a.clock.start(at)
            else:
                a.clock.stop(at)

    def _record(self, type_: str, at: datetime, **data: Any) -> None:
        self.events.append(SessionEvent(type=type_, at=at, data=data))
