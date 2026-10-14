"use client";

import Link from "next/link";
import { useState } from "react";

import { Apruvi } from "@/components/apruvi";
import { Icon, type IconName } from "@/components/illustrations";

export type Level = {
  icon: IconName;
  title: string;
  /** Lo que dice Apruvi al elegir el nivel. */
  says: string;
  done: boolean;
  /** Pantalla de vista previa (mockup con datos de ejemplo) mientras no exista la real. */
  preview?: string;
};

// Recorrido real del estudiante según las specs (FR-003 a FR-020). Solo se marca como hecho lo
// que la app ya permite; el resto aparece como "Próximamente", nunca con avance inventado.
export const LEVELS: Level[] = [
  {
    icon: "user",
    title: "Tu cuenta",
    says: "¡Hola! Soy Apruvi. Tu cuenta ya está lista; desde aquí te acompaño nivel a nivel.",
    done: true,
  },
  {
    icon: "list",
    title: "Elige tus materias",
    says: "Aquí elegirás tu programa y las materias que entran en tu examen. ¡Muy pronto!",
    done: false,
  },
  {
    icon: "calendar",
    title: "Arma tu plan",
    says: "Armaremos un plan hasta la fecha de tu examen, según el tiempo que tengas cada semana.",
    done: false,
    preview: "/plan",
  },
  {
    icon: "book",
    title: "Practica con alternativas",
    says: "Responderás preguntas de alternativas. Si te equivocas, verás la explicación.",
    done: false,
    preview: "/practica",
  },
  {
    icon: "mic",
    title: "Tu primera simulación oral",
    says: "Respira hondo: responderás en voz alta, como en el examen, y verás una evaluación orientativa.",
    done: false,
    preview: "/simulacion",
  },
  {
    icon: "repeat",
    title: "Refuerza lo que más te cuesta",
    says: "Volveremos a lo que más te cuesta. Así se avanza: paso a paso.",
    done: false,
  },
  {
    icon: "clock",
    title: "Simulacro del examen",
    says: "Un simulacro con todas tus materias y los tiempos reales del examen.",
    done: false,
  },
  {
    icon: "cap",
    title: "Examen de grado",
    says: "El gran día. Llegarás con todo lo que practicaste, y yo voy a estar apoyándote.",
    done: false,
  },
];

// Camino serpenteante: posición horizontal de cada nivel (en % del ancho) y alto de cada fila.
const X = [50, 68, 74, 62, 38, 26, 34, 56];
const ROW = 112;
const TOP = 56;

export function StudyMap({ levels = LEVELS }: { levels?: Level[] }) {
  const current = Math.max(
    0,
    levels.findIndex((level) => !level.done),
  );
  const [selected, setSelected] = useState(current);
  const points = levels.map((_, i) => ({ x: X[i % X.length], y: TOP + i * ROW }));
  const height = TOP * 2 + (levels.length - 1) * ROW;
  // Curva suave entre niveles (en unidades del viewBox: ancho 100, alto en px).
  const path = curve(points);
  const donePath = curve(points.slice(0, current + 1));
  const apruvi = points[current];
  // Del lado contrario a la etiqueta del nivel (las etiquetas van hacia el centro).
  const apruviOnRight = apruvi.x >= 50;

  return (
    <div className="overflow-hidden rounded-3xl border border-line bg-gradient-to-b from-brand-soft via-surface to-accent-soft">
      <div className="relative mx-auto w-full max-w-md" style={{ height }}>
        {/* Paisaje: nubes y colinas suaves. */}
        <svg className="absolute inset-0 h-full w-full" viewBox={`0 0 100 ${height}`} preserveAspectRatio="none" aria-hidden="true">
          <ellipse cx="12" cy="90" rx="9" ry="14" fill="#ffffff" opacity=".8" />
          <ellipse cx="20" cy="96" rx="8" ry="11" fill="#ffffff" opacity=".8" />
          <ellipse cx="88" cy="330" rx="9" ry="13" fill="#ffffff" opacity=".7" />
          <ellipse cx="80" cy="338" rx="7" ry="10" fill="#ffffff" opacity=".7" />
          <ellipse cx="10" cy={height - 40} rx="40" ry="60" fill="var(--success)" opacity=".08" />
          <ellipse cx="95" cy={height - 20} rx="35" ry="50" fill="var(--accent)" opacity=".12" />
          {/* Camino completo y tramo recorrido. */}
          <path d={path} fill="none" stroke="var(--line)" strokeWidth="14" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
          <path d={path} fill="none" stroke="#ffffff" strokeWidth="4" strokeDasharray="2 10" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
          <path
            d={donePath}
            fill="none"
            stroke="var(--success)"
            strokeWidth="14"
            strokeLinecap="round"
            vectorEffect="non-scaling-stroke"
            opacity=".55"
          />
        </svg>

        <ol aria-label="Niveles">
          {levels.map((level, i) => {
            const p = points[i];
            const state = level.done ? "done" : i === current ? "current" : "locked";
            const labelRight = p.x < 50;
            return (
              <li
                key={level.title}
                className="absolute"
                style={{ left: `${p.x}%`, top: p.y, transform: "translate(-50%, -50%)" }}
              >
                <button
                  type="button"
                  onClick={() => setSelected(i)}
                  aria-pressed={selected === i}
                  aria-label={`Nivel ${i + 1}: ${level.title}. ${
                    state === "done" ? "Completado" : state === "current" ? "Siguiente" : "Próximamente"
                  }`}
                  className={`relative flex h-16 w-16 items-center justify-center rounded-full border-b-[6px] transition focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand ${
                    state === "done"
                      ? "border-[#05603a] bg-success text-white"
                      : state === "current"
                        ? "border-brand-strong bg-brand text-on-brand ring-8 ring-brand/15"
                        : "border-[#d6cfc2] bg-[#ece7de] text-muted"
                  } ${selected === i ? "scale-110" : "hover:scale-105"}`}
                >
                  <Icon name={state === "done" ? "check" : state === "locked" ? "lock" : level.icon} className="h-7 w-7" />
                </button>
                <p
                  className={`pointer-events-none absolute top-1/2 w-28 -translate-y-1/2 text-xs font-semibold leading-tight sm:w-36 sm:text-sm ${
                    labelRight ? "left-[4.75rem] text-left" : "right-[4.75rem] text-right"
                  } ${state === "locked" ? "text-muted" : "text-foreground"}`}
                >
                  {level.title}
                  <span className="block text-[11px] font-medium text-muted">
                    {state === "done" ? "¡Listo!" : state === "current" ? "Siguiente · Próximamente" : "Próximamente"}
                  </span>
                </p>
              </li>
            );
          })}
        </ol>

        {/* Apruvi se para junto al nivel en curso y comenta el nivel elegido. */}
        <div
          className="pointer-events-none absolute transition-all duration-700 ease-out"
          style={{
            left: `${apruvi.x}%`,
            top: apruvi.y,
            transform: `translate(${apruviOnRight ? "34px" : "calc(-100% - 34px)"}, -62%)`,
          }}
        >
          <Apruvi className="h-14 w-14" />
        </div>
      </div>

      <div className="border-t border-line bg-surface/90 p-4 sm:p-5" aria-live="polite">
        <div className="flex items-start gap-3">
          <Apruvi className="h-12 w-12 flex-none" />
          <div className="relative rounded-2xl border border-line bg-background px-4 py-3">
            <p className="text-xs font-semibold text-brand">
              Apruvi · Nivel {selected + 1}: {levels[selected].title}
            </p>
            <p className="mt-1 text-sm">{levels[selected].says}</p>
            {levels[selected].preview ? (
              <Link
                href={levels[selected].preview}
                className="mt-2 inline-flex items-center gap-1 text-sm font-semibold text-brand hover:underline"
              >
                Probar (vista previa) →
              </Link>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}

function curve(points: Array<{ x: number; y: number }>): string {
  return points
    .map((p, i) => {
      if (i === 0) return `M ${p.x} ${p.y}`;
      const prev = points[i - 1];
      const midY = (prev.y + p.y) / 2;
      return `C ${prev.x} ${midY}, ${p.x} ${midY}, ${p.x} ${p.y}`;
    })
    .join(" ");
}
