import { buttonStyles } from "@/components/button";

export function SubmitButton({ pending, children }: { pending: boolean; children: string }) {
  return (
    <button type="submit" disabled={pending} aria-busy={pending} className={`w-full ${buttonStyles.primary}`}>
      {pending ? "Procesando…" : children}
    </button>
  );
}
