"use client";

import { useSearchParams } from "next/navigation";
import { useActionState } from "react";

import { Alert } from "@/components/alert";
import { ButtonLink } from "@/components/button";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";

type State = { status: "idle" } | { status: "verified" } | { status: "error"; message: string };

export function VerifyEmail() {
  const token = useSearchParams().get("token");

  // Se confirma con un botón, no al cargar la página: así los antivirus de correo que abren
  // enlaces no consumen el token de un solo uso por el estudiante.
  const [state, action, pending] = useActionState<State>(async () => {
    const result = await api("/auth/verify-email", { body: { token } });
    return result.ok ? { status: "verified" } : { status: "error", message: result.error.message };
  }, { status: "idle" });

  if (!token) {
    return <Alert tone="error">El enlace está incompleto. Ábrelo de nuevo desde tu correo.</Alert>;
  }
  if (state.status === "verified") {
    return (
      <div className="space-y-5">
        <Alert tone="success">Tu correo quedó verificado. Ya puedes iniciar sesión.</Alert>
        <ButtonLink href="/iniciar-sesion" className="w-full">
          Iniciar sesión
        </ButtonLink>
      </div>
    );
  }
  return (
    <form action={action} className="space-y-5">
      {state.status === "error" ? (
        <Alert tone="error">
          {state.message} Puedes pedir un enlace nuevo al iniciar sesión.
        </Alert>
      ) : (
        <p className="text-sm text-muted">Confirma que este correo es tuyo para activar tu cuenta.</p>
      )}
      <SubmitButton pending={pending}>Confirmar mi correo</SubmitButton>
    </form>
  );
}
