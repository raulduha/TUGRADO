"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useActionState, useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { Field } from "@/components/field";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";
import { safeNext } from "@/lib/navigation";

type State =
  | { status: "idle" }
  | { status: "success" }
  | { status: "error"; email: string; code: string; message: string };

async function login(_: State, form: FormData): Promise<State> {
  const email = String(form.get("email") ?? "");
  const password = String(form.get("password") ?? "");
  const result = await api("/auth/login", { body: { email, password } });
  if (result.ok) {
    return { status: "success" };
  }
  return { status: "error", email, code: result.error.code, message: result.error.message };
}

export function LoginForm() {
  const router = useRouter();
  const next = safeNext(useSearchParams().get("next"));
  const [state, action, pending] = useActionState(login, { status: "idle" });

  useEffect(() => {
    if (state.status === "success") {
      router.replace(next);
    }
  }, [state, next, router]);

  const email = state.status === "error" ? state.email : undefined;

  return (
    <form action={action} className="space-y-5">
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
      <SubmitButton pending={pending || state.status === "success"}>Iniciar sesión</SubmitButton>
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
