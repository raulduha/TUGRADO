import type { Metadata } from "next";
import { Suspense } from "react";

import { AuthShell } from "@/components/auth-shell";

import { Unsubscribe } from "./unsubscribe";

export const metadata: Metadata = { title: "Recordatorios por correo" };

export default function UnsubscribePage() {
  return (
    <AuthShell title="Recordatorios por correo">
      <Suspense>
        <Unsubscribe />
      </Suspense>
    </AuthShell>
  );
}
