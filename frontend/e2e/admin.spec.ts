import path from "node:path";

import { expect, type Page, test } from "@playwright/test";

import { createAdmin, E2E_PASSWORD, uniqueEmail } from "./support";

// Banco de preguntas (FR-013, FR-014, AC-029, AC-044): importar y descargar la planilla, revisar y publicar con
// dos administradores. Solo en escritorio: los proyectos corren en paralelo sobre la misma base.

const TEMPLATE = path.resolve(__dirname, "..", "..", "docs", "plantillas", "preguntas-alternativas.xlsx");

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
  await expect(page.getByRole("region", { name: "Detalle" }).getByText(/^Publicada · v1$/)).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("banco.png"), fullPage: true });

  // La pregunta publicada aparece en la práctica (sin aviso de ejemplo).
  await page.goto("/practica");
  await expect(page.getByRole("list", { name: "Alternativas" })).toBeVisible();
  await expect(page.getByText("Vista previa con datos de ejemplo.")).toBeHidden();

  // La pregunta publicada forma parte de la ruta de estudio, en la unidad de su materia.
  await page.goto("/ruta");
  await expect(page.getByRole("heading", { level: 1, name: "Tu ruta de estudio" })).toBeVisible();
  const unit = page.getByRole("region", { name: /: Derecho Civil$/ });
  await expect(unit).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("ruta.png"), fullPage: true });
  await unit.getByRole("link", { name: /^(Empezar|Continuar|Repasar|Abrir \(administrador\))$/ }).first().click();
  await expect(page).toHaveURL(/\/practica\?leccion=/);
  await expect(page.getByRole("list", { name: "Alternativas" })).toBeVisible();

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
