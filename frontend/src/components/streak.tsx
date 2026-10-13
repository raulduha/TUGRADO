"use client";

import { Apruvi } from "@/components/apruvi";
import { buttonStyles } from "@/components/button";
import type { Streak } from "@/lib/api";

const WEEKDAYS = ["D", "L", "M", "M", "J", "V", "S"];

export function Flame({ className = "h-10 w-10", lit = true }: { className?: string; lit?: boolean }) {
  return (
    <svg viewBox="0 0 32 40" className={className} aria-hidden="true">
      <path
        className={lit ? "flame-outer" : undefined}
        d="M16 2c1 7 9 10 9 21a9 9 0 0 1-18 0c0-5 3-8 5-11 0 4 2 6 3 6-1-6 0-11 1-16Z"
        fill={lit ? "#f97316" : "#d6cfc2"}
      />
      <path
        className={lit ? "flame-inner" : undefined}
        d="M16 18c1 4 5 6 5 11a5 5 0 0 1-10 0c0-3 2-5 3-7 0 2 1 3 2 3-1-3 0-5 0-7Z"
        fill={lit ? "#fbbf24" : "#ece7de"}
      />
    </svg>
  );
}

/** Racha de días seguidos con la semana marcada (FR-033). */
export function StreakCard({ streak }: { streak: Streak }) {
  const today = new Date().getDay();
  // Letra del día para cada posición de la semana (la última es hoy).
  const labels = streak.week.map((_, i) => WEEKDAYS[(today - (6 - i) + 7) % 7]);
  return (
    <section
      aria-labelledby="racha"
      className="flex flex-col gap-5 rounded-3xl border border-line bg-surface p-6 sm:flex-row sm:items-center sm:justify-between"
    >
      <div className="flex items-center gap-4">
        <Flame className="h-14 w-14 flex-none" lit={streak.current > 0} />
        <div>
          <h2 id="racha" className="text-sm font-semibold text-muted">
            Tu racha
          </h2>
          <p className="text-3xl font-semibold tracking-tight">
            {streak.current} {streak.current === 1 ? "día seguido" : "días seguidos"}
          </p>
          <p className="text-sm text-muted">Mejor racha: {streak.best} {streak.best === 1 ? "día" : "días"}</p>
        </div>
      </div>
      <ol className="flex gap-2" aria-label="Últimos 7 días">
        {streak.week.map((active, i) => (
          <li key={i} className="flex flex-col items-center gap-1">
            <span
              className={`flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold ${
                active ? "bg-[#fff1e6] text-[#c2410c] ring-2 ring-[#f97316]" : "bg-background text-muted"
              }`}
              aria-label={active ? "Con actividad" : "Sin actividad"}
            >
              {active ? <Flame className="h-5 w-5" lit /> : null}
            </span>
            <span className="text-xs text-muted" aria-hidden="true">
              {labels[i]}
            </span>
          </li>
        ))}
      </ol>
    </section>
  );
}

function celebration(current: number): string {
  if (current <= 1) return "¡Empezaste tu racha! Vuelve mañana para que el fueguito siga creciendo.";
  if (current >= 30) return "¡Un mes entero! Esa constancia es lo que más ayuda a preparar el examen.";
  if (current >= 7) return "¡Una semana o más sin parar! Así se avanza: un poquito cada día.";
  return "¡Sigue así! Cada día que estudias suma.";
}

/** Celebración de la primera visita del día, con Apruvi. */
export function StreakCelebration({ streak, onClose }: { streak: Streak; onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-foreground/40 p-4 sm:items-center">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="celebracion"
        className="pop-in w-full max-w-sm rounded-3xl bg-surface p-6 text-center shadow-xl"
      >
        <div className="flex items-end justify-center gap-1">
          <Apruvi className="h-24 w-24" />
          <Flame className="h-16 w-16" />
        </div>
        <h2 id="celebracion" className="mt-3 text-2xl font-semibold tracking-tight">
          {streak.current === 1 ? "¡Racha iniciada!" : `¡${streak.current} días seguidos!`}
        </h2>
        <p className="mt-2 text-muted">{celebration(streak.current)}</p>
        <button type="button" onClick={onClose} className={`mt-5 w-full ${buttonStyles.primary}`} autoFocus>
          ¡Vamos!
        </button>
      </div>
    </div>
  );
}
