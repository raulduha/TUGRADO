"use client";

import Link from "next/link";
import { useActionState } from "react";

import { Alert } from "@/components/alert";
import { AuthShell } from "@/components/auth-shell";
import { Field } from "@/components/field";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";

type State = { status: "idle" } | { status: "sent" } | { status: "error"; message: string };

async function requestReset(_: State, form: FormData): Promise<State> {
  const result = await api("/auth/password-reset/request", {
    body: { email: String(form.get("email") ?? "") },
  });
  return result.ok ? { status: "sent" } : { status: "error", message: result.error.message };
}

export default function RequestResetPage() {
  const [state, action, pending] = useActionState(requestReset, { status: "idle" });

  return (
    <AuthShell
      title="Recupera tu contraseña"
      description="Te enviaremos un enlace para elegir una nueva. Vale 30 minutos."
      footer={
        <Link href="/iniciar-sesion" className="font-medium text-brand underline-offset-4 hover:underline">
          Volver a iniciar sesión
        </Link>
      }
    >
      {state.status === "sent" ? (
        <Alert tone="success">
          Si el correo está registrado, te enviamos un enlace para restablecer tu contraseña.
        </Alert>
      ) : (
        <form action={action} className="space-y-5">
          {state.status === "error" ? <Alert tone="error">{state.message}</Alert> : null}
          <Field label="Correo" name="email" type="email" autoComplete="email" />
          <SubmitButton pending={pending}>Enviar enlace</SubmitButton>
        </form>
      )}
    </AuthShell>
  );
}
