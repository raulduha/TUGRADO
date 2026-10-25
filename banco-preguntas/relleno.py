"""Relleno de prueba para las electivas que aún no tienen preguntas.

Genera preguntas evidentemente falsas («[Relleno] …») sobre los subtemas reales del temario, para
ver la ruta, el plan diario y la práctica con todas las materias mientras se redacta el contenido
real. NO es contenido jurídico: solo se carga en el entorno local y nunca debe publicarse en
producción.

Ejecutar desde backend/, con el backend local arriba:

    uv run python ../banco-preguntas/relleno.py            # genera la planilla
    uv run python ../banco-preguntas/relleno.py --cargar   # además la importa y publica en local

La carga usa la API como lo haría un administrador (la autora importa y envía a revisión; el
revisor aprueba y publica), con las cuentas demo; se cambian con RELLENO_AUTORA, RELLENO_REVISOR y
RELLENO_CLAVE. Solo acepta un backend en 127.0.0.1 o localhost.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))

from app.content.spreadsheet import COLUMNS, SHEET, parse_workbook  # noqa: E402

SALIDA = ROOT / "salida" / "relleno-electivas-NO-PUBLICAR.xlsx"
MARCA = "[Relleno]"
POR_SUBTEMA = 2

# Materia → subtemas, según el temario (frontend/src/lib/temario.ts).
ELECTIVAS = {
    "Derecho Administrativo II": [
        "El contrato administrativo",
        "Principales figuras contractuales",
        "Concesiones, permisos y licencias",
        "Ingreso y principios",
        "Probidad administrativa",
        "Responsabilidad administrativa",
        "Control jurisdiccional",
        "Control administrativo",
    ],
    "Derecho Canónico": [
        "Naturaleza jurídica de la Iglesia",
        "Fieles: derechos y deberes",
        "Bautismo",
        "Orden sagrado",
        "Matrimonio",
        "Magisterio",
        "Enseñanza religiosa en Chile",
        "Funciones legislativa, judicial y ejecutiva",
        "Estructura jerárquica de la Iglesia",
    ],
    "Derecho Comercial II (Títulos de crédito)": [
        "El dinero y los medios de pago",
        "Letra de cambio",
        "Pagaré",
        "Descuento y factoring",
        "Operaciones de crédito de dinero",
        "Mutuo, apertura de crédito, depósito y cuenta corriente mercantil",
        "Operaciones bancarias",
        "Prenda mercantil y prendas especiales",
    ],
    "Derecho Comercial III (Concursal)": [
        "Responsabilidad del comerciante individual",
        "Introducción y reglas generales del Derecho concursal",
        "Reorganización judicial y extrajudicial",
        "Liquidación de la empresa deudora y de la persona deudora",
        "Renegociación de la persona deudora",
        "Acciones revocatorias concursales",
        "Insolvencia transfronteriza",
    ],
    "Historia del Derecho": [
        "El sustrato jurídico común de Occidente",
        "Difusión castellana de la tradición jurídica: el Derecho Indiano",
        "Independencia de Chile y Constitución de 1833",
        "La codificación en Chile desde 1855",
        "Cambios del ordenamiento jurídico y Constitución de 1925",
        "La crisis del Estado de Derecho en Chile",
    ],
    "Derecho Internacional Público": [
        "Tratados internacionales",
        "Derecho internacional y derecho chileno",
        "El Estado",
        "Organizaciones internacionales",
        "La persona y los sistemas de derechos humanos",
        "Responsabilidad internacional",
        "Solución pacífica de controversias",
        "Uso de la fuerza",
    ],
    "Derecho Natural": [
        "Ética, orden moral y orden jurídico",
        "Fin último y acto humano",
        "Las virtudes: prudencia, fortaleza, templanza y justicia",
        "Ley y conciencia: ley eterna, natural y positiva",
        "Derecho natural: parte especial",
    ],
    "Derecho Romano": [
        "Fuentes del Derecho romano y su evolución",
        "Personas",
        "Procedimiento y acciones",
        "Los bienes",
        "Las obligaciones y sus fuentes",
        "Las sucesiones",
    ],
    "Derecho Tributario": [
        "Norma general antielusión",
        "Principios constitucionales",
        "Fuentes y la obligación tributaria",
        "El proceso tributario",
        "Primera categoría",
        "Impuestos al trabajo",
        "Impuesto adicional",
    ],
    "Fundamentos del Derecho": [
        "Naturaleza del conocimiento filosófico",
        "El hombre como sujeto de derecho: consideración antropológica",
        "El hombre como sujeto de derecho: consideración metafísica",
        "El hombre como sujeto de derecho: consideración teológica",
        "El hombre como ser personal y los fundamentos del derecho",
    ],
}


def filas() -> list[list]:
    rows = []
    n = 0
    for materia, subtemas in ELECTIVAS.items():
        for subtema in subtemas:
            for i in range(1, POR_SUBTEMA + 1):
                correcta = "ABCD"[n % 4]
                n += 1
                opciones = [
                    f"Alternativa {letra}"
                    + (" (la correcta en este ejemplo)" if letra == correcta else "")
                    for letra in "ABCD"
                ]
                rows.append(
                    [
                        materia,
                        subtema,
                        1 + (i % 3),
                        f"{MARCA} Pregunta de ejemplo {i} sobre «{subtema}».",
                        *opciones,
                        None,
                        correcta,
                        "Pregunta de relleno para probar la app: aún no hay contenido real para "
                        "este subtema.",
                        "Relleno de prueba: no es contenido jurídico",
                    ]
                )
    return rows


def generar() -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = SHEET
    ws.append(COLUMNS)
    for row in filas():
        ws.append(row)
    SALIDA.parent.mkdir(exist_ok=True)
    wb.save(SALIDA)
    parsed, errors = parse_workbook(SALIDA.read_bytes())
    if errors:
        raise SystemExit("\n".join(f"fila {e.row}: {e.message}" for e in errors))
    print(f"{SALIDA.name}: {len(parsed)} preguntas en {len(ELECTIVAS)} materias")
    return SALIDA


def cargar(planilla: Path) -> None:
    import httpx

    base = os.environ.get("RELLENO_BACKEND", "http://127.0.0.1:8000")
    if urlparse(base).hostname not in ("127.0.0.1", "localhost"):
        raise SystemExit("El relleno solo se carga en un backend local.")
    clave = os.environ.get("RELLENO_CLAVE", "demo banco preguntas 2026")

    def sesion(email: str) -> httpx.Client:
        client = httpx.Client(
            base_url=base, headers={"Origin": "http://localhost:3000"}, timeout=120
        )
        response = client.post("/auth/login", json={"email": email, "password": clave})
        if response.status_code != 204:
            raise SystemExit(f"No se pudo iniciar sesión como {email}: {response.status_code}")
        return client

    def relleno(cliente: httpx.Client, status: str | None = None) -> list[str]:
        params = {"q": MARCA, "limit": 500} | ({"status": status} if status else {})
        response = cliente.get("/admin/questions", params=params)
        response.raise_for_status()
        return [v["id"] for v in response.json()]

    autora = sesion(os.environ.get("RELLENO_AUTORA", "demo-autora@ejemplo.cl"))
    # Sin `id` en la planilla, importarla dos veces duplicaría las preguntas.
    if relleno(autora):
        print("El relleno ya estaba importado; solo se publica lo pendiente.")
    else:
        resumen = autora.post("/admin/questions/import", content=planilla.read_bytes()).json()
        print("importadas:", {k: v for k, v in resumen.items() if k != "errors"})
    borradores = relleno(autora, "draft")
    if not borradores:
        print("No hay borradores de relleno por publicar.")
        return
    autora.post("/admin/questions/bulk", json={"action": "submit", "ids": borradores})
    revisor = sesion(os.environ.get("RELLENO_REVISOR", "demo-revisor@ejemplo.cl"))
    for accion in ("approve", "publish"):
        result = revisor.post("/admin/questions/bulk", json={"action": accion, "ids": borradores})
        print(accion, result.json()["done"])


if __name__ == "__main__":
    planilla = generar()
    if "--cargar" in sys.argv:
        cargar(planilla)
