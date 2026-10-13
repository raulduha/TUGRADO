"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useActionState, useState } from "react";

import { Alert } from "@/components/alert";
import { Field } from "@/components/field";
import { GoogleButton } from "@/components/google-button";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";
import { safeNext } from "@/lib/navigation";

type State =
  | { status: "idle" }
  | { status: "error"; email: string; code: string; message: string };

export function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const next = safeNext(searchParams.get("next"));
  // La redirección ocurre en el envío y el estado vuelve a "idle": con Cache Components la
  // página se conserva (Activity) y un estado "éxito" guardado redirigiría otra vez al volver.
  const [state, action, pending] = useActionState(
    async (_: State, form: FormData): Promise<State> => {
      const email = String(form.get("email") ?? "");
      const password = String(form.get("password") ?? "");
      const result = await api("/auth/login", { body: { email, password } });
      if (result.ok) {
        router.replace(next);
        return { status: "idle" };
      }
      return { status: "error", email, code: result.error.code, message: result.error.message };
    },
    { status: "idle" },
  );

  const email = state.status === "error" ? state.email : undefined;
  const googleFailed = searchParams.get("error") === "google";

  return (
    <form action={action} className="space-y-5">
      <GoogleButton next={next} />
      {googleFailed && state.status === "idle" ? (
        <Alert tone="error">
          No pudimos completar el ingreso con Google. Inténtalo de nuevo o usa tu correo.
        </Alert>
      ) : null}
      {state.status === "error" ? (
        <Alert tone="error">
          <p>{state.message}</p>
          {state.code === "email_not_verified" ? <ResendVerification email={state.email} /> : null}
        </Alert>
      ) : null}
      <Field label="Correo" name="email" type="email" autoComplete="email" defaultValue={email} />
      <Field label="Contraseña" name="password" type="password" autoComplete="current-password" />
      <div className="text-right text-sm">
        <Link
          href="/recuperar-contrasena"
          className="font-medium text-brand underline-offset-4 hover:underline"
        >
          ¿Olvidaste tu contraseña?
        </Link>
      </div>
      <SubmitButton pending={pending}>Iniciar sesión</SubmitButton>
    </form>
  );
}

function ResendVerification({ email }: { email: string }) {
  const [sent, setSent] = useState(false);
  if (sent) {
    return <p className="mt-2">Te reenviamos el enlace de verificación.</p>;
  }
  return (
    <button
      type="button"
      onClick={async () => {
        await api("/auth/resend-verification", { body: { email } });
        setSent(true);
      }}
      className="mt-2 font-medium underline underline-offset-4"
    >
      Reenviar correo de verificación
    </button>
  );
}
