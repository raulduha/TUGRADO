"use client";

import { useActionState } from "react";

import { Alert } from "@/components/alert";
import { Field } from "@/components/field";
import { GoogleButton } from "@/components/google-button";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";

type State =
  | { status: "idle" }
  | { status: "sent"; email: string }
  | { status: "error"; email: string; field?: "password"; message: string };

async function register(_: State, form: FormData): Promise<State> {
  const email = String(form.get("email") ?? "");
  const password = String(form.get("password") ?? "");
  const result = await api("/auth/register", { body: { email, password } });
  if (result.ok) {
    return { status: "sent", email };
  }
  const field = result.error.code.startsWith("password_") ? "password" : undefined;
  return { status: "error", email, field, message: result.error.message };
}

export function RegisterForm() {
  const [state, action, pending] = useActionState(register, { status: "idle" });

  if (state.status === "sent") {
    return (
      <Alert tone="success">
        <p className="font-medium">Revisa tu correo</p>
        <p className="mt-1">
          Si <strong>{state.email}</strong> es válido, te enviamos un enlace para verificar tu
          cuenta. El enlace vale 24 horas.
        </p>
      </Alert>
    );
  }

  const email = state.status === "error" ? state.email : undefined;
  const passwordError =
    state.status === "error" && state.field === "password" ? state.message : undefined;

  return (
    <form action={action} className="space-y-5">
      <GoogleButton />
      {state.status === "error" && !passwordError ? (
        <Alert tone="error">{state.message}</Alert>
      ) : null}
      <Field label="Correo" name="email" type="email" autoComplete="email" defaultValue={email} />
      <Field
        label="Contraseña"
        name="password"
        type="password"
        autoComplete="new-password"
        hint="Mínimo 12 caracteres. Puedes usar una frase; evita contraseñas comunes."
        error={passwordError}
      />
      <SubmitButton pending={pending}>Crear cuenta</SubmitButton>
    </form>
  );
}
