import path from "node:path";

import { expect, type Page, test } from "@playwright/test";

import { createAdmin, E2E_PASSWORD, uniqueEmail } from "./support";

// Banco de preguntas (FR-013, FR-014, AC-029, AC-044, AC-046): planilla, revisión con dos
// administradores, CRUD desde el panel y ruta de estudio, también en el ancho de un celular.
// Solo en el proyecto de escritorio: los proyectos corren en paralelo sobre la misma base.

const TEMPLATE = path.resolve(__dirname, "..", "..", "docs", "plantillas", "preguntas-alternativas.xlsx");

const PHONE = { width: 390, height: 844 };
const DESKTOP = { width: 1280, height: 900 };

/** Gate 10: la pantalla no se desplaza hacia el lado. */
async function expectNoHorizontalScroll(page: Page) {
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow, "no debe haber desplazamiento horizontal").toBeLessThanOrEqual(0);
}

async function loginAs(page: Page, email: string) {
  await page.goto("/iniciar-sesion");
  await page.getByLabel("Correo").fill(email);
  await page.getByLabel("Contraseña", { exact: true }).fill(E2E_PASSWORD);
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page).toHaveURL(/\/panel$/);
  // Primera visita del día: se cierra la celebración de la racha.
  await page.getByRole("dialog").getByRole("button", { name: "¡Vamos!" }).click();
}

test("una autora importa y otro administrador revisa y publica", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "escritorio", "Solo en escritorio (datos compartidos)");
  const author = uniqueEmail("admin-autora");
  const reviewer = uniqueEmail("admin-revisor");
  createAdmin(author);
  createAdmin(reviewer);

  await loginAs(page, author);
  await page.getByRole("link", { name: "Preguntas" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Banco de preguntas" })).toBeVisible();
  await page.locator('input[type="file"]').setInputFiles(TEMPLATE);
  await expect(
    page.getByText("Listo: 2 preguntas nuevas. Lo nuevo y lo modificado queda como borrador."),
  ).toBeVisible();

  // El banco se descarga como Excel para editarlo y volver a subirlo.
  const download = page.waitForEvent("download");
  await page.getByRole("link", { name: "Descargar banco (.xlsx)" }).click();
  expect((await download).suggestedFilename()).toMatch(/^banco-preguntas-\d{4}-\d{2}-\d{2}\.xlsx$/);

  await page.getByRole("tab", { name: "Borrador" }).click();
  await page.getByRole("region", { name: "Versiones" }).getByRole("button", { name: /existencia legal/ }).first().click();
  await page.getByRole("button", { name: "Enviar a revisión" }).click();
  await expect(page.getByText("Tú creaste esta versión: otro administrador debe revisarla.")).toBeVisible();

  // Otro administrador aprueba y publica.
  await page.getByRole("button", { name: "Cerrar sesión" }).click();
  await loginAs(page, reviewer);
  await page.goto("/admin/preguntas");
  await page.getByRole("tab", { name: "En revisión" }).click();
  await page.getByRole("region", { name: "Versiones" }).getByRole("button", { name: /existencia legal/ }).first().click();
  await page.getByRole("button", { name: "Aprobar", exact: true }).click();
  await page.getByRole("button", { name: "Publicar", exact: true }).click();
  await expect(page.getByRole("region", { name: "Detalle" }).getByText(/^Publicada · v1$/).first()).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("banco.png"), fullPage: true });

  // La pregunta publicada aparece en la práctica (sin aviso de ejemplo).
  await page.goto("/practica");
  await expect(page.getByRole("list", { name: "Alternativas" })).toBeVisible();
  await expect(page.getByText("Vista previa con datos de ejemplo.")).toBeHidden();

  // La pregunta publicada forma parte de la ruta de estudio, en la unidad de su materia
  // (revisado en el ancho de un celular).
  await page.setViewportSize(PHONE);
  await page.goto("/ruta");
  await expect(page.getByRole("heading", { level: 1, name: "Tu ruta de estudio" })).toBeVisible();
  const unit = page.getByRole("region", { name: /: Derecho Civil$/ });
  await expect(unit).toBeVisible();
  await expectNoHorizontalScroll(page);
  await page.screenshot({ path: testInfo.outputPath("ruta.png"), fullPage: true });

  // Plan diario (FR-035): con la fecha del examen y la meta, la ruta muestra la cuenta regresiva.
  const examDate = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Santiago" }).format(
    Date.now() + 30 * 24 * 3600 * 1000,
  );
  const planForm = page.getByRole("form", { name: "Tu plan de estudio" });
  await planForm.getByLabel("¿Cuándo das el examen?").fill(examDate);
  await planForm.getByRole("button", { name: "20", exact: true }).click();
  await planForm.getByRole("button", { name: "Guardar mi plan" }).click();
  const today = page.getByRole("region", { name: "Tu plan de hoy" });
  await expect(today).toContainText("Faltan 30 días para tu examen");
  await expect(today.getByRole("img", { name: /de 20 preguntas hoy$/ })).toBeVisible();
  await expect(unit).toContainText(/Preparación \d+ %/);
  await expectNoHorizontalScroll(page);

  // Sin errores pendientes, el repaso lo dice en vez de mostrar una práctica vacía.
  await page.goto("/practica?repaso=1");
  await expect(page.getByRole("heading", { name: "Estás al día con tus repasos" })).toBeVisible();
  await page.goto("/ruta");
  await unit.getByRole("link", { name: /^(Empezar|Continuar|Repasar|Abrir \(administrador\))$/ }).first().click();
  await expect(page).toHaveURL(/\/practica\?leccion=/);
  await expect(page.getByRole("list", { name: "Alternativas" })).toBeVisible();
  await expectNoHorizontalScroll(page);
  await page.setViewportSize(DESKTOP);

  // Herramientas de admin: simular un estudiante que completó todo el mapa.
  await page.goto("/panel");
  await page.getByRole("button", { name: "Herramientas de administrador" }).click();
  await page.getByRole("button", { name: "Listo para el examen" }).click();
  await expect(page.getByText("Modo simulación (solo tú lo ves):")).toBeVisible();
  await expect(page.getByRole("img", { name: "Mapa completado al 100 %" })).toBeVisible();
  await expect(page.getByRole("region", { name: "Tu racha" })).toContainText("45 días seguidos");
  await page.screenshot({ path: testInfo.outputPath("devtools.png"), fullPage: true });
  await page.getByRole("checkbox", { name: "Activa" }).uncheck();
  await expect(page.getByText("Modo simulación (solo tú lo ves):")).toBeHidden();
});

test("una administradora crea, edita y descarta una pregunta desde el panel", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "escritorio", "Solo en escritorio (datos compartidos)");
  const admin = uniqueEmail("admin-crud");
  createAdmin(admin);
  const prompt = `¿Qué es la jurisdicción? (${Date.now()})`;

  await loginAs(page, admin);
  await page.goto("/admin/preguntas");
  await page.getByRole("button", { name: "Nueva pregunta" }).click();
  const form = page.getByRole("form", { name: "Nueva pregunta" });
  await form.getByLabel("Materia").fill("Derecho Procesal");
  await form.getByLabel(/Subtema/).fill("La jurisdicción");
  await form.getByLabel("Enunciado").fill(prompt);
  for (const [letter, text] of [
    ["A", "Un poder-deber del Estado"],
    ["B", "Un contrato"],
    ["C", "Una costumbre"],
    ["D", "Un acto administrativo"],
  ]) {
    await form.getByLabel(`Alternativa ${letter}`, { exact: true }).fill(text);
  }
  await form.getByLabel("Explicación").fill("Es el poder-deber de resolver conflictos.");
  await form.getByLabel("Fuente").fill("Código Orgánico de Tribunales, art. 1");
  await form.getByRole("button", { name: "Crear borrador" }).click();

  const panel = page.getByRole("region", { name: "Detalle" });
  await expect(page.getByText("Se creó la pregunta como borrador.")).toBeVisible();
  await expect(panel.getByText(/^Borrador · v1$/).first()).toBeVisible();

  // Editar guarda la versión 2 en borrador; la 1 queda en el historial.
  await panel.getByRole("button", { name: "Editar (crea una versión nueva)" }).click();
  await page.getByRole("form", { name: "Editar pregunta" }).getByLabel("Enunciado").fill(`${prompt} v2`);
  await page.getByRole("button", { name: "Guardar como versión 2" }).click();
  await expect(panel.getByText(/^Borrador · v2$/).first()).toBeVisible();
  await expect(panel.getByRole("region", { name: "Historial de versiones" }).getByRole("listitem")).toHaveCount(2);

  // Descartar pide confirmación y no borra: la versión queda retirada.
  page.once("dialog", (dialog) => void dialog.accept());
  await panel.getByRole("button", { name: "Descartar esta versión" }).click();
  await expect(panel.getByText(/^Retirada · v2$/).first()).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("crud.png"), fullPage: true });

  // En un celular el detalle se abre a pantalla completa y se vuelve a la lista.
  await page.setViewportSize(PHONE);
  await page.goto("/admin/preguntas");
  await expectNoHorizontalScroll(page);
  await page.getByRole("searchbox", { name: "Buscar preguntas" }).fill(prompt);
  await page.getByRole("region", { name: "Versiones" }).getByRole("button", { name: new RegExp(`${prompt.slice(-14, -1)}`) }).first().click();
  await expect(page.getByRole("button", { name: "← Volver a la lista" })).toBeVisible();
  await expectNoHorizontalScroll(page);
  await page.screenshot({ path: testInfo.outputPath("crud-movil.png") });
  await page.getByRole("button", { name: "← Volver a la lista" }).click();
  await expect(page.getByRole("searchbox", { name: "Buscar preguntas" })).toBeVisible();
});
