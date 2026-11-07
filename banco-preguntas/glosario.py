"""Glosario inicial del rosco legal (Civil y Procesal).

Genera salida/glosario-civil-procesal.xlsx con el formato que importa /admin/glosario y lo
valida con el lector real de la app. Los términos entran como borrador: el abogado del equipo
debe revisarlos y otro administrador aprobarlos y publicarlos.

Ejecutar desde backend/:  uv run python ../banco-preguntas/glosario.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from app.glossary.terms import COLUMNS, SHEET, parse_glossary  # noqa: E402

CIVIL = "Derecho Civil"
PROCESAL = "Derecho Procesal"
CC = "Código Civil"
CPC = "Código de Procedimiento Civil"
COT = "Código Orgánico de Tribunales"

TERMINOS = [
    # ------------------------------------------------------------------ Derecho Civil
    (CIVIL, "Acto jurídico", "Manifestación de voluntad hecha con el propósito de crear, "
     "modificar o extinguir derechos, que produce los efectos queridos porque el derecho la "
     "sanciona.", f"{CC}, art. 1445 (doctrina)"),
    (CIVIL, "Accesión", "Modo de adquirir por el cual el dueño de una cosa pasa a serlo de lo "
     "que ella produce o de lo que se junta a ella.", f"{CC}, art. 643"),
    (CIVIL, "Buena fe", "En materia posesoria, conciencia de haberse adquirido el dominio de la "
     "cosa por medios legítimos, exentos de fraude y de todo otro vicio.", f"{CC}, art. 706"),
    (CIVIL, "Comodato", "Contrato en que una parte entrega gratuitamente a otra una especie, "
     "mueble o raíz, para que haga uso de ella con cargo de restituir la misma especie después "
     "de terminado el uso.", f"{CC}, art. 2174"),
    (CIVIL, "Cuasicontrato", "Hecho voluntario, lícito y no convencional que genera "
     "obligaciones, como la agencia oficiosa o el pago de lo no debido.", f"{CC}, arts. 2284 "
     "y 2285"),
    (CIVIL, "Dolo", "Intención positiva de inferir injuria a la persona o propiedad de otro.",
     f"{CC}, art. 44"),
    (CIVIL, "Daño emergente", "Pérdida efectiva que sufre el acreedor en su patrimonio por el "
     "incumplimiento de la obligación.", f"{CC}, art. 1556"),
    (CIVIL, "Error", "Falso concepto de la realidad que vicia el consentimiento en los casos "
     "que la ley señala, por ejemplo cuando recae sobre la especie del acto o la identidad de "
     "la cosa.", f"{CC}, arts. 1453 a 1455"),
    (CIVIL, "Fuerza", "Vicio del consentimiento que consiste en una presión física o moral capaz "
     "de producir una impresión fuerte en una persona de sano juicio.", f"{CC}, art. 1456"),
    (CIVIL, "Gananciales", "Utilidades del haber social que, al liquidarse la sociedad "
     "conyugal, se dividen por mitad entre los cónyuges o sus herederos.", f"{CC}, art. 1774"),
    (CIVIL, "Hipoteca", "Derecho de prenda constituido sobre inmuebles que no dejan por eso de "
     "permanecer en poder del deudor.", f"{CC}, art. 2407"),
    (CIVIL, "Interdicción", "Declaración judicial que priva a una persona de la administración "
     "de sus bienes, como al demente o al disipador.", f"{CC}, arts. 443 y 456"),
    (CIVIL, "Inoponibilidad", "Ineficacia, respecto de terceros, de un acto válido o de su "
     "nulidad, por ejemplo por falta de publicidad.", f"{CC}, arts. 1707 y 2160 (doctrina)"),
    (CIVIL, "Lesión enorme", "Perjuicio que sufre el vendedor de un inmueble cuando el precio "
     "que recibe es inferior a la mitad del justo precio, o el comprador cuando el justo precio "
     "es inferior a la mitad del que paga.", f"{CC}, arts. 1888 y 1889"),
    (CIVIL, "Legítima", "Cuota de los bienes de un difunto que la ley reserva a ciertos herederos "
     "forzosos, como los hijos, el cónyuge o los ascendientes.", f"{CC}, arts. 1181 y 1182"),
    (CIVIL, "Mutuo", "Contrato en que una parte entrega a otra cierta cantidad de cosas "
     "fungibles con cargo de restituir otras tantas del mismo género y calidad.",
     f"{CC}, art. 2196"),
    (CIVIL, "Mora", "Retardo imputable en el cumplimiento de una obligación, que se produce "
     "por regla general cuando el deudor ha sido judicialmente reconvenido.", f"{CC}, art. 1551"),
    (CIVIL, "Nulidad", "Sanción legal de todo acto o contrato a que falta alguno de los "
     "requisitos que la ley prescribe para su valor según su especie y la calidad o estado de "
     "las partes.", f"{CC}, art. 1681"),
    (CIVIL, "Novación", "Sustitución de una nueva obligación a otra anterior, la cual queda por "
     "tanto extinguida.", f"{CC}, art. 1628"),
    (CIVIL, "Ocupación", "Modo de adquirir el dominio de las cosas que no pertenecen a nadie y "
     "cuya adquisición no está prohibida por las leyes chilenas o el derecho internacional.",
     f"{CC}, art. 606"),
    (CIVIL, "Obligación natural", "La que no confiere derecho para exigir su cumplimiento, pero "
     "que, cumplida, autoriza para retener lo que se ha dado o pagado en razón de ella.",
     f"{CC}, art. 1470"),
    (CIVIL, "Prescripción", "Modo de adquirir las cosas ajenas o de extinguir las acciones y "
     "derechos ajenos por haberse poseído las cosas o no haberse ejercido dichas acciones "
     "durante cierto lapso.", f"{CC}, art. 2492"),
    (CIVIL, "Pago", "Prestación de lo que se debe; modo de extinguir las obligaciones.",
     f"{CC}, art. 1568"),
    (CIVIL, "Quirografario", "Se dice del crédito de quinta clase, que no goza de preferencia y "
     "se paga a prorrata sobre el sobrante de los bienes del deudor.", f"{CC}, art. 2489"),
    (CIVIL, "Rescisión", "Nombre que el Código da a la nulidad relativa.", f"{CC}, art. 1682"),
    (CIVIL, "Representación", "Lo que una persona ejecuta a nombre de otra, estando facultada "
     "por ella o por la ley, produce respecto del representado iguales efectos que si él mismo "
     "hubiese contratado.", f"{CC}, art. 1448"),
    (CIVIL, "Servidumbre", "Gravamen impuesto sobre un predio en utilidad de otro predio de "
     "distinto dueño.", f"{CC}, art. 820"),
    (CIVIL, "Tradición", "Modo de adquirir el dominio que consiste en la entrega que el dueño "
     "hace de una cosa a otro, con facultad e intención de transferir y capacidad e intención "
     "de adquirir.", f"{CC}, art. 670"),
    (CIVIL, "Transacción", "Contrato en que las partes terminan extrajudicialmente un litigio "
     "pendiente o precaven un litigio eventual.", f"{CC}, art. 2446"),
    (CIVIL, "Usufructo", "Derecho real que consiste en la facultad de gozar de una cosa con "
     "cargo de conservar su forma y sustancia y de restituirla a su dueño.", f"{CC}, art. 764"),
    (CIVIL, "Vicio redhibitorio", "Defecto oculto de la cosa vendida, existente al tiempo de la "
     "venta, que la hace impropia para su uso natural o hace que solo sirva imperfectamente.",
     f"{CC}, arts. 1857 y 1858"),
    # --------------------------------------------------------------- Derecho Procesal
    (PROCESAL, "Árbitro", "Juez nombrado por las partes, o por la autoridad judicial en "
     "subsidio, para la resolución de un asunto litigioso.", f"{COT}, art. 222"),
    (PROCESAL, "Absolución de posiciones", "Medio para obtener la confesión judicial de la "
     "contraparte, que declara bajo juramento sobre los hechos que se le preguntan.",
     f"{CPC}, arts. 385 y siguientes"),
    (PROCESAL, "Bilateralidad de la audiencia", "Principio según el cual ninguna resolución "
     "debe dictarse sin oír a la parte contra la que se pide, o sin darle la oportunidad de "
     "ser oída.", "Doctrina; Constitución Política, art. 19 n.º 3"),
    (PROCESAL, "Competencia", "Facultad que tiene cada juez o tribunal para conocer de los "
     "negocios que la ley ha colocado dentro de la esfera de sus atribuciones.",
     f"{COT}, art. 108"),
    (PROCESAL, "Cosa juzgada", "Efecto de las sentencias firmes que impide volver a discutir lo "
     "resuelto y permite exigir su cumplimiento.", f"{CPC}, arts. 175 a 177"),
    (PROCESAL, "Demanda", "Acto procesal con que el actor ejerce su acción e inicia el juicio, "
     "y que debe cumplir los requisitos legales.", f"{CPC}, art. 254"),
    (PROCESAL, "Emplazamiento", "Notificación válida de la demanda y transcurso del plazo que la "
     "ley da al demandado para comparecer y defenderse.", f"{CPC}, art. 795 n.º 1 (doctrina)"),
    (PROCESAL, "Exhorto", "Comunicación que un tribunal dirige a otro para que practique o "
     "haga practicar en su territorio una diligencia judicial.", f"{CPC}, art. 71"),
    (PROCESAL, "Fuero mayor", "Alteración de la competencia en razón de la calidad de alguna de "
     "las partes, que lleva el asunto a un tribunal de mayor jerarquía.", f"{COT}, art. 133"),
    (PROCESAL, "Gestión preparatoria", "Trámite previo que permite al acreedor obtener un "
     "título ejecutivo que no tiene, como el reconocimiento de firma o la confesión de deuda.",
     f"{CPC}, art. 435"),
    (PROCESAL, "Hecho sustancial, pertinente y controvertido", "Requisito de los hechos que el "
     "tribunal fija en la resolución que recibe la causa a prueba.", f"{CPC}, art. 318"),
    (PROCESAL, "Incidente", "Toda cuestión accesoria de un juicio que requiera pronunciamiento "
     "especial con audiencia de las partes.", f"{CPC}, art. 82"),
    (PROCESAL, "Jurisdicción", "Poder deber del Estado de resolver, mediante el proceso y con "
     "efecto de cosa juzgada, los conflictos de relevancia jurídica.", f"{COT}, art. 1 "
     "(doctrina)"),
    (PROCESAL, "Litispendencia", "Excepción dilatoria fundada en la existencia de otro juicio "
     "pendiente entre las mismas partes y sobre la misma materia.", f"{CPC}, art. 303 n.º 3"),
    (PROCESAL, "Medida precautoria", "Medida que puede pedir el demandante para asegurar el "
     "resultado de la acción, como el secuestro o la retención de bienes.", f"{CPC}, art. 290"),
    (PROCESAL, "Notificación", "Actuación judicial que pone en conocimiento de las partes, o de "
     "terceros, una resolución del tribunal.", f"{CPC}, art. 38"),
    (PROCESAL, "Querella", "Forma en que la víctima u otros legitimados ejercen la acción penal "
     "en el proceso penal.", "Código Procesal Penal, arts. 111 a 113"),
    (PROCESAL, "Rebeldía", "Declaración del tribunal de que una parte no realizó un trámite "
     "dentro del plazo legal, con lo que el juicio sigue adelante sin ese trámite.",
     f"{CPC}, art. 78"),
    (PROCESAL, "Sentencia definitiva", "Resolución que pone fin a la instancia, resolviendo la "
     "cuestión o asunto que ha sido objeto del juicio.", f"{CPC}, art. 158"),
    (PROCESAL, "Ultra petita", "Vicio de la sentencia que otorga más de lo pedido por las "
     "partes o se extiende a puntos no sometidos a la decisión del tribunal.",
     f"{CPC}, art. 768 n.º 4"),
    (PROCESAL, "Vista de la causa", "Trámite ante un tribunal colegiado en que se conoce el "
     "asunto mediante la relación y los alegatos de los abogados.", f"{CPC}, arts. 222 y 223"),
]


def main() -> int:
    out = ROOT / "salida" / "glosario-civil-procesal.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = SHEET
    sheet.append(COLUMNS)
    for row in TERMINOS:
        sheet.append(list(row))
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for column, width in zip("ABCD", (20, 30, 90, 40), strict=True):
        sheet.column_dimensions[column].width = width
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    workbook.save(out)
    terms, errors = parse_glossary(out.read_bytes())
    for row, message in errors:
        print(f"ERR fila {row}: {message}")
    print(f"{out.name}: {len(terms)} términos válidos de {len(TERMINOS)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
