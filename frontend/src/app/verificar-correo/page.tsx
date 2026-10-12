import type { Metadata } from "next";
import { Suspense } from "react";

import { AuthShell } from "@/components/auth-shell";

import { VerifyEmail } from "./verify-email";

export const metadata: Metadata = { title: "Verificar correo" };

export default function VerifyEmailPage() {
  return (
    <AuthShell title="Verifica tu correo">
      <Suspense>
        <VerifyEmail />
      </Suspense>
    </AuthShell>
  );
}
