import { expect, test } from "@playwright/test";

// Gate 10: las pantallas deben poder usarse en móvil, tablet y escritorio, sin
// desplazamiento horizontal y con sus controles principales visibles.
const PAGES = [
  { path: "/", heading: "Llega a tu examen de grado con confianza" },
  { path: "/registro", heading: "Crea tu cuenta" },
  { path: "/iniciar-sesion", heading: "Inicia sesión" },
  { path: "/recuperar-contrasena", heading: "Recupera tu contraseña" },
  { path: "/verificar-correo?token=x", heading: "Verifica tu correo" },
  { path: "/restablecer-contrasena?token=x", heading: "Elige una nueva contraseña" },
  { path: "/privacidad", heading: "Política de privacidad" },
  { path: "/terminos", heading: "Términos y condiciones" },
  { path: "/correos/baja?token=x", heading: "Recordatorios por correo" },
];

for (const { path, heading } of PAGES) {
  test(`${path} se adapta al ancho de la pantalla`, async ({ page }, testInfo) => {
    await page.goto(path);
    await expect(page.getByRole("heading", { level: 1, name: heading })).toBeVisible();

    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow, "no debe haber desplazamiento horizontal").toBeLessThanOrEqual(0);

    for (const button of await page.getByRole("button").all()) {
      await expect(button).toBeInViewport();
    }
    await page.screenshot({
      path: testInfo.outputPath(`${path.replace(/[/?=]/g, "_") || "inicio"}.png`),
      fullPage: true,
    });
  });
}
