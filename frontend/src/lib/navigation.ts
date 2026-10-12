// Solo rutas internas: evita redirecciones abiertas con ?next=https://otro-sitio.
export function safeNext(next: string | null, fallback = "/panel"): string {
  if (!next || !next.startsWith("/") || next.startsWith("//") || next.startsWith("/\\")) {
    return fallback;
  }
  return next;
}
