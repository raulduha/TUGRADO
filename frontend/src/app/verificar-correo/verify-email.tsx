"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useActionState } from "react";

import { Alert } from "@/components/alert";
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
        <LinkButton href="/iniciar-sesion">Iniciar sesión</LinkButton>
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

function LinkButton({ href, children }: { href: string; children: string }) {
  return (
    <Link
      href={href}
      className="flex w-full items-center justify-center rounded-lg bg-brand px-4 py-2.5 text-base font-semibold text-on-brand hover:bg-brand-strong focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand"
    >
      {children}
    </Link>
  );
}
