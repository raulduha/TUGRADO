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

const E2E_ACCOUNTS = `u.email LIKE '${E2E_EMAIL_PREFIX}%@ejemplo.cl'`;

/** Acceso de cortesía (FR-032) con el CLI del backend: la cuenta entra al panel sin suscripción. */
export function grantAccess(email: string): void {
  docker([
    "exec",
    "-T",
    "backend",
    "python",
    "-m",
    "app.cli",
    "grant-access",
    "--email",
    email,
    "--reason",
    "Prueba e2e",
    "--by",
    "e2e@ejemplo.cl",
  ]);
}

/** Crea un administrador con el CLI del backend (contraseña por ADMIN_PASSWORD). */
export function createAdmin(email: string): void {
  docker([
    "exec",
    "-T",
    "-e",
    `ADMIN_PASSWORD=${E2E_PASSWORD}`,
    "backend",
    "python",
    "-m",
    "app.cli",
    "create-admin",
    "--email",
    email,
  ]);
}

/** Borra las cuentas creadas por las pruebas, con sus suscripciones (los comentarios se borran en cascada). */
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
    // Las suscripciones y sus eventos no se borran en cascada (RESTRICT): primero ellos.
    [
      // Contenido creado por administradores e2e (autor, revisor y actor son RESTRICT).
      `CREATE TEMP TABLE e2e_users AS SELECT id FROM user_account u WHERE ${E2E_ACCOUNTS};`,
      `CREATE TEMP TABLE e2e_versions AS SELECT id, question_id FROM question_version WHERE created_by IN (SELECT id FROM e2e_users);`,
      `DELETE FROM practice_attempt WHERE version_id IN (SELECT id FROM e2e_versions) OR user_id IN (SELECT id FROM e2e_users);`,
      `DELETE FROM content_event WHERE version_id IN (SELECT id FROM e2e_versions) OR actor_id IN (SELECT id FROM e2e_users);`,
      `DELETE FROM content_review WHERE version_id IN (SELECT id FROM e2e_versions) OR reviewer_id IN (SELECT id FROM e2e_users);`,
      `DELETE FROM answer_option WHERE version_id IN (SELECT id FROM e2e_versions);`,
      `DELETE FROM question_version WHERE id IN (SELECT id FROM e2e_versions);`,
      `DELETE FROM question q WHERE NOT EXISTS (SELECT 1 FROM question_version v WHERE v.question_id = q.id);`,
      `DELETE FROM subtopic t WHERE NOT EXISTS (SELECT 1 FROM question_version v WHERE v.subtopic_id = t.id);`,
      `DELETE FROM subject s WHERE NOT EXISTS (SELECT 1 FROM question_version v WHERE v.subject_id = s.id) AND NOT EXISTS (SELECT 1 FROM subtopic t WHERE t.subject_id = s.id);`,
      `DELETE FROM billing_event WHERE subscription_id IN (SELECT s.id FROM subscription s JOIN user_account u ON u.id = s.user_id WHERE ${E2E_ACCOUNTS});`,
      `DELETE FROM subscription WHERE user_id IN (SELECT id FROM user_account u WHERE ${E2E_ACCOUNTS});`,
      `DELETE FROM user_account u WHERE ${E2E_ACCOUNTS};`,
    ].join(" "),
  ]);
}
