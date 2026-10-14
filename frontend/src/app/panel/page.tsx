"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { AppHeader } from "@/components/app-header";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink } from "@/components/button";
import { FeedbackButton } from "@/components/feedback-button";
import { DevSimBanner, DevTools } from "@/components/dev-tools";
import { StreakCard, StreakCelebration } from "@/components/streak";
import { LEVELS, StudyMap } from "@/components/study-map";
import { Icon, type IconName } from "@/components/illustrations";
import { api, formatDate, type Me, type Streak, type Subscription } from "@/lib/api";
import { useDevSim } from "@/lib/devsim";
import { useRequireUser } from "@/lib/use-user";

const ROLE_LABELS: Record<Me["roles"][number], string> = {
  student: "Estudiante",
  administrator: "Administrador",
};

// Sin datos todavía: se muestra el estado vacío, nunca cifras inventadas.
const STATS: Array<{ icon: IconName; label: string }> = [
  { icon: "book", label: "Preguntas respondidas" },
  { icon: "mic", label: "Simulaciones orales" },
  { icon: "chart", label: "Cobertura del programa" },
];

export default function PanelPage() {
  const router = useRouter();
  const { me, setMe, error: userError } = useRequireUser("/panel");
  const [sub, setSub] = useState<Subscription | null>(null);
  const [streak, setStreak] = useState<Streak | null>(null);
  const [celebrate, setCelebrate] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Sin acceso (suscripción, cortesía o administrador) no se entra al panel: primero la prueba
  // gratis. Cada vez que el panel se muestra se consulta de nuevo al backend, que decide.
  useEffect(() => {
    if (!me) return;
    let cancelled = false;
    api<Subscription>("/billing/subscription").then((result) => {
      if (cancelled) return;
      if (!result.ok) {
        if (result.status !== 401) setError(result.error.message);
      } else if (result.data.has_access) {
        setSub(result.data);
        // Marca el día como activo; el backend dice si es la primera visita de hoy.
        api<Streak>("/engagement/checkin", { method: "POST" }).then((checkin) => {
          if (cancelled || !checkin.ok) return;
          setStreak(checkin.data);
          if (checkin.data.new_today) setCelebrate(true);
        });
      } else {
        setSub(null);
        router.replace("/suscripcion");
      }
    });
    return () => {
      cancelled = true;
    };
  }, [me, router]);

  // Herramientas de admin: con la simulación activa, el panel muestra un estudiante ficticio.
  const isAdmin = me?.roles.includes("administrator") ?? false;
  const sim = useDevSim(isAdmin);
  const simDone = Math.round((sim.percent / 100) * LEVELS.length);
  const levels = sim.enabled ? LEVELS.map((l, i) => ({ ...l, done: i < simDone })) : LEVELS;
  const shownStreak: Streak | null = sim.enabled
    ? {
        current: sim.streak,
        best: Math.max(sim.streak, streak?.best ?? 0),
        new_today: false,
        week: Array.from({ length: 7 }, (_, i) => i >= 7 - Math.min(7, sim.streak)),
      }
    : streak;
  const statValues: Array<string | null> = sim.enabled
    ? [String(Math.round(sim.percent * 3.2)), String(Math.round(sim.percent / 8)), `${sim.percent} %`]
    : [null, null, null];

  const done = levels.filter((level) => level.done).length;
  const percent = Math.round((done / levels.length) * 100);

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => {
          setMe(null);
          setSub(null);
          setStreak(null);
          setCelebrate(false);
        }} />

      {/* pb-28: espacio para el botón flotante de comentarios. */}
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 pb-28 pt-8">
        {userError || error ? (
          <p role="alert" className="text-danger">
            {userError ?? error}
          </p>
        ) : !me || !sub ? (
          <ApruviLoader label="Cargando tu panel…" />
        ) : (
          <div className="space-y-10">
            <section className="flex flex-col gap-6 rounded-3xl bg-gradient-to-br from-brand-soft to-accent-soft p-6 sm:flex-row sm:items-center sm:justify-between sm:p-8">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">¡Hola! Qué bueno verte</h1>
                <p className="mt-2 break-all text-muted">
                  {me.email} · {me.roles.map((role) => ROLE_LABELS[role]).join(", ")}
                </p>
                <p className="mt-4 max-w-md text-pretty">
                  {percent >= 100
                    ? "Completaste todo tu mapa de estudio. ¡A darlo todo en el examen!"
                    : percent >= 50
                      ? "Vas por buen camino: ya pasaste la mitad de tu mapa de estudio."
                      : "Ya diste los primeros pasos. Sigue avanzando nivel a nivel."}
                </p>
              </div>
              <ProgressRing percent={percent} label={`${done} de ${levels.length} niveles`} />
            </section>

            <DevSimBanner sim={sim} />
            {shownStreak ? <StreakCard streak={shownStreak} /> : null}

            <section aria-labelledby="mapa">
              <h2 id="mapa" className="text-xl font-semibold tracking-tight">
                Tu mapa de estudio
              </h2>
              <p className="mt-1 text-sm text-muted">
                Toca un nivel para que Apruvi te cuente de qué se trata.
              </p>
              <div className="mt-4">
                <StudyMap key={sim.enabled ? `sim-${simDone}` : "real"} levels={levels} />
              </div>
            </section>

            <SubscriptionCard sub={sub} />

            <section aria-labelledby="progreso">
              <h2 id="progreso" className="text-xl font-semibold tracking-tight">
                Tu progreso
              </h2>
              <ul className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3 sm:gap-4">
                {STATS.map((stat, i) => (
                  <li key={stat.label} className="rounded-2xl border border-line bg-surface p-4 sm:p-5">
                    <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-soft text-brand">
                      <Icon name={stat.icon} />
                    </span>
                    {statValues[i] ? (
                      <p className="mt-4 text-3xl font-semibold">{statValues[i]}</p>
                    ) : (
                      <p className="mt-4 text-3xl font-semibold" aria-label="Sin datos">
                        —
                      </p>
                    )}
                    <p className="mt-1 font-medium">{stat.label}</p>
                    <p className="mt-1 text-sm text-muted">
                      {statValues[i] ? "Dato simulado." : "Aparecerá cuando empieces a estudiar."}
                    </p>
                  </li>
                ))}
              </ul>
            </section>
          </div>
        )}
      </main>

      {me ? <FeedbackButton /> : null}
      {isAdmin ? <DevTools sim={sim} /> : null}
      {celebrate && streak ? (
        <StreakCelebration streak={streak} onClose={() => setCelebrate(false)} />
      ) : null}
    </div>
  );
}

function ProgressRing({ percent, label }: { percent: number; label: string }) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  return (
    <div className="flex items-center gap-4 self-start sm:self-auto">
      <svg viewBox="0 0 100 100" className="h-24 w-24 -rotate-90" role="img" aria-label={`Mapa completado al ${percent} %`}>
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

/** Acceso directo para administrar o cancelar la suscripción desde el panel. */
function SubscriptionCard({ sub }: { sub: Subscription }) {
  const active = sub.status === "authorized";
  return (
    <section
      aria-labelledby="suscripcion"
      className="flex flex-col gap-4 rounded-3xl border border-line bg-surface p-6 sm:flex-row sm:items-center sm:justify-between"
    >
      <div>
        <h2 id="suscripcion" className="text-xl font-semibold tracking-tight">
          Tu suscripción
        </h2>
        <p className="mt-1 text-sm text-muted">
          {active
            ? sub.next_payment_date
              ? `Activa. Próximo cobro: ${formatDate(sub.next_payment_date)}.`
              : "Activa."
            : "Tienes acceso sin suscripción."}
        </p>
      </div>
      {active ? (
        <ButtonLink href="/suscripcion" variant="secondary" className="flex-none">
          Administrar o cancelar
        </ButtonLink>
      ) : null}
    </section>
  );
}
