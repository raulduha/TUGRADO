"use client";

import { useEffect, useState } from "react";

import { AppHeader } from "@/components/app-header";
import { ButtonLink } from "@/components/button";
import { FeedbackButton } from "@/components/feedback-button";
import { Icon, type IconName } from "@/components/illustrations";
import { api, formatClp, type Me, type Subscription } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

const ROLE_LABELS: Record<Me["roles"][number], string> = {
  student: "Estudiante",
  administrator: "Administrador",
};

// La ruta refleja el estado real: con sesión iniciada, la cuenta existe y el correo está
// verificado. Los pasos siguientes aún no existen en la app y se marcan como "Próximamente".
const ROUTE: Array<{ icon: IconName; title: string; text: string; done: boolean }> = [
  { icon: "user", title: "Crea tu cuenta", text: "Listo.", done: true },
  { icon: "mail", title: "Verifica tu correo", text: "Listo.", done: true },
  { icon: "list", title: "Elige tu programa y materias", text: "Próximamente", done: false },
  { icon: "book", title: "Responde tu primera práctica", text: "Próximamente", done: false },
  { icon: "mic", title: "Haz tu primera simulación oral", text: "Próximamente", done: false },
  { icon: "calendar", title: "Arma tu plan de estudio", text: "Próximamente", done: false },
];

// Sin datos todavía: se muestra el estado vacío, nunca cifras inventadas.
const STATS: Array<{ icon: IconName; label: string }> = [
  { icon: "book", label: "Preguntas respondidas" },
  { icon: "mic", label: "Simulaciones orales" },
  { icon: "chart", label: "Cobertura del programa" },
  { icon: "flame", label: "Días seguidos estudiando" },
];

export default function PanelPage() {
  const { me, setMe, error } = useRequireUser("/panel");
  const [sub, setSub] = useState<Subscription | null>(null);

  useEffect(() => {
    if (!me) return;
    let cancelled = false;
    api<Subscription>("/billing/subscription").then((result) => {
      if (!cancelled && result.ok) setSub(result.data);
    });
    return () => {
      cancelled = true;
    };
  }, [me]);

  const done = ROUTE.filter((step) => step.done).length;
  const percent = Math.round((done / ROUTE.length) * 100);

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />

      {/* pb-28: espacio para el botón flotante de comentarios. */}
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 pb-28 pt-8">
        {error ? (
          <p role="alert" className="text-danger">
            {error}
          </p>
        ) : !me ? (
          <p role="status" className="text-muted">
            Cargando tu panel…
          </p>
        ) : (
          <div className="space-y-10">
            {sub && !sub.has_access ? <SubscriptionBanner sub={sub} /> : null}
            <section className="flex flex-col gap-6 rounded-3xl bg-gradient-to-br from-brand-soft to-accent-soft p-6 sm:flex-row sm:items-center sm:justify-between sm:p-8">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">¡Hola! Qué bueno verte</h1>
                <p className="mt-2 break-all text-muted">
                  {me.email} · {me.roles.map((role) => ROLE_LABELS[role]).join(", ")}
                </p>
                <p className="mt-4 max-w-md text-pretty">
                  Ya diste los primeros pasos. Muy pronto podrás practicar y simular tu examen
                  desde aquí.
                </p>
              </div>
              <ProgressRing percent={percent} label={`${done} de ${ROUTE.length} pasos`} />
            </section>

            <section aria-labelledby="ruta">
              <h2 id="ruta" className="text-xl font-semibold tracking-tight">
                Tu ruta
              </h2>
              <ol className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {ROUTE.map((step, index) => (
                  <li
                    key={step.title}
                    className={`flex items-center gap-4 rounded-2xl border p-4 ${
                      step.done ? "border-success/30 bg-surface" : "border-line bg-surface/60"
                    }`}
                  >
                    <span
                      className={`flex h-11 w-11 flex-none items-center justify-center rounded-full ${
                        step.done ? "bg-success text-white" : "bg-background text-muted"
                      }`}
                    >
                      <Icon name={step.done ? "check" : step.icon} />
                    </span>
                    <div className="min-w-0">
                      <p className="text-xs font-semibold text-muted">Paso {index + 1}</p>
                      <p className="font-semibold">{step.title}</p>
                      <p className={`text-sm ${step.done ? "text-success" : "text-muted"}`}>
                        {step.text}
                      </p>
                    </div>
                  </li>
                ))}
              </ol>
            </section>

            <section aria-labelledby="progreso">
              <h2 id="progreso" className="text-xl font-semibold tracking-tight">
                Tu progreso
              </h2>
              <ul className="mt-4 grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
                {STATS.map((stat) => (
                  <li key={stat.label} className="rounded-2xl border border-line bg-surface p-4 sm:p-5">
                    <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-soft text-brand">
                      <Icon name={stat.icon} />
                    </span>
                    <p className="mt-4 text-3xl font-semibold" aria-label="Sin datos">
                      —
                    </p>
                    <p className="mt-1 font-medium">{stat.label}</p>
                    <p className="mt-1 text-sm text-muted">Aparecerá cuando empieces a estudiar.</p>
                  </li>
                ))}
              </ul>
            </section>
          </div>
        )}
      </main>

      {me ? <FeedbackButton /> : null}
    </div>
  );
}

function ProgressRing({ percent, label }: { percent: number; label: string }) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  return (
    <div className="flex items-center gap-4 self-start sm:self-auto">
      <svg viewBox="0 0 100 100" className="h-24 w-24 -rotate-90" role="img" aria-label={`Ruta completada al ${percent} %`}>
        <circle cx="50" cy="50" r={radius} fill="none" stroke="var(--surface)" strokeWidth="10" />
        <circle
          cx="50"
          cy="50"
          r={radius}
          fill="none"
          stroke="var(--brand)"
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference * (1 - percent / 100)}
        />
      </svg>
      <div>
        <p className="text-3xl font-semibold">{percent} %</p>
        <p className="text-sm text-muted">{label}</p>
      </div>
    </div>
  );
}

function SubscriptionBanner({ sub }: { sub: Subscription }) {
  const pending = sub.status === "pending";
  return (
    <section className="flex flex-col gap-4 rounded-3xl border border-brand/30 bg-surface p-6 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-start gap-3">
        <span className="flex h-10 w-10 flex-none items-center justify-center rounded-full bg-brand-soft text-brand">
          <Icon name="lock" />
        </span>
        <div>
          <p className="font-semibold">
            {pending ? "Completa tu suscripción" : "Activa tu suscripción para estudiar"}
          </p>
          <p className="mt-1 text-sm text-muted">
            {sub.trial_days > 0 ? `${sub.trial_days} días gratis, luego ` : ""}
            {formatClp(sub.amount_clp)} al mes. Cancela cuando quieras.
          </p>
        </div>
      </div>
      <ButtonLink href="/suscripcion" className="flex-none">
        {pending ? "Ver estado del pago" : "Ver plan"}
      </ButtonLink>
    </section>
  );
}
