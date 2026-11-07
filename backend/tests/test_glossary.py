"""Glosario del rosco (FR-038): comparación de respuestas y lectura de la planilla, sin base."""

from io import BytesIO

from openpyxl import Workbook

from app.glossary.terms import COLUMNS, SHEET, normalize, parse_glossary


def xlsx(rows: list[list], header: list[str] = COLUMNS) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = SHEET
    ws.append(header)
    for values in rows:
        ws.append(values)
    out = BytesIO()
    wb.save(out)
    return out.getvalue()


def test_la_respuesta_se_compara_sin_mayusculas_tildes_ni_articulo():
    assert normalize("La Tradición") == normalize("tradicion") == "tradicion"
    assert normalize("  el   DOLO ") == "dolo"
    assert normalize("Señorío") == "señorio"  # la ñ no es una n con tilde
    assert normalize("Tradición") != normalize("Ocupación")


def test_la_planilla_valida_cada_fila_y_es_todo_o_nada():
    ok = ["Derecho Civil", "Tradición", "Modo de adquirir por entrega.", "CC, art. 670"]
    terms, errors = parse_glossary(xlsx([ok]))
    assert errors == [] and terms[0].term == "Tradición"

    bad = [
        ok,
        ["Derecho Civil", "Dolo", "", "CC, art. 44"],  # sin definición
        ["Derecho Civil", "Culpa", "Falta de culpa diligente.", "CC, art. 44"],  # se delata
        ["derecho civil", "tradición", "Repetida.", "CC"],  # repetida
    ]
    terms, errors = parse_glossary(xlsx(bad))
    assert terms == []
    assert [row for row, _ in errors] == [3, 4, 5]
    assert parse_glossary(xlsx([ok], header=["materia", "termino"]))[1][0][0] == 0
    assert parse_glossary(b"no es excel")[1][0][0] == 0
