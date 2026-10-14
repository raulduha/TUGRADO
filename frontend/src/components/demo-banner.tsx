/** Aviso visible en las pantallas que todavía usan datos de ejemplo (mockup). */
export function DemoBanner({ children }: { children: React.ReactNode }) {
  return (
    <p className="rounded-2xl border border-accent/40 bg-accent-soft px-4 py-3 text-sm">
      <span className="font-semibold">Vista previa con datos de ejemplo.</span> {children}
    </p>
  );
}
