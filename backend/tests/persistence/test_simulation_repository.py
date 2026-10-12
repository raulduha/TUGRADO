"""Persistencia de la sesión contra PostgreSQL: ida y vuelta, rechazos, idempotencia y
concurrencia real entre transacciones (Gate 3, AC-011, AC-014, AC-015)."""

import threading
import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.simulation.session import AttemptState, SessionRuleError, SessionState
from app.persistence.auth_models import UserAccountRow
from app.persistence.simulation_models import SessionEventRow
from app.persistence.simulation_repository import (
    SessionNotFound,
    create_session,
    run_locked,
)
from tests.domain.conftest import at, make_session, secs
from tests.fakes import FakeClock

pytestmark = pytest.mark.integration


@pytest.fixture
def stored(engine):
    with Session(engine) as db:
        student = UserAccountRow(email="estudiante@ejemplo.cl", password_hash="x")
        db.add(student)
        db.commit()
        student_id = student.id
    session_id = uuid.uuid4()
    create_session(engine, session_id, student_id, make_session())
    return session_id


def run(engine, session_id, seconds, operation):
    return run_locked(engine, session_id, operation, FakeClock(seconds))


def heartbeats(engine, session_id, start, end, step=10):
    t = start
    while t <= end:
        run(engine, session_id, t, lambda s, now: s.heartbeat(now))
        t += step


def test_ida_y_vuelta_reproduce_la_misma_sesion_que_en_memoria(engine, stored):
    script = [
        (0, lambda s, now: s.start_question(now, "q1")),
        (10, lambda s, now: s.heartbeat(now)),
        (20, lambda s, now: s.submit_answer(now, "a1")),
        (25, lambda s, now: s.start_evaluation(now, 1)),
        (30, lambda s, now: s.complete_evaluation(now, 1)),
        (31, lambda s, now: s.start_voluntary_pause(now, "p1")),
        (40, lambda s, now: s.heartbeat(now)),
        (50, lambda s, now: s.start_question(now, "q2")),
        *[(t, lambda s, now: s.heartbeat(now)) for t in range(60, 171, 10)],
        (171, lambda s, now: s.request_extension(now, "e1")),
    ]
    memory = make_session()
    for seconds, operation in script:
        operation(memory, at(seconds))
        run(engine, stored, seconds, operation)

    loaded = run(engine, stored, 171, lambda s, now: s)
    assert loaded.state is memory.state is SessionState.IN_PROGRESS
    assert loaded.snapshot(at(200)) == memory.snapshot(at(200))
    assert [(e.type, e.at, e.data) for e in loaded.events] == [
        (e.type, e.at, e.data) for e in memory.events
    ]
    assert [a.state for a in loaded.attempts] == [AttemptState.EVALUATED, AttemptState.IN_PROGRESS]
    assert loaded.attempts[1].extensions_granted == 1


def test_un_rechazo_guarda_la_pausa_detectada_antes_de_rechazar(engine, stored):
    run(engine, stored, 10, lambda s, now: s.heartbeat(now))
    with pytest.raises(SessionRuleError) as exc:
        run(engine, stored, 45, lambda s, now: s.heartbeat(now))
    assert exc.value.code == "session_paused"

    loaded = run(engine, stored, 46, lambda s, now: s)
    assert loaded.state is SessionState.PAUSED_DISCONNECTED
    assert loaded.paused_at == at(10)
    assert loaded.events[-1].type == "paused_disconnected"


def test_un_error_inesperado_no_guarda_cambios(engine, stored):
    run(engine, stored, 10, lambda s, now: s.heartbeat(now))

    def falla_a_mitad(s, now):
        s.start_question(now, "q1")
        raise RuntimeError("fallo inesperado")

    with pytest.raises(RuntimeError):
        run(engine, stored, 11, falla_a_mitad)
    loaded = run(engine, stored, 12, lambda s, now: s)
    assert loaded.attempts == []
    assert "q1" not in loaded.request_results


def test_solicitud_duplicada_en_otra_transaccion_devuelve_el_mismo_resultado(engine, stored):
    assert run(engine, stored, 0, lambda s, now: s.start_question(now, "q1")) == 1
    heartbeats(engine, stored, 10, 130)
    limit = run(engine, stored, 130, lambda s, now: s.request_extension(now, "e1"))
    received = run(engine, stored, 140, lambda s, now: s.submit_answer(now, "a1"))

    assert run(engine, stored, 141, lambda s, now: s.start_question(now, "q1")) == 1
    assert run(engine, stored, 142, lambda s, now: s.request_extension(now, "e1")) == limit
    assert run(engine, stored, 143, lambda s, now: s.submit_answer(now, "a1")) == received
    assert limit == secs(190)
    assert received == at(140)

    loaded = run(engine, stored, 144, lambda s, now: s)
    types = [e.type for e in loaded.events]
    assert types.count("extension_granted") == 1
    assert types.count("answer_received") == 1


def test_los_eventos_se_guardan_en_secuencia_contigua(engine, stored):
    run(engine, stored, 0, lambda s, now: s.start_question(now, "q1"))
    run(engine, stored, 5, lambda s, now: s.submit_answer(now, "a1"))
    run(engine, stored, 6, lambda s, now: s.complete_evaluation(now, 1))
    with Session(engine) as db:
        seqs = db.scalars(
            select(SessionEventRow.seq)
            .where(SessionEventRow.session_id == stored)
            .order_by(SessionEventRow.seq)
        ).all()
    assert seqs == list(range(len(seqs)))
    assert len(seqs) == 4  # started, question_started, answer_received, evaluation_completed


def test_sesion_inexistente(engine):
    with pytest.raises(SessionNotFound):
        run(engine, uuid.uuid4(), 0, lambda s, now: s)


# ------------------------------------------------------------------ concurrencia


def _prepare_extension_window(engine, session_id):
    run(engine, session_id, 0, lambda s, now: s.start_question(now, "q1"))
    heartbeats(engine, session_id, 10, 130)


def _in_parallel(*operations):
    """Ejecuta las operaciones en hilos a la vez; devuelve resultados o excepciones."""
    barrier = threading.Barrier(len(operations))
    results: list = [None] * len(operations)

    def worker(index, operation):
        barrier.wait()
        try:
            results[index] = operation()
        except Exception as exc:  # noqa: BLE001 - se devuelve para inspeccionarla
            results[index] = exc

    threads = [threading.Thread(target=worker, args=(i, op)) for i, op in enumerate(operations)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)
    return results


def test_extensiones_concurrentes_distintas_conceden_una_sola(engine, stored):
    _prepare_extension_window(engine, stored)
    clock = FakeClock(131)
    results = _in_parallel(
        *[
            lambda rid=rid: run_locked(
                engine, stored, lambda s, now, rid=rid: s.request_extension(now, rid), clock
            )
            for rid in ("e1", "e2", "e3", "e4")
        ]
    )
    granted = [r for r in results if not isinstance(r, Exception)]
    rejected = [r for r in results if isinstance(r, SessionRuleError)]
    assert len(granted) == 1
    assert len(rejected) == 3
    assert {r.code for r in rejected} == {"extension_not_available"}

    loaded = run(engine, stored, 132, lambda s, now: s)
    assert loaded.attempts[0].extensions_granted == 1
    assert [e.type for e in loaded.events].count("extension_granted") == 1


def test_extensiones_concurrentes_con_el_mismo_request_id_son_idempotentes(engine, stored):
    _prepare_extension_window(engine, stored)
    clock = FakeClock(131)
    results = _in_parallel(
        *[
            lambda: run_locked(engine, stored, lambda s, now: s.request_extension(now, "e1"), clock)
            for _ in range(4)
        ]
    )
    assert results == [secs(191)] * 4
    loaded = run(engine, stored, 132, lambda s, now: s)
    assert [e.type for e in loaded.events].count("extension_granted") == 1


def test_el_bloqueo_serializa_las_transacciones_sobre_la_misma_sesion(engine, stored):
    holding = threading.Event()
    release = threading.Event()
    order: list[str] = []

    def slow(s, now):
        s.heartbeat(now)
        holding.set()
        release.wait(timeout=10)
        order.append("first")

    def fast(s, now):
        s.heartbeat(now)
        order.append("second")

    first = threading.Thread(target=lambda: run(engine, stored, 5, slow))
    first.start()
    assert holding.wait(timeout=10)
    second = threading.Thread(target=lambda: run(engine, stored, 6, fast))
    second.start()
    second.join(timeout=0.5)
    assert second.is_alive(), "la segunda transacción debió esperar el bloqueo"
    release.set()
    first.join(timeout=10)
    second.join(timeout=10)
    assert order == ["first", "second"]
