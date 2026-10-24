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
  // Un archivo (Blob/File) se envía tal cual, en binario; el resto como JSON.
  const isFile = options.body instanceof Blob;
  try {
    response = await fetch(`/api${path}`, {
      method: options.method ?? (options.body === undefined ? "GET" : "POST"),
      credentials: "same-origin",
      headers:
        options.body === undefined
          ? undefined
          : { "Content-Type": isFile ? "application/octet-stream" : "application/json" },
      body:
        options.body === undefined
          ? undefined
          : isFile
            ? (options.body as Blob)
            : JSON.stringify(options.body),
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

export type SubscriptionStatus = "pending" | "authorized" | "paused" | "cancelled";

export type Subscription = {
  status: SubscriptionStatus | null;
  has_access: boolean;
  amount_clp: number;
  trial_days: number;
  next_payment_date: string | null;
  checkout_url: string | null;
  payer_email: string | null;
};

export function formatClp(amount: number): string {
  return new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP" }).format(amount);
}

export function formatDate(iso: string): string {
  return new Intl.DateTimeFormat("es-CL", { dateStyle: "long" }).format(new Date(iso));
}

export type Streak = { current: number; best: number; new_today: boolean; week: boolean[] };

export type PracticeQuestion = {
  id: string;
  subject: string;
  subtopic: string | null;
  difficulty: number;
  prompt: string;
  options: string[];
};

export type LessonSummary = {
  id: string;
  title: string;
  subtopics: string[];
  total: number;
  answered: number;
  correct: number;
  completed: boolean;
  stars: number;
};

export type StudyPath = {
  units: Array<{ subject: string; lessons: LessonSummary[] }>;
  xp: number;
};

export type LessonDetail = LessonSummary & { subject: string; questions: PracticeQuestion[] };

export type PracticeResult = {
  correct: boolean;
  correct_position: number;
  explanation: string;
  source: string;
};
