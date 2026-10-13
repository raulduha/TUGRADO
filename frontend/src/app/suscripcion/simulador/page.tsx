"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { buttonStyles } from "@/components/button";
import { api } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

/** Reemplaza la página de pago de Mercado Pago cuando BILLING_PROVIDER=fake (desarrollo). */
export default function FakeCheckoutPage() {
  const router = useRouter();
  const { me, setMe } = useRequireUser("/suscripcion/simulador");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function approve() {
    setBusy(true);
    setError(null);
    const result = await api("/billing/fake/approve", { method: "POST" });
    if (result.ok) {
      router.push("/suscripcion/retorno");
      return;
    }
    setError(
      result.status === 404
        ? "El simulador de pagos no está disponible en este entorno."
        : result.error.message,
    );
    setBusy(false);
  }

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-xl flex-1 space-y-6 px-4 py-8">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Pago simulado</h1>
        <Alert tone="info">
          Entorno de desarrollo: esta página reemplaza a Mercado Pago. No se cobra nada.
        </Alert>
        {error ? <Alert tone="error">{error}</Alert> : null}
        <button
          type="button"
          onClick={approve}
          disabled={busy || !me}
          className={`w-full ${buttonStyles.primary}`}
        >
          {busy ? "Aprobando…" : "Aprobar pago simulado"}
        </button>
      </main>
    </div>
  );
}
