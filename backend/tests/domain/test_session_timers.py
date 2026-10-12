"""Límite individual, extensión y límite total (FR-009 a FR-011, AC-006, AC-014, AC-031)."""

import pytest

from app.domain.simulation.session import AttemptState, SessionRuleError, SessionState
from tests.domain.conftest import at, keep_alive, make_session, secs


def evaluate(session, t, order):
    session.start_evaluation(at(t), order)
    session.complete_evaluation(at(t), order)


# ------------------------------------------------------------ límite individual


def test_respuesta_justo_antes_del_limite_individual_se_acepta(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 110)
    session.submit_answer(at(119.999), "a1")
    assert session.attempts[0].state is AttemptState.SUBMITTED


def test_al_vencer_el_limite_individual_se_ofrece_extension_y_la_respuesta_se_rechaza(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 110)
    with pytest.raises(SessionRuleError) as exc:
        session.submit_answer(at(120), "a1")
    assert exc.value.code == "answer_not_accepted"
    assert session.attempts[0].state is AttemptState.AWAITING_EXTENSION
    assert [e.type for e in session.events][-1] == "extension_offered"
    assert session.events[-1].at == at(120)


def test_sin_solicitud_dentro_de_la_ventana_la_pregunta_pasa_a_timed_out(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 130)
    session.heartbeat(at(135))
    assert session.attempts[0].state is AttemptState.TIMED_OUT
    assert session.events[-1].type == "question_timed_out"
    assert session.events[-1].at == at(135)
    assert session.state is SessionState.IN_PROGRESS


# ------------------------------------------------------------------- extensión


def test_extension_justo_antes_del_cierre_de_la_ventana_se_concede(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 130)
    new_limit = session.request_extension(at(134.999), "e1")
    # Hora de concesión + 60 s: el estudiante dispone de 60 s completos.
    assert new_limit == secs(134.999 + 60)
    assert session.snapshot(at(134.999)).question_remaining == secs(60)


def test_extension_al_cerrar_la_ventana_se_rechaza(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 130)
    with pytest.raises(SessionRuleError) as exc:
        session.request_extension(at(135), "e1")
    assert exc.value.code == "extension_not_available"
    assert session.attempts[0].state is AttemptState.TIMED_OUT


def test_extension_agrega_exactamente_60_s_desde_la_concesion(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 130)
    session.request_extension(at(130), "e1")
    keep_alive(session, 180)
    session.submit_answer(at(189.999), "a1")
    assert session.attempts[0].state is AttemptState.SUBMITTED


def test_al_agotar_la_extension_no_se_ofrece_otra_con_maximo_1(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 130)
    session.request_extension(at(130), "e1")
    keep_alive(session, 190)
    assert session.attempts[0].state is AttemptState.TIMED_OUT
    assert [e.type for e in session.events].count("extension_offered") == 1


def test_extension_duplicada_no_concede_dos_veces(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 130)
    first = session.request_extension(at(130), "e1")
    again = session.request_extension(at(131), "e1")
    assert again == first
    assert session.attempts[0].extensions_granted == 1
    assert [e.type for e in session.events].count("extension_granted") == 1


def test_dos_solicitudes_simultaneas_distintas_conceden_una_sola_extension(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 130)
    session.request_extension(at(130), "e1")
    with pytest.raises(SessionRuleError) as exc:
        session.request_extension(at(130), "e2")
    assert exc.value.code == "extension_not_available"
    assert session.attempts[0].extensions_granted == 1


def test_extension_antes_de_vencer_el_limite_se_rechaza(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 60)
    with pytest.raises(SessionRuleError) as exc:
        session.request_extension(at(60), "e1")
    assert exc.value.code == "extension_not_available"


def test_maximo_de_extensiones_es_configurable():
    session = make_session(max_extensions_per_question=2)
    session.start_question(at(0), "q1")
    keep_alive(session, 120)
    session.request_extension(at(120), "e1")
    keep_alive(session, 180)
    session.request_extension(at(180), "e2")
    assert session.attempts[0].extensions_granted == 2
    keep_alive(session, 240)
    assert session.attempts[0].state is AttemptState.TIMED_OUT


def test_sin_extensiones_configuradas_la_pregunta_vence_directamente():
    session = make_session(max_extensions_per_question=0)
    session.start_question(at(0), "q1")
    keep_alive(session, 120)
    assert session.attempts[0].state is AttemptState.TIMED_OUT


def test_la_ventana_de_oferta_consume_tiempo_total(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 135)
    assert session.attempts[0].state is AttemptState.TIMED_OUT
    assert session.total_remaining(at(135)) == secs(600 - 135)


# --------------------------------------------------------------- límite total


def test_tiempo_total_agotado_entre_preguntas_completa_la_sesion():
    session = make_session(total=100, question=60)
    session.start_question(at(0), "q1")
    keep_alive(session, 20)
    session.submit_answer(at(20), "a1")
    evaluate(session, 20, 1)
    keep_alive(session, 100)
    assert session.state is SessionState.COMPLETED
    with pytest.raises(SessionRuleError) as exc:
        session.start_question(at(101), "q2")
    assert exc.value.code == "session_closed"


def test_tiempo_total_agotado_con_pregunta_activa_permite_terminarla():
    session = make_session(total=100, question=90)
    session.start_question(at(0), "q1")
    keep_alive(session, 20)
    session.submit_answer(at(20), "a1")
    evaluate(session, 20, 1)
    session.start_question(at(20), "q2")
    keep_alive(session, 100)
    assert session.state is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION
    # La pregunta activa conserva su límite individual (vence a los 110 s).
    keep_alive(session, 109.999)
    session.submit_answer(at(109.999), "a2")
    assert session.state is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION
    evaluate(session, 115, 2)
    assert session.state is SessionState.COMPLETED


def test_tiempo_total_agotado_bloquea_nuevas_preguntas():
    session = make_session(total=100, question=60, count=5)
    session.start_question(at(0), "q1")
    keep_alive(session, 50)
    session.submit_answer(at(50), "a1")
    evaluate(session, 50, 1)
    session.start_question(at(50), "q2")
    keep_alive(session, 100)
    assert session.state is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION
    with pytest.raises(SessionRuleError) as exc:
        session.start_question(at(100), "q3")
    assert exc.value.code == "no_new_questions"


def test_extension_permitida_despues_de_agotar_el_tiempo_total():
    session = make_session(total=100, question=60)
    session.start_question(at(0), "q1")
    keep_alive(session, 30)
    session.submit_answer(at(30), "a1")
    evaluate(session, 30, 1)
    session.start_question(at(30), "q2")
    keep_alive(session, 90)  # total agotado a los 100; la pregunta vence a los 90
    keep_alive(session, 100)
    assert session.state is SessionState.AWAITING_CURRENT_QUESTION_COMPLETION
    session.request_extension(at(100), "e1")
    keep_alive(session, 150)
    session.submit_answer(at(150), "a2")
    evaluate(session, 151, 2)
    assert session.state is SessionState.COMPLETED


def test_pregunta_activa_que_vence_tras_el_tiempo_total_cierra_la_sesion():
    session = make_session(total=100, question=60)
    session.start_question(at(0), "q1")
    keep_alive(session, 30)
    session.submit_answer(at(30), "a1")
    evaluate(session, 30, 1)
    session.start_question(at(30), "q2")
    keep_alive(session, 105)  # vence a los 90 + 15 s de ventana
    assert session.attempts[1].state is AttemptState.TIMED_OUT
    assert session.state is SessionState.COMPLETED


def test_sesion_completa_al_evaluar_la_ultima_pregunta():
    session = make_session(count=2)
    for i, t in ((1, 0), (2, 40)):
        session.start_question(at(t), f"q{i}")
        keep_alive(session, t + 20)
        session.submit_answer(at(t + 20), f"a{i}")
        evaluate(session, t + 30, i)
    assert session.state is SessionState.COMPLETED
    assert session.events[-1].type == "session_completed"


# -------------------------------------------------------- tiempo de procesamiento


def test_el_procesamiento_no_consume_el_reloj_de_la_pregunta_ni_el_total(session):
    session.start_question(at(0), "q1")
    keep_alive(session, 50)
    received = session.submit_answer(at(50), "a1")
    assert received == at(50)
    keep_alive(session, 300)
    session.start_evaluation(at(300), 1)
    keep_alive(session, 400)
    assert session.total_remaining(at(400)) == secs(550)
    session.complete_evaluation(at(400), 1)
    assert session.attempts[0].clock.used(at(400)) == secs(50)
    # El total se reanuda al terminar el procesamiento.
    keep_alive(session, 410)
    assert session.total_remaining(at(410)) == secs(540)


def test_no_se_inicia_otra_pregunta_mientras_la_anterior_se_procesa(session):
    session.start_question(at(0), "q1")
    session.submit_answer(at(10), "a1")
    with pytest.raises(SessionRuleError) as exc:
        session.start_question(at(11), "q2")
    assert exc.value.code == "question_active"


def test_respuesta_duplicada_no_crea_otra_recepcion(session):
    session.start_question(at(0), "q1")
    first = session.submit_answer(at(10), "a1")
    again = session.submit_answer(at(12), "a1")
    assert again == first
    assert [e.type for e in session.events].count("answer_received") == 1


def test_evaluacion_duplicada_se_rechaza(session):
    session.start_question(at(0), "q1")
    session.submit_answer(at(10), "a1")
    evaluate(session, 11, 1)
    with pytest.raises(SessionRuleError) as exc:
        session.complete_evaluation(at(12), 1)
    assert exc.value.code == "invalid_attempt_state"
