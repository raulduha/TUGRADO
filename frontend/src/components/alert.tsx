import type { ReactNode } from "react";

const STYLES = {
  error: "border-danger/40 bg-danger/10 text-danger",
  success: "border-success/40 bg-success/10 text-success",
  info: "border-line bg-background text-foreground",
} as const;

export function Alert({ tone, children }: { tone: keyof typeof STYLES; children: ReactNode }) {
  // Los errores interrumpen al lector de pantalla; el resto se anuncia sin interrumpir.
  return (
    <div
      role={tone === "error" ? "alert" : "status"}
      className={`rounded-lg border px-4 py-3 text-sm ${STYLES[tone]}`}
    >
      {children}
    </div>
  );
}
