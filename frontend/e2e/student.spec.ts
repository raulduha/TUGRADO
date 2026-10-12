import { expect, type Page, test } from "@playwright/test";

import { E2E_PASSWORD, lastEmailToken, uniqueEmail } from "./support";

// Recorrido real de un estudiante contra el backend (AC-036, AC-037, Gate 10).

async function registerAndVerify(page: Page, email: string) {
  await page.goto("/registro");
  await page.getByLabel("Correo").fill(email);
  await page.getByLabel("Contraseña", { exact: true }).fill(E2E_PASSWORD);
  await page.getByRole("button", { name: "Crear cuenta" }).click();
  await expect(page.getByText("Revisa tu correo")).toBeVisible();

  await page.goto(`/verificar-correo?token=${lastEmailToken(email)}`);
  await page.getByRole("button", { name: "Confirmar mi correo" }).click();
  await expect(page.getByText("Tu correo quedó verificado")).toBeVisible();
}

async function login(page: Page, email: string) {
  await page.getByLabel("Correo").fill(email);
  await page.getByLabel("Contraseña", { exact: true }).fill(E2E_PASSWORD);
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
}

test("un estudiante se registra, entra al panel, comenta y cierra sesión", async ({ page }, testInfo) => {
  const email = uniqueEmail(testInfo.project.name);
  await registerAndVerify(page, email);

  await page.getByRole("link", { name: "Iniciar sesión" }).click();
  await login(page, email);

  // Panel
  await expect(page).toHaveURL(/\/panel$/);
  await expect(page.getByRole("heading", { level: 1, name: "¡Hola! Qué bueno verte" })).toBeVisible();
  await expect(page.getByText(`${email} · Estudiante`)).toBeVisible();
  await expect(page.getByRole("img", { name: "Ruta completada al 33 %" })).toBeVisible();
  const route = page.getByRole("region", { name: "Tu ruta" }).getByRole("listitem");
  await expect(route).toHaveCount(6);
  await expect(route.filter({ hasText: "Listo." })).toHaveCount(2);
  await expect(page.getByRole("region", { name: "Tu progreso" }).getByRole("listitem")).toHaveCount(4);
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow, "no debe haber desplazamiento horizontal").toBeLessThanOrEqual(0);
  await page.screenshot({ path: testInfo.outputPath("panel.png"), fullPage: true });

  // Al final de la página, el botón flotante no tapa la última tarjeta.
  await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
  const lastCard = await page
    .getByRole("region", { name: "Tu progreso" })
    .getByRole("listitem")
    .last()
    .boundingBox();
  const floating = await page.getByRole("button", { name: "Enviar comentarios" }).boundingBox();
  expect(lastCard && floating).toBeTruthy();
  const overlaps =
    lastCard!.x < floating!.x + floating!.width &&
    floating!.x < lastCard!.x + lastCard!.width &&
    lastCard!.y < floating!.y + floating!.height &&
    floating!.y < lastCard!.y + lastCard!.height;
  expect(overlaps, "el botón de comentarios no debe tapar contenido").toBe(false);

  // Comentarios
  await page.getByRole("button", { name: "Enviar comentarios" }).click();
  const dialog = page.getByRole("dialog", { name: "¿Cómo te está yendo?" });
  await expect(dialog).toBeVisible();
  await dialog.getByText("Problema", { exact: true }).click();
  await dialog.getByLabel("Tu comentario").fill("Comentario automático de prueba.");
  await expect(dialog.getByText("32 / 2000")).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("comentarios.png") });
  await dialog.getByRole("button", { name: "Enviar" }).click();
  await expect(dialog.getByText("¡Gracias! Leemos todos los comentarios.")).toBeVisible();
  await dialog.getByRole("button", { name: "Cerrar", exact: true }).first().click();
  await expect(dialog).toBeHidden();
  // Al reabrir, el formulario empieza limpio.
  await page.getByRole("button", { name: "Enviar comentarios" }).click();
  await expect(dialog.getByLabel("Tu comentario")).toHaveValue("");
  await page.keyboard.press("Escape");
  await expect(dialog).toBeHidden();

  // Cierre de sesión: el panel deja de ser accesible.
  await page.getByRole("button", { name: "Cerrar sesión" }).click();
  await expect(page).toHaveURL(/\/iniciar-sesion$/);
  await page.goto("/panel");
  await expect(page).toHaveURL(/\/iniciar-sesion\?next=%2Fpanel|\/iniciar-sesion\?next=\/panel/);

  // Volver a entrar: la página de inicio se conserva entre navegaciones (Activity) y no debe
  // quedar en un bucle de redirecciones.
  await login(page, email);
  await expect(page).toHaveURL(/\/panel$/);
  await expect(page.getByText(`${email} · Estudiante`)).toBeVisible();
  await page.waitForTimeout(1000);
  await expect(page).toHaveURL(/\/panel$/);
});

test("sin verificar el correo no se puede entrar", async ({ page }, testInfo) => {
  const email = uniqueEmail(`${testInfo.project.name}-sinverificar`);
  await page.goto("/registro");
  await page.getByLabel("Correo").fill(email);
  await page.getByLabel("Contraseña", { exact: true }).fill(E2E_PASSWORD);
  await page.getByRole("button", { name: "Crear cuenta" }).click();
  await expect(page.getByText("Revisa tu correo")).toBeVisible();

  await page.goto("/iniciar-sesion");
  await login(page, email);
  // Filtra por texto: Next agrega su propio role="alert" (anunciador de rutas).
  await expect(
    page.getByRole("alert").filter({ hasText: "Debes verificar tu correo" }),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Reenviar correo de verificación" })).toBeVisible();
});
