"use client";

import { useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink } from "@/components/button";
import { api, formatDate, providerName, type Subscription } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

/** Vuelta desde la página del proveedor de pagos. Los parámetros de la URL no se usan: el backend consulta el
 * estado real de la suscripción. */
export default function SubscriptionReturnPage() {
  const { me, setMe, error: userError } = useRequireUser("/suscripcion/retorno");
  const [sub, setSub] = useState<Subscription | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!me) return;
    let cancelled = false;
    api<Subscription>("/billing/subscription/sync", { method: "POST" }).then((result) => {
      if (cancelled) return;
      if (result.ok) setSub(result.data);
      else if (result.status !== 401) setError(result.error.message);
    });
    return () => {
      cancelled = true;
    };
  }, [me]);

  const failure = userError ?? error;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-xl flex-1 space-y-6 px-4 py-8">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Estado de tu pago</h1>
        {failure ? <Alert tone="error">{failure}</Alert> : null}
        {!sub && !failure ? (
          <ApruviLoader label="Consultando tu pago…" />
        ) : null}
        {sub ? <Result sub={sub} /> : null}
        <div className="flex flex-col gap-2 sm:flex-row">
          <ButtonLink href="/panel">Ir a mi panel</ButtonLink>
          <ButtonLink href="/suscripcion" variant="secondary">
            Ver mi suscripción
          </ButtonLink>
        </div>
      </main>
    </div>
  );
}

function Result({ sub }: { sub: Subscription }) {
  if (sub.status === "authorized") {
    return (
      <Alert tone="success">
        <p className="font-medium">¡Listo! Tu suscripción está activa.</p>
        {sub.next_payment_date ? (
          <p className="mt-1">Próximo cobro: {formatDate(sub.next_payment_date)}.</p>
        ) : null}
      </Alert>
    );
  }
  if (sub.status === "pending") {
    return (
      <Alert tone="info">
        {providerName(sub.provider)} aún no confirma tu pago. Puede tardar unos minutos: vuelve a
        revisar desde tu suscripción.
      </Alert>
    );
  }
  return <Alert tone="info">No encontramos una suscripción activa.</Alert>;
}
