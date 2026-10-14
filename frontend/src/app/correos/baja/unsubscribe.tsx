"use client";

import { useSearchParams } from "next/navigation";
import { useActionState } from "react";

import { Alert } from "@/components/alert";
import { ButtonLink } from "@/components/button";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";

type State = { status: "idle" } | { status: "done" } | { status: "error"; message: string };

export function Unsubscribe() {
  const token = useSearchParams().get("token");

  // Se confirma con un botón: los antivirus de correo que abren enlaces no dan de baja a nadie.
  const [state, action, pending] = useActionState<State>(async () => {
    const result = await api("/engagement/reminders/unsubscribe", { body: { token } });
    return result.ok ? { status: "done" } : { status: "error", message: result.error.message };
  }, { status: "idle" });

  if (!token) {
    return <Alert tone="error">El enlace está incompleto. Ábrelo de nuevo desde tu correo.</Alert>;
  }
  if (state.status === "done") {
    return (
      <div className="space-y-5">
        <Alert tone="success">
          Listo: ya no te enviaremos recordatorios. Seguirás recibiendo los correos de tu cuenta y
          de tu suscripción.
        </Alert>
        <ButtonLink href="/panel" className="w-full">
          Ir a mi panel
        </ButtonLink>
      </div>
    );
  }
  return (
    <form action={action} className="space-y-5">
      {state.status === "error" ? (
        <Alert tone="error">{state.message}. Ábrelo de nuevo desde el último correo.</Alert>
      ) : (
        <p className="text-sm text-muted">
          Apruvi te escribe cuando llevas un par de días sin entrar. ¿Prefieres no recibir más estos
          recordatorios?
        </p>
      )}
      <SubmitButton pending={pending}>No quiero recibir recordatorios</SubmitButton>
    </form>
  );
}
