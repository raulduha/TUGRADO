import { defineConfig } from "@playwright/test";

// Pruebas de interfaz contra la app ya levantada (frontend en :3000 y backend en Docker).
// Usa el Chrome instalado en el equipo: no descarga navegadores.
export default defineConfig({
  testDir: "e2e",
  outputDir: "e2e/.results",
  use: {
    baseURL: process.env.E2E_BASE_URL ?? "http://localhost:3000",
    channel: "chrome",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "movil", use: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } },
    { name: "tablet", use: { viewport: { width: 768, height: 1024 }, hasTouch: true } },
    { name: "escritorio", use: { viewport: { width: 1280, height: 800 } } },
  ],
});
