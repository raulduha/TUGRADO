"""Desconexión, recuperación, pausa voluntaria, abandono y solicitudes tardías
(FR-012, FR-012b, AC-011, AC-015, AC-028)."""

from datetime import timedelta

import pytest

from app.domain.simulation.session import AttemptState, SessionRuleError, SessionState
from tests.domain.conftest import T0, at, keep_alive, make_session, secs

RECOVERY = 30 * 60


# ------------------------------------------------------------------ desconexión


def test_sin_latido_durante_menos_de_30_s_no_hay_pausa(session):
    session.heartbeat(at(10))
    session.sweep(at(39.999))
    assert session.state is SessionState.IN_PROGRESS


def test_sin_latido_durante_30_s_pausa_retroactivamente_desde_el_ultimo(session):
    session.heartbeat(at(10))
    session.sweep(at(40))
    assert session.state is SessionState.PAUSED_DISCONNECTED
    assert session.paused_at == at(10)
    assert session.resume_state is SessionState.IN_PROGRESS
    # El tiempo entre el último latido y la detección no se consume.
    assert session.total_remaining(at(500)) == secs(590)


def test_la_deteccion_ocurre_tambien_al_llegar_el_siguiente_comando(session):
    session.heartbeat(at(10))
    with pytest.raises(SessionRuleError) as exc:
        session.heartbeat(at(45))
    assert exc.value.code == "session_paused"
    assert session.paused_at == at(10)


def test_la_pausa_retroactiva_no_aplica_vencimientos_posteriores_al_ultimo_latido(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 115)
    session.sweep(at(145))  # sin la pausa, la pregunta habría vencido a los 120
    attempt = session.attempts[0]
    assert attempt.state is AttemptState.IN_PROGRESS
    session.resume(at(600), "r1")
    # Al reanudar quedan los 5 s que faltaban.
    assert session.snapshot(at(600)).question_remaining == secs(5)
    session.submit_answer(at(604), "a1")
    assert attempt.state is AttemptState.SUBMITTED


def test_reanudar_restaura_estado_y_tiempo_restante(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 50)
    session.sweep(at(80))
    session.resume(at(1000), "r1")
    assert session.state is SessionState.IN_PROGRESS
    snapshot = session.snapshot(at(1000))
    assert snapshot.question_remaining == secs(70)
    assert snapshot.total_remaining == secs(550)
    assert session.events[-1].type == "session_resumed"


def test_reanudar_vuelve_a_awaiting_current_question_completion():
    session = make_session(total=100, question=60)
    session.start_question(at(0), "q1")
    keep_alive(session, 30)
    session.submit_answer(at(30), "a1")
    session.complete_evaluation(at(30), 1)
    session.start_question(at(30), "q2")
    keep_alive(session, 100)
    session.sweep(at(130))
    assert session.resume_state is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION
    session.resume(at(200), "r1")
    assert session.state is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION


def test_reanudar_justo_antes_de_30_minutos_desde_el_ultimo_latido(session):
    session.heartbeat(at(10))
    session.sweep(at(40))
    session.resume(at(10 + RECOVERY - 0.001), "r1")
    assert session.state is SessionState.IN_PROGRESS


def test_a_los_30_minutos_del_ultimo_latido_la_sesion_queda_expired(session):
    session.heartbeat(at(10))
    session.sweep(at(40))
    with pytest.raises(SessionRuleError) as exc:
        session.resume(at(10 + RECOVERY), "r1")
    assert exc.value.code == "session_expired"
    assert session.state is SessionState.EXPIRED
    assert session.events[-1].at == at(10 + RECOVERY)


def test_la_tarea_periodica_vence_la_sesion_no_recuperada(session):
    session.start_question(at(0), "q1")
    session.sweep(at(10 + RECOVERY))
    assert session.state is SessionState.EXPIRED
    assert session.attempts[0].state is AttemptState.CANCELLED


def test_ventana_de_recuperacion_configurable():
    session = make_session(recovery_window=timedelta(minutes=5))
    session.sweep(at(40))
    session.sweep(at(300))
    assert session.state is SessionState.EXPIRED


def test_comandos_durante_la_pausa_se_rechazan(session):
    session.sweep(at(30))
    with pytest.raises(SessionRuleError) as exc:
        session.start_question(at(31), "q1")
    assert exc.value.code == "session_paused"


def test_reanudar_duplicado_es_idempotente(session):
    session.sweep(at(30))
    session.resume(at(100), "r1")
    session.resume(at(101), "r1")
    assert [e.type for e in session.events].count("session_resumed") == 1


def test_reanudar_sin_pausa_se_rechaza(session):
    with pytest.raises(SessionRuleError) as exc:
        session.resume(at(5), "r1")
    assert exc.value.code == "session_not_paused"


def test_evaluacion_terminada_durante_la_desconexion_completa_la_sesion():
    session = make_session(total=100, question=90)
    session.start_question(at(0), "q1")
    keep_alive(session, 30)
    session.submit_answer(at(30), "a1")
    session.complete_evaluation(at(30), 1)
    session.start_question(at(30), "q2")
    keep_alive(session, 110)
    session.submit_answer(at(110), "a2")
    session.sweep(at(140))
    assert session.resume_state is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION
    assert session.state is SessionState.PAUSED_DISCONNECTED
    session.complete_evaluation(at(150), 2)
    assert session.state is SessionState.COMPLETED


# ----------------------------------------------------------- pausa voluntaria


def test_pausa_voluntaria_con_pregunta_activa_se_rechaza(session):
    session.start_question(at(0), "q1")
    with pytest.raises(SessionRuleError) as exc:
        session.start_voluntary_pause(at(5), "p1")
    assert exc.value.code == "pause_not_allowed"


def test_pausa_voluntaria_detiene_el_total_y_se_reanuda_sola_a_los_30_s(session):
    session.heartbeat(at(10))
    session.start_voluntary_pause(at(10), "p1")
    keep_alive(session, 39.999)
    assert session.voluntary_pause_started_at is not None
    assert session.total_remaining(at(39.999)) == secs(590)
    keep_alive(session, 50)
    assert session.voluntary_pause_started_at is None
    assert session.total_remaining(at(50)) == secs(580)
    ended = [e for e in session.events if e.type == "voluntary_pause_ended"]
    assert ended[0].at == at(40)
    assert ended[0].data == {"reason": "expired"}


def test_segunda_pausa_voluntaria_se_rechaza(session):
    session.start_voluntary_pause(at(1), "p1")
    session.end_voluntary_pause(at(5), "p1-end")
    with pytest.raises(SessionRuleError) as exc:
        session.start_voluntary_pause(at(6), "p2")
    assert exc.value.code == "pause_limit_reached"


def test_iniciar_pregunta_termina_la_pausa_voluntaria(session):
    session.start_voluntary_pause(at(1), "p1")
    session.start_question(at(5), "q1")
    assert session.voluntary_pause_started_at is None
    assert session.events[-2].data == {"reason": "question_started"}


def test_pausa_voluntaria_duplicada_es_idempotente(session):
    session.start_voluntary_pause(at(1), "p1")
    session.start_voluntary_pause(at(2), "p1")
    assert session.voluntary_pauses_used == 1


# -------------------------------------------------------------------- abandono


def test_abandonar_conserva_lo_evaluado_y_cancela_lo_pendiente(session):
    session.start_question(at(0), "q1")
    session.submit_answer(at(10), "a1")
    session.complete_evaluation(at(11), 1)
    session.start_question(at(12), "q2")
    session.abandon(at(20), "x1")
    assert session.state is SessionState.ABANDONED
    assert [a.state for a in session.attempts] == [AttemptState.EVALUATED, AttemptState.CANCELLED]


def test_evaluacion_tardia_de_un_intento_cancelado_se_rechaza(session):
    session.start_question(at(0), "q1")
    session.submit_answer(at(10), "a1")
    session.abandon(at(11), "x1")
    with pytest.raises(SessionRuleError) as exc:
        session.complete_evaluation(at(12), 1)
    assert exc.value.code == "invalid_attempt_state"
    assert session.state is SessionState.ABANDONED


# ------------------------------------------------- solicitudes tardías e inválidas


def test_solicitud_tardia_no_reabre_una_sesion_cerrada():
    session = make_session(count=1)
    session.start_question(at(0), "q1")
    session.submit_answer(at(10), "a1")
    session.complete_evaluation(at(11), 1)
    assert session.state is SessionState.COMPLETED
    for command in (
        lambda: session.start_question(at(12), "q2"),
        lambda: session.heartbeat(at(12)),
        lambda: session.start_voluntary_pause(at(12), "p1"),
    ):
        with pytest.raises(SessionRuleError) as exc:
            command()
        assert exc.value.code == "session_closed"
    assert session.state is SessionState.COMPLETED


def test_iniciar_dos_veces_se_rechaza(session):
    with pytest.raises(SessionRuleError) as exc:
        session.start(at(1))
    assert exc.value.code == "session_already_started"


def test_horas_sin_zona_horaria_se_rechazan(session):
    with pytest.raises(ValueError):
        session.heartbeat(T0.replace(tzinfo=None))


def test_operaciones_fuera_de_orden_temporal_se_rechazan(session):
    session.heartbeat(at(10))
    with pytest.raises(ValueError):
        session.heartbeat(at(5))


def test_snapshot_no_modifica_la_sesion(session):
    session.start_question(at(0), "q1")
    snapshot = session.snapshot(at(200))
    assert snapshot.state is SessionState.PAUSED_DISCONNECTED
    assert session.state is SessionState.IN_PROGRESS
    assert session.attempts[0].state is AttemptState.IN_PROGRESS
