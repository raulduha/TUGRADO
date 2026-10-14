"use client";

import { useState } from "react";

import { AppHeader } from "@/components/app-header";
import { Apruvi } from "@/components/apruvi";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink } from "@/components/button";
import { DemoBanner } from "@/components/demo-banner";
import { Icon } from "@/components/illustrations";
import { useStudyAccess } from "@/lib/use-access";

// Datos de EJEMPLO (FR-019, FR-020). La prioridad usa la regla decidida: peso de la materia en
// el programa × brecha de desempeño reciente. Los pesos y materias reales llegan con el cedulario.
const SUBJECTS = [
  { name: "Derecho Civil", weight: 0.35, gap: 0.4 },
  { name: "Derecho Procesal", weight: 0.3, gap: 0.55 },
  { name: "Derecho Constitucional", weight: 0.2, gap: 0.2 },
  { name: "Derecho Penal", weight: 0.15, gap: 0.35 },
].map((s) => ({ ...s, priority: s.weight * s.gap }));

type TaskState = "done" | "pending" | "late";
const TASKS: Array<{ day: string; title: string; minutes: number; state: TaskState }> = [
  { day: "Lun", title: "Práctica: Obligaciones (10 preguntas)", minutes: 30, state: "done" },
  { day: "Mar", title: "Simulación oral: Procesal civil", minutes: 25, state: "done" },
  { day: "Mié", title: "Repaso: Recursos procesales", minutes: 45, state: "late" },
  { day: "Jue", title: "Práctica: Garantías constitucionales", minutes: 30, state: "pending" },
  { day: "Vie", title: "Simulación oral: Acto jurídico", minutes: 25, state: "pending" },
  { day: "Sáb", title: "Práctica mixta (20 preguntas)", minutes: 40, state: "pending" },
];

const STATE_LABEL: Record<TaskState, { text: string; className: string }> = {
  done: { text: "Completada", className: "bg-success/10 text-success" },
  pending: { text: "Pendiente", className: "bg-brand-soft text-brand-strong" },
  late: { text: "Atrasada", className: "bg-danger/10 text-danger" },
};

export default function StudyPlanPage() {
  const { me, setMe, hasAccess } = useStudyAccess("/plan");
  const [showOriginal, setShowOriginal] = useState(false);
  const maxPriority = Math.max(...SUBJECTS.map((s) => s.priority));
  const sorted = [...SUBJECTS].sort((a, b) => b.priority - a.priority);

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-4xl flex-1 space-y-6 px-4 pb-16 pt-6">
        {!me || !hasAccess ? (
          <ApruviLoader label="Armando tu plan…" />
        ) : (
          <>
            <DemoBanner>Tu plan real se arma con tu fecha de examen, tu disponibilidad y tu avance.</DemoBanner>

            <section className="flex flex-col gap-5 rounded-3xl bg-gradient-to-br from-brand-soft to-accent-soft p-6 sm:flex-row sm:items-center sm:justify-between sm:p-8">
              <div className="flex items-center gap-4">
                <Apruvi className="h-20 w-20 flex-none" />
                <div>
                  <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Tu plan de estudio</h1>
                  <p className="text-muted">Examen: 15 de marzo de 2027 · 10 horas por semana</p>
                </div>
              </div>
              <dl className="grid grid-cols-3 gap-3 text-center">
                {[
                  ["18 %", "Cobertura"],
                  ["2/6", "Esta semana"],
                  ["1", "Atrasada"],
                ].map(([value, label]) => (
                  <div key={label} className="rounded-2xl bg-surface px-3 py-2">
                    <dt className="text-xs text-muted">{label}</dt>
                    <dd className="text-xl font-semibold">{value}</dd>
                  </div>
                ))}
              </dl>
            </section>

            <div className="grid gap-6 lg:grid-cols-[3fr_2fr]">
              <section className="rounded-3xl border border-line bg-surface p-6">
                <h2 className="text-lg font-semibold">Esta semana</h2>
                <ul className="mt-4 space-y-2">
                  {TASKS.map((task) => (
                    <li key={task.title} className="flex items-center gap-3 rounded-2xl border border-line p-3">
                      <span className="w-10 flex-none text-sm font-semibold text-muted">{task.day}</span>
                      <span
                        className={`flex h-7 w-7 flex-none items-center justify-center rounded-full ${
                          task.state === "done" ? "bg-success text-white" : "border-2 border-line"
                        }`}
                      >
                        {task.state === "done" ? <Icon name="check" className="h-4 w-4" /> : null}
                      </span>
                      <span className="min-w-0 flex-1 text-sm font-medium">
                        {task.title}
                        <span className="block text-xs text-muted">{task.minutes} min</span>
                      </span>
                      <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${STATE_LABEL[task.state].className}`}>
                        {STATE_LABEL[task.state].text}
                      </span>
                    </li>
                  ))}
                </ul>
              </section>

              <section className="rounded-3xl border border-line bg-surface p-6">
                <h2 className="text-lg font-semibold">Dónde poner foco</h2>
                <p className="mt-1 text-xs text-muted">Prioridad = peso en el programa × brecha reciente.</p>
                <ul className="mt-4 space-y-4">
                  {sorted.map((s) => (
                    <li key={s.name}>
                      <div className="flex justify-between text-sm font-medium">
                        <span>{s.name}</span>
                        <span className="text-muted">
                          {Math.round(s.weight * 100)} % × {Math.round(s.gap * 100)} %
                        </span>
                      </div>
                      <div className="mt-1.5 h-2.5 overflow-hidden rounded-full bg-line">
                        <div className="h-full rounded-full bg-accent" style={{ width: `${(s.priority / maxPriority) * 100}%` }} />
                      </div>
                    </li>
                  ))}
                </ul>
              </section>
            </div>

            <section className="rounded-3xl border border-line bg-surface p-6">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-lg font-semibold">Ajuste del 13 de octubre</h2>
                  <p className="text-sm text-muted">
                    +1 sesión de Derecho Procesal: en tus últimas prácticas acertaste 45 % en recursos.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setShowOriginal((v) => !v)}
                  aria-expanded={showOriginal}
                  className="text-sm font-semibold text-brand hover:underline"
                >
                  {showOriginal ? "Ocultar plan original" : "Ver plan original"}
                </button>
              </div>
              {showOriginal ? (
                <p className="pop-in mt-3 rounded-2xl bg-background p-4 text-sm">
                  Plan original (2 de octubre): 3 sesiones de Civil, 2 de Procesal y 1 de
                  Constitucional por semana. Se conserva siempre como línea base.
                </p>
              ) : null}
            </section>

            <ButtonLink href="/panel" variant="secondary" className="w-full sm:w-auto">
              Volver al mapa
            </ButtonLink>
          </>
        )}
      </main>
    </div>
  );
}
