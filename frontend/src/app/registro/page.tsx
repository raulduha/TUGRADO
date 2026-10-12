import type { Metadata } from "next";
import Link from "next/link";

import { AuthShell } from "@/components/auth-shell";

import { RegisterForm } from "./register-form";

export const metadata: Metadata = { title: "Crear cuenta" };

export default function RegisterPage() {
  return (
    <AuthShell
      title="Crea tu cuenta"
      description="Practica y simula tu examen de grado. Te enviaremos un correo para verificar tu cuenta."
      footer={
        <>
          ¿Ya tienes cuenta?{" "}
          <Link href="/iniciar-sesion" className="font-medium text-brand underline-offset-4 hover:underline">
            Inicia sesión
          </Link>
        </>
      }
    >
      <RegisterForm />
    </AuthShell>
  );
}
