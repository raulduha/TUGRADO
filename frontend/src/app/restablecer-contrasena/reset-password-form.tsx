"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useActionState } from "react";

import { Alert } from "@/components/alert";
import { Field } from "@/components/field";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";

type State =
  | { status: "idle" }
  | { status: "done" }
  | { status: "error"; field?: "password"; message: string };

export function ResetPasswordForm() {
  const token = useSearchParams().get("token");
  const [state, action, pending] = useActionState(
    async (_: State, form: FormData): Promise<State> => {
      const result = await api("/auth/password-reset/confirm", {
        body: { token, password: String(form.get("password") ?? "") },
      });
      if (result.ok) {
        return { status: "done" };
      }
      const field = result.error.code.startsWith("password_") ? "password" : undefined;
      return { status: "error", field, message: result.error.message };
    },
    { status: "idle" },
  );

  if (!token) {
    return <Alert tone="error">El enlace está incompleto. Ábrelo de nuevo desde tu correo.</Alert>;
  }
  if (state.status === "done") {
    return (
      <div className="space-y-5">
        <Alert tone="success">Tu contraseña se actualizó.</Alert>
        <Link
          href="/iniciar-sesion"
          className="flex w-full items-center justify-center rounded-lg bg-brand px-4 py-2.5 text-base font-semibold text-on-brand hover:bg-brand-strong focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand"
        >
          Iniciar sesión
        </Link>
      </div>
    );
  }

  const passwordError =
    state.status === "error" && state.field === "password" ? state.message : undefined;
  return (
    <form action={action} className="space-y-5">
      {state.status === "error" && !passwordError ? (
        <Alert tone="error">
          {state.message}{" "}
          <Link href="/recuperar-contrasena" className="font-medium underline underline-offset-4">
            Pide un enlace nuevo
          </Link>
        </Alert>
      ) : null}
      <Field
        label="Nueva contraseña"
        name="password"
        type="password"
        autoComplete="new-password"
        hint="Mínimo 12 caracteres. Puedes usar una frase; evita contraseñas comunes."
        error={passwordError}
      />
      <SubmitButton pending={pending}>Guardar contraseña</SubmitButton>
    </form>
  );
}
