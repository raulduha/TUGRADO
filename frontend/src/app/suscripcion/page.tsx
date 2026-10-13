"use client";

import { useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { ButtonLink, buttonStyles } from "@/components/button";
import { Field } from "@/components/field";
import { Icon } from "@/components/illustrations";
import { api, formatClp, formatDate, type Subscription } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

const BENEFITS = [
  "Práctica con preguntas revisadas y su explicación",
  "Simulación del examen oral con tiempos reales",
  "Plan de estudio que se ajusta a tu avance",
];

export default function SubscriptionPage() {
  const { me, setMe, error: userError } = useRequireUser("/suscripcion");
  const [sub, setSub] = useState<Subscription | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [confirmCancel, setConfirmCancel] = useState(false);

  useEffect(() => {
    if (!me) return;
    let cancelled = false;
    (async () => {
      let result = await api<Subscription>("/billing/subscription");
      // Con un pago pendiente se consulta a Mercado Pago: así se activa aunque el aviso
      // (webhook) no haya llegado o el estudiante no haya vuelto desde la página de pago.
      if (result.ok && result.data.status === "pending") {
        const synced = await api<Subscription>("/billing/subscription/sync", { method: "POST" });
        if (synced.ok) result = synced;
      }
      if (cancelled) return;
      if (result.ok) setSub(result.data);
      else if (result.status !== 401) setError(result.error.message);
    })();
    return () => {
      cancelled = true;
    };
  }, [me]);

  async function subscribe(payerEmail: string) {
    setBusy(true);
    setError(null);
    const result = await api<{ checkout_url: string }>("/billing/subscription", {
      body: { payer_email: payerEmail },
    });
    if (result.ok) {
      // El pago ocurre en la página de Mercado Pago (o en el simulador en desarrollo).
      window.location.assign(result.data.checkout_url);
      return;
    }
    setError(result.error.message);
    setBusy(false);
  }

  async function cancel() {
    setBusy(true);
    setError(null);
    const result = await api<Subscription>("/billing/subscription/cancel", { method: "POST" });
    if (result.ok) setSub(result.data);
    else setError(result.error.message);
    setConfirmCancel(false);
    setBusy(false);
  }

  const failure = userError ?? error;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-8">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Tu suscripción</h1>
        {failure ? (
          <div className="mt-6">
            <Alert tone="error">{failure}</Alert>
          </div>
        ) : null}

        {!sub ? (
          <p role="status" className="mt-6 text-muted">
            Cargando…
          </p>
        ) : (
          <section className="mt-6 overflow-hidden rounded-3xl border border-line bg-surface">
            <div className="bg-gradient-to-br from-brand-soft to-accent-soft p-6 sm:p-8">
              <p className="text-sm font-semibold text-brand">Plan mensual</p>
              <p className="mt-2 text-4xl font-semibold tracking-tight">
                {formatClp(sub.amount_clp)}
                <span className="text-base font-medium text-muted"> / mes</span>
              </p>
              {sub.trial_days > 0 ? (
                <p className="mt-1 text-sm text-muted">
                  Los primeros {sub.trial_days} días son gratis. Cancela cuando quieras.
                </p>
              ) : null}
            </div>
            <div className="space-y-6 p-6 sm:p-8">
              <ul className="space-y-3">
                {BENEFITS.map((benefit) => (
                  <li key={benefit} className="flex items-start gap-3">
                    <span className="mt-0.5 flex h-5 w-5 flex-none items-center justify-center rounded-full bg-success text-white">
                      <Icon name="check" className="h-3.5 w-3.5" />
                    </span>
                    {benefit}
                  </li>
                ))}
              </ul>
              <StatusPanel
                sub={sub}
                defaultEmail={sub.payer_email ?? me?.email ?? ""}
                busy={busy}
                confirmCancel={confirmCancel}
                onSubscribe={subscribe}
                onAskCancel={() => setConfirmCancel(true)}
                onKeep={() => setConfirmCancel(false)}
                onCancel={cancel}
              />
              <p className="text-xs text-muted">
                El pago se procesa en Mercado Pago: no recibimos ni guardamos los datos de tu
                tarjeta. Las evaluaciones son orientativas y no garantizan la aprobación del examen.
              </p>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

function StatusPanel({
  sub,
  defaultEmail,
  busy,
  confirmCancel,
  onSubscribe,
  onAskCancel,
  onKeep,
  onCancel,
}: {
  sub: Subscription;
  defaultEmail: string;
  busy: boolean;
  confirmCancel: boolean;
  onSubscribe: (payerEmail: string) => void;
  onAskCancel: () => void;
  onKeep: () => void;
  onCancel: () => void;
}) {
  if (sub.status === "authorized") {
    return (
      <div className="space-y-4">
        <Alert tone="success">
          <p className="font-medium">Tu suscripción está activa.</p>
          {sub.next_payment_date ? (
            <p className="mt-1">Próximo cobro: {formatDate(sub.next_payment_date)}.</p>
          ) : null}
        </Alert>
        {confirmCancel ? (
          <div className="space-y-3 rounded-2xl border border-line p-4">
            <p className="font-medium">¿Cancelar tu suscripción?</p>
            <p className="text-sm text-muted">
              Dejarás de tener acceso a las funciones de estudio. Puedes volver a suscribirte
              cuando quieras.
            </p>
            <div className="flex flex-col gap-2 sm:flex-row">
              <button type="button" onClick={onKeep} className={buttonStyles.primary}>
                Mantener suscripción
              </button>
              <button
                type="button"
                onClick={onCancel}
                disabled={busy}
                className={`${buttonStyles.secondary} text-danger`}
              >
                {busy ? "Cancelando…" : "Sí, cancelar"}
              </button>
            </div>
          </div>
        ) : (
          <button type="button" onClick={onAskCancel} className="text-sm font-medium text-danger hover:underline">
            Cancelar suscripción
          </button>
        )}
      </div>
    );
  }

  if (sub.status === "pending") {
    return (
      <div className="space-y-3">
        <Alert tone="info">Tu suscripción está esperando que completes el pago en Mercado Pago.</Alert>
        <PayForm defaultEmail={defaultEmail} busy={busy} label="Ir a pagar en Mercado Pago" onSubmit={onSubscribe} />
        <a href="/suscripcion/retorno" className={`w-full ${buttonStyles.secondary}`}>
          Ya pagué: actualizar estado
        </a>
      </div>
    );
  }

  if (sub.status === "paused") {
    return (
      <Alert tone="info">
        Tu suscripción está en pausa en Mercado Pago. Revisa tu medio de pago allí para
        reactivarla.
      </Alert>
    );
  }

  return (
    <div className="space-y-3">
      {sub.has_access ? (
        <>
          <Alert tone="info">
            Tu cuenta ya tiene acceso sin suscripción (administrador o cuenta autorizada por el
            equipo).
          </Alert>
          <ButtonLink href="/panel" className="w-full">
            Ir a mi panel
          </ButtonLink>
        </>
      ) : (
        <p className="text-sm text-muted">
          Para empezar a estudiar, activa tu prueba gratis. Mercado Pago te pedirá un medio de
          pago; puedes cancelar desde aquí antes de que termine la prueba.
        </p>
      )}
      {sub.has_access ? null : (
        <PayForm
          defaultEmail={defaultEmail}
          busy={busy}
          label={sub.trial_days > 0 ? `Comenzar ${sub.trial_days} días gratis` : "Suscribirme"}
          onSubmit={onSubscribe}
        />
      )}
    </div>
  );
}

/** Mercado Pago exige que el correo coincida con la cuenta con la que se paga: puede ser
 * distinto del correo de la app. */
function PayForm({
  defaultEmail,
  busy,
  label,
  onSubmit,
}: {
  defaultEmail: string;
  busy: boolean;
  label: string;
  onSubmit: (payerEmail: string) => void;
}) {
  return (
    <form
      className="space-y-3"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit(String(new FormData(event.currentTarget).get("payer_email") ?? "").trim());
      }}
    >
      <Field
        label="Correo de tu cuenta de Mercado Pago"
        name="payer_email"
        type="email"
        autoComplete="email"
        defaultValue={defaultEmail}
        hint="Debe ser el correo con el que inicias sesión en Mercado Pago."
      />
      <button type="submit" disabled={busy} className={`w-full ${buttonStyles.primary}`}>
        {busy ? "Redirigiendo a Mercado Pago…" : label}
      </button>
    </form>
  );
}
