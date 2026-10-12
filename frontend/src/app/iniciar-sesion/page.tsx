import type { Metadata } from "next";
import Link from "next/link";
import { Suspense } from "react";

import { AuthShell } from "@/components/auth-shell";

import { LoginForm } from "./login-form";

export const metadata: Metadata = { title: "Iniciar sesión" };

export default function LoginPage() {
  return (
    <AuthShell
      title="Inicia sesión"
      footer={
        <>
          ¿No tienes cuenta?{" "}
          <Link href="/registro" className="font-medium text-brand underline-offset-4 hover:underline">
            Crea una
          </Link>
        </>
      }
    >
      {/* El formulario lee ?next= de la URL: va dentro de Suspense (Cache Components). */}
      <Suspense>
        <LoginForm />
      </Suspense>
    </AuthShell>
  );
}
