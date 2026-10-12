import { execFileSync } from "node:child_process";
import path from "node:path";

// Las pruebas corren contra el entorno local: backend y base en Docker (raíz del repo).
const REPO_ROOT = path.resolve(__dirname, "..", "..");

export const E2E_EMAIL_PREFIX = "e2e-";
export const E2E_PASSWORD = "clave de prueba e2e 2026";

export function uniqueEmail(tag: string): string {
  return `${E2E_EMAIL_PREFIX}${tag}-${Date.now()}-${Math.floor(Math.random() * 1e6)}@ejemplo.cl`;
}

function docker(args: string[]): string {
  return execFileSync("docker", ["compose", ...args], { cwd: REPO_ROOT, encoding: "utf8" });
}

/** En desarrollo los correos se escriben en el log del backend: se lee el último token enviado a `email`. */
export function lastEmailToken(email: string): string {
  const logs = docker(["logs", "backend", "--since", "10m", "--no-log-prefix"]);
  const start = logs.lastIndexOf(`Para: ${email}`);
  if (start === -1) throw new Error(`No hay correo para ${email} en el log del backend`);
  const match = logs.slice(start).match(/token=([\w-]+)/);
  if (!match) throw new Error(`El correo para ${email} no tiene token`);
  return match[1];
}

/** Borra las cuentas creadas por las pruebas (sus comentarios se borran en cascada). */
export function deleteE2eAccounts(): void {
  docker([
    "exec",
    "-T",
    "db",
    "psql",
    "-U",
    "tugrado",
    "-d",
    "tugrado",
    "-c",
    `DELETE FROM user_account WHERE email LIKE '${E2E_EMAIL_PREFIX}%@ejemplo.cl';`,
  ]);
}
