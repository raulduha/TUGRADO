"""Cálculo de rachas (FR-033)."""

from datetime import UTC, date, datetime, timedelta

from app.clock import chile_date
from app.engagement.streaks import compute

TODAY = date(2026, 10, 13)


def days(*offsets: int) -> set[date]:
    return {TODAY - timedelta(days=o) for o in offsets}


def test_racha_actual_cuenta_dias_seguidos_hasta_hoy():
    assert compute(days(0, 1, 2), TODAY) == (3, 3)


def test_un_dia_sin_entrar_corta_la_racha_pero_queda_la_mejor():
    assert compute(days(0, 2, 3, 4, 5), TODAY) == (1, 4)


def test_sin_actividad_hoy_la_racha_actual_es_cero():
    assert compute(days(1, 2), TODAY) == (0, 2)


def test_sin_dias():
    assert compute(set(), TODAY) == (0, 0)


def test_el_dia_se_cuenta_en_hora_de_chile():
    # 02:00 UTC del 14 de octubre todavía es 13 de octubre en Chile.
    assert chile_date(datetime(2026, 10, 14, 2, 0, tzinfo=UTC)) == TODAY
