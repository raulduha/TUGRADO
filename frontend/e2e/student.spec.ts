import { expect, type Page, test } from "@playwright/test";

import { E2E_PASSWORD, grantAccess, lastEmailToken, uniqueEmail } from "./support";

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
  grantAccess(email);

  await page.getByRole("link", { name: "Iniciar sesión" }).click();
  await login(page, email);

  // Panel
  await expect(page).toHaveURL(/\/panel$/);
  await expect(page.getByRole("heading", { level: 1, name: "¡Hola! Qué bueno verte" })).toBeVisible();
  // Primera visita del día: Apruvi celebra el inicio de la racha.
  const celebration = page.getByRole("dialog", { name: "¡Racha iniciada!" });
  await expect(celebration).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("celebracion.png") });
  await celebration.getByRole("button", { name: "¡Vamos!" }).click();
  await expect(celebration).toBeHidden();
  await expect(page.getByRole("region", { name: "Tu racha" })).toContainText("1 día seguido");
  await expect(page.getByText(`${email} · Estudiante`)).toBeVisible();
  await expect(page.getByRole("img", { name: "Mapa completado al 13 %" })).toBeVisible();
  const map = page.getByRole("region", { name: "Tu mapa de estudio" });
  await expect(map.getByRole("listitem")).toHaveCount(8);
  await expect(map.getByRole("button", { name: /Completado$/ })).toHaveCount(1);
  // Apruvi comenta el nivel que se toca.
  await map.getByRole("button", { name: /^Nivel 5:/ }).click();
  await expect(map.getByText("Apruvi · Nivel 5: Tu primera simulación oral")).toBeVisible();
  await expect(page.getByRole("region", { name: "Tu progreso" }).getByRole("listitem")).toHaveCount(3);
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

test("un estudiante se suscribe con el simulador de pagos y cancela", async ({ page }, testInfo) => {
  const email = uniqueEmail(`${testInfo.project.name}-sub`);
  await registerAndVerify(page, email);
  await page.getByRole("link", { name: "Iniciar sesión" }).click();
  await login(page, email);

  // Sin suscripción no se entra al panel: primero la prueba gratis.
  await expect(page).toHaveURL(/\/suscripcion$/);
  await expect(page.getByRole("heading", { level: 1, name: "Tu suscripción" })).toBeVisible();
  await expect(page.getByText("$9.990 / mes")).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath("suscripcion.png"), fullPage: true });
  // El correo de Mercado Pago viene con el de la cuenta y se puede cambiar.
  const payer = page.getByLabel("Correo de tu cuenta de Mercado Pago");
  await expect(payer).toHaveValue(email);
  await payer.fill(`mp-${email}`);
  await page.getByRole("button", { name: "Comenzar 7 días gratis" }).click();

  // BILLING_PROVIDER=fake: el simulador reemplaza la página de Mercado Pago.
  await expect(page).toHaveURL(/\/suscripcion\/simulador/);
  await page.getByRole("button", { name: "Aprobar pago simulado" }).click();
  await expect(page).toHaveURL(/\/suscripcion\/retorno$/);
  await expect(page.getByText("¡Listo! Tu suscripción está activa.")).toBeVisible();
  await page.getByRole("link", { name: "Ir a mi panel" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "¡Hola! Qué bueno verte" })).toBeVisible();
  await page.getByRole("dialog").getByRole("button", { name: "¡Vamos!" }).click();
  await expect(page.getByRole("region", { name: "Tu suscripción" })).toBeVisible();
  await page.getByRole("link", { name: "Administrar o cancelar" }).click();

  await expect(page.getByText("Tu suscripción está activa.", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Cancelar suscripción" }).click();
  await page.getByRole("button", { name: "Sí, cancelar" }).click();
  await expect(page.getByRole("button", { name: "Comenzar 7 días gratis" })).toBeVisible();

  // Sin acceso, el panel vuelve a llevar a la suscripción.
  await page.goto("/panel");
  await expect(page).toHaveURL(/\/suscripcion$/);
});
