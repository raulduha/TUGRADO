// Cliente de la API. Todas las llamadas van a /api (mismo origen), con la cookie de sesión.

export type ApiError = { code: string; message: string };

export type ApiResult<T> =
  | { ok: true; status: number; data: T }
  | { ok: false; status: number; error: ApiError };

const NETWORK_ERROR: ApiError = {
  code: "network_error",
  message: "No pudimos conectar con el servidor. Revisa tu conexión e inténtalo de nuevo.",
};

function toError(status: number, body: unknown): ApiError {
  const detail = (body as { detail?: unknown } | null)?.detail;
  if (detail && typeof detail === "object" && "code" in detail && "message" in detail) {
    return detail as ApiError;
  }
  if (status === 422) {
    // Validación de FastAPI (por ejemplo, un correo con formato inválido).
    return { code: "invalid_input", message: "Revisa los datos ingresados." };
  }
  return { code: "unexpected_error", message: "Ocurrió un error inesperado. Inténtalo de nuevo." };
}

export async function api<T = unknown>(
  path: string,
  options: { method?: "GET" | "POST"; body?: unknown } = {},
): Promise<ApiResult<T>> {
  let response: Response;
  try {
    response = await fetch(`/api${path}`, {
      method: options.method ?? (options.body === undefined ? "GET" : "POST"),
      credentials: "same-origin",
      headers: options.body === undefined ? undefined : { "Content-Type": "application/json" },
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
      cache: "no-store",
    });
  } catch {
    return { ok: false, status: 0, error: NETWORK_ERROR };
  }
  const text = await response.text();
  let body: unknown = null;
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = null;
    }
  }
  if (response.ok) {
    return { ok: true, status: response.status, data: body as T };
  }
  return { ok: false, status: response.status, error: toError(response.status, body) };
}

export type Me = { id: string; email: string; roles: Array<"student" | "administrator"> };
