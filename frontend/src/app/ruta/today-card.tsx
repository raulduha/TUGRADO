"use client";

import { useState } from "react";

import { Alert } from "@/components/alert";
import { ButtonLink, buttonStyles } from "@/components/button";
import { Icon } from "@/components/illustrations";
import { api, formatDate, type StudyToday } from "@/lib/api";

const GOALS = [10, 20, 30];
// Sin meta elegida ni fecha de examen, la meta del día es esta.
const DEFAULT_GOAL = 10;

/** Hoy en Chile como AAAA-MM-DD (el backend cuenta los días en esa zona). */
function chileToday(): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "America/Santiago" }).format(new Date());
}

/** El plan del día (FR-035): cuenta regresiva al examen, meta diaria y qué hacer primero
 * (repasar los errores que tocan hoy y luego seguir la ruta). Todo lo calcula el backend. */
export function TodayCard({
  today,
  nextLessonHref,
  onSaved,
}: {
  today: StudyToday;
  nextLessonHref: string | null;
  onSaved: (today: StudyToday) => void;
}) {
  const configured = today.exam_date !== null || today.daily_goal !== null;
  const [editing, setEditing] = useState(false);

  if (!configured || editing) {
    return (
      <PlanForm
        today={today}
        onCancel={configured ? () => setEditing(false) : null}
        onSaved={(updated) => {
          setEditing(false);
          onSaved(updated);
        }}
      />
    );
  }

  const goal = today.daily_goal ?? today.suggested_goal ?? DEFAULT_GOAL;
  const progress = Math.min(today.answered_today / goal, 1);
  const reached = today.answered_today >= goal;

  return (
    <section aria-label="Tu plan de hoy" className="rounded-3xl border border-line bg-surface p-5">
      <div className="flex items-center gap-4">
        <GoalRing progress={progress} label={`${today.answered_today} de ${goal} preguntas hoy`}>
          <span className="text-lg font-bold leading-none">{today.answered_today}</span>
          <span className="text-xs text-muted">de {goal}</span>
        </GoalRing>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-semibold uppercase tracking-wide text-brand">Hoy</p>
          <p className="font-semibold leading-snug">
            {reached ? "¡Meta del día cumplida!" : `Responde ${goal - today.answered_today} preguntas más`}
          </p>
          {today.exam_date && today.days_left !== null ? (
            <p className="text-sm text-muted">
              {today.days_left === 0
                ? "Tu examen es hoy. ¡Éxito!"
                : `Faltan ${today.days_left} ${today.days_left === 1 ? "día" : "días"} para tu examen (${formatDate(`${today.exam_date}T12:00:00`)}).`}
            </p>
          ) : (
            <p className="text-sm text-muted">Agrega la fecha de tu examen para ver la cuenta regresiva.</p>
          )}
        </div>
        <button
          type="button"
          onClick={() => setEditing(true)}
          className="self-start text-sm font-semibold text-brand hover:underline"
        >
          Cambiar
        </button>
      </div>

      <div className="mt-4 flex flex-col gap-2 sm:flex-row">
        {today.review_due > 0 ? (
          <ButtonLink href="/practica?repaso=1" className="flex-1">
            {`Repasar ${today.review_due} ${today.review_due === 1 ? "error" : "errores"}`}
          </ButtonLink>
        ) : null}
        {nextLessonHref ? (
          <ButtonLink
            href={nextLessonHref}
            variant={today.review_due > 0 ? "secondary" : "primary"}
            className="flex-1"
          >
            Seguir mi ruta
          </ButtonLink>
        ) : null}
      </div>
      {today.review_due > 0 ? (
        <p className="mt-2 text-xs text-muted">
          Las preguntas que fallaste vuelven al día siguiente, y luego a los 3, 7 y 14 días.
        </p>
      ) : null}
    </section>
  );
}

function PlanForm({
  today,
  onCancel,
  onSaved,
}: {
  today: StudyToday;
  onCancel: (() => void) | null;
  onSaved: (today: StudyToday) => void;
}) {
  const [examDate, setExamDate] = useState(today.exam_date ?? "");
  // null = que la app calcule la meta con la fecha del examen.
  const [goal, setGoal] = useState<number | null>(today.daily_goal ?? (today.exam_date ? null : DEFAULT_GOAL));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const min = chileToday();

  async function save(event: React.FormEvent) {
    event.preventDefault();
    setSaving(true);
    setError(null);
    const saved = await api("/study/profile", {
      method: "PUT",
      body: { exam_date: examDate || null, daily_goal: goal },
    });
    if (!saved.ok) {
      setSaving(false);
      setError(saved.error.message);
      return;
    }
    const updated = await api<StudyToday>("/study/today");
    setSaving(false);
    if (updated.ok) onSaved(updated.data);
    else setError(updated.error.message);
  }

  return (
    <form onSubmit={save} aria-label="Tu plan de estudio" className="space-y-4 rounded-3xl border border-line bg-surface p-5">
      <div className="flex items-start gap-3">
        <span className="flex h-10 w-10 flex-none items-center justify-center rounded-full bg-brand-soft text-brand">
          <Icon name="calendar" />
        </span>
        <div>
          <h2 className="font-semibold">Arma tu plan diario</h2>
          <p className="text-sm text-muted">Con la fecha de tu examen calculamos cuánto estudiar cada día.</p>
        </div>
      </div>

      {error ? <Alert tone="error">{error}</Alert> : null}

      <label className="block">
        <span className="text-sm font-semibold">¿Cuándo das el examen?</span>
        <input
          type="date"
          min={min}
          value={examDate}
          onChange={(e) => {
            setExamDate(e.target.value);
            if (!e.target.value && goal === null) setGoal(DEFAULT_GOAL);
          }}
          className="mt-1 block w-full rounded-xl border border-line bg-surface px-3 py-2"
        />
        <span className="text-xs text-muted">Si aún no lo sabes, déjalo en blanco y elige una meta.</span>
      </label>

      <fieldset>
        <legend className="text-sm font-semibold">Preguntas por día</legend>
        <div className="mt-1 flex flex-wrap gap-2">
          {examDate ? (
            <GoalChip selected={goal === null} onClick={() => setGoal(null)}>
              Calcúlala por mí
            </GoalChip>
          ) : null}
          {GOALS.map((value) => (
            <GoalChip key={value} selected={goal === value} onClick={() => setGoal(value)}>
              {String(value)}
            </GoalChip>
          ))}
        </div>
      </fieldset>

      <div className="flex flex-col gap-2 sm:flex-row">
        <button type="submit" disabled={saving} className={`flex-1 ${buttonStyles.primary}`}>
          {saving ? "Guardando…" : "Guardar mi plan"}
        </button>
        {onCancel ? (
          <button type="button" onClick={onCancel} className={`flex-1 ${buttonStyles.secondary}`}>
            Cancelar
          </button>
        ) : null}
      </div>
    </form>
  );
}

function GoalChip({
  selected,
  onClick,
  children,
}: {
  selected: boolean;
  onClick: () => void;
  children: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={selected}
      className={`rounded-xl border-2 px-4 py-2 text-sm font-semibold transition ${
        selected ? "border-brand bg-brand-soft text-brand" : "border-line bg-surface hover:border-brand/50"
      }`}
    >
      {children}
    </button>
  );
}

function GoalRing({
  progress,
  label,
  children,
}: {
  progress: number;
  label: string;
  children: React.ReactNode;
}) {
  const radius = 26;
  const length = 2 * Math.PI * radius;
  return (
    <div className="relative h-16 w-16 flex-none" role="img" aria-label={label}>
      <svg viewBox="0 0 64 64" className="h-16 w-16 -rotate-90" aria-hidden="true">
        <circle cx="32" cy="32" r={radius} fill="none" strokeWidth="7" className="stroke-line" />
        <circle
          cx="32"
          cy="32"
          r={radius}
          fill="none"
          strokeWidth="7"
          strokeLinecap="round"
          strokeDasharray={length}
          strokeDashoffset={length * (1 - progress)}
          className={`transition-all duration-700 ${progress >= 1 ? "stroke-success" : "stroke-accent"}`}
        />
      </svg>
      <div aria-hidden="true" className="absolute inset-0 flex flex-col items-center justify-center">
        {children}
      </div>
    </div>
  );
}
