"""Repaso espaciado y meta sugerida (FR-035): reglas puras, sin base de datos."""

import uuid
from datetime import date, timedelta

from app.study.plan import suggested_goal
from app.study.review import Attempt, due_questions

DAY0 = date(2026, 11, 2)
Q1, Q2 = uuid.uuid4(), uuid.uuid4()


def on(day: int, correct: bool, question: uuid.UUID = Q1) -> Attempt:
    return Attempt(question, DAY0 + timedelta(days=day), correct)


def due(attempts: list[Attempt], day: int) -> list[uuid.UUID]:
    return due_questions(attempts, DAY0 + timedelta(days=day))


def test_una_pregunta_acertada_a_la_primera_no_entra_al_repaso():
    assert due([on(0, True)], 30) == []


def test_un_error_vuelve_al_dia_siguiente():
    attempts = [on(0, False)]
    assert due(attempts, 0) == []
    assert due(attempts, 1) == [Q1]
    assert due(attempts, 20) == [Q1]  # atrasada: sigue pendiente hasta repasarla


def test_cada_acierto_en_el_repaso_alarga_la_espera_y_al_cuarto_sale():
    attempts = [on(0, False), on(1, True)]  # siguiente en 3 días
    assert (due(attempts, 3), due(attempts, 4)) == ([], [Q1])
    attempts += [on(4, True)]  # siguiente en 7 días
    assert (due(attempts, 10), due(attempts, 11)) == ([], [Q1])
    attempts += [on(11, True)]  # siguiente en 14 días
    assert (due(attempts, 24), due(attempts, 25)) == ([], [Q1])
    attempts += [on(25, True)]
    assert due(attempts, 365) == []  # cuatro aciertos seguidos: ya la domina


def test_volver_a_fallar_reinicia_el_repaso():
    attempts = [on(0, False), on(1, True), on(4, True), on(11, False)]
    assert due(attempts, 12) == [Q1]


def test_las_mas_atrasadas_van_primero():
    attempts = [on(0, False, Q2), on(3, False, Q1)]
    assert due(attempts, 10) == [Q2, Q1]


def test_la_meta_sugerida_reparte_lo_que_falta_entre_los_dias_que_quedan():
    assert suggested_goal(remaining=300, days_left=30) == 10
    assert suggested_goal(remaining=301, days_left=30) == 11  # redondea hacia arriba
    assert suggested_goal(remaining=20, days_left=30) == 5  # nunca menos del mínimo
    assert suggested_goal(remaining=40, days_left=0) == 40  # el mismo día: todo lo que falta
    assert suggested_goal(remaining=40, days_left=None) is None  # sin fecha no hay sugerencia
