"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { Apruvi } from "@/components/apruvi";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink } from "@/components/button";
import { Icon } from "@/components/illustrations";
import { api, type LessonSummary, type StudyPath, type StudyToday } from "@/lib/api";
import { useStudyAccess } from "@/lib/use-access";

import { TodayCard } from "./today-card";

// Zigzag del camino: posición horizontal (en % del ancho) de cada lección y alto de cada fila.
const X = [50, 68, 76, 64, 42, 26, 22, 34];
const ROW = 104;
const TOP = 52;
const BUBBLE_SPACE = 200;

type State = "done" | "current" | "open" | "locked";

const PRACTICE = [
  { href: "/practica", label: "Pregunta aleatoria", icon: "target" },
  { href: "/prueba", label: "Prueba cronometrada", icon: "clock" },
  { href: "/flashcards", label: "Flashcards", icon: "repeat" },
] as const;

/** Dentro de una unidad, cada lección se abre al completar la anterior (como en Duolingo). */
function states(lessons: LessonSummary[]): State[] {
  let currentSet = false;
  return lessons.map((lesson, i) => {
    if (lesson.completed) return "done";
    const unlocked = i === 0 || lessons[i - 1].completed;
    if (!unlocked) return "locked";
    if (!currentSet) {
      currentSet = true;
      return "current";
    }
    return "open";
  });
}

/** Ruta de estudio (FR-006): unidades por materia y lecciones cortas por subtema, sobre las
 * preguntas publicadas. El avance lo calcula el backend con las respuestas del estudiante. */
export default function StudyPathPage() {
  const { me, setMe, hasAccess } = useStudyAccess("/ruta");
  const isAdmin = me?.roles.includes("administrator") ?? false;
  const [path, setPath] = useState<StudyPath | null>(null);
  const [today, setToday] = useState<StudyToday | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Se vuelve a pedir cada vez que la página se muestra (también al volver de una lección).
  useEffect(() => {
    if (!hasAccess) return;
    let cancelled = false;
    Promise.all([api<StudyPath>("/practice/path"), api<StudyToday>("/study/today")]).then(
      ([pathResult, todayResult]) => {
        if (cancelled) return;
        if (pathResult.ok) setPath(pathResult.data);
        else setError(pathResult.error.message);
        if (todayResult.ok) setToday(todayResult.data);
      },
    );
    return () => {
      cancelled = true;
    };
  }, [hasAccess]);

  const lessons = path?.units.flatMap((u) => u.lessons) ?? [];
  const completed = lessons.filter((l) => l.completed).length;
  // Apruvi acompaña a la primera unidad que tiene lecciones pendientes.
  const activeUnit = path?.units.findIndex((u) => u.lessons.some((l) => !l.completed)) ?? -1;
  // La siguiente lección es la primera sin completar de esa unidad (siempre está abierta).
  const nextLesson = path?.units[activeUnit]?.lessons.find((l) => !l.completed) ?? null;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-2xl flex-1 space-y-6 px-4 pb-16 pt-6">
        {error ? <Alert tone="error">{error}</Alert> : null}
        {!path ? (
          error ? null : <ApruviLoader label="Armando tu ruta…" />
        ) : (
          <>
            <div className="flex flex-wrap items-end justify-between gap-3">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Tu ruta de estudio</h1>
                <p className="text-muted">Lecciones cortas, tema por tema, siguiendo el temario del examen.</p>
              </div>
              <Link href="/temario" className="text-sm font-semibold text-brand hover:underline">
                Qué entra en el examen →
              </Link>
            </div>

            {today && path.units.length > 0 ? (
              <TodayCard
                today={today}
                nextLessonHref={nextLesson ? `/practica?leccion=${encodeURIComponent(nextLesson.id)}` : null}
                onSaved={setToday}
              />
            ) : null}

            <dl className="grid grid-cols-2 gap-3" aria-label="Tu avance">
              <div className="rounded-2xl border border-line bg-surface p-4">
                <dt className="text-sm text-muted">Experiencia</dt>
                <dd className="text-2xl font-bold text-accent">
                  {path.xp} <span className="text-base font-semibold">XP</span>
                </dd>
              </div>
              <div className="rounded-2xl border border-line bg-surface p-4">
                <dt className="text-sm text-muted">Lecciones completadas</dt>
                <dd className="text-2xl font-bold">
                  {completed}
                  <span className="text-base font-semibold text-muted"> de {lessons.length}</span>
                </dd>
              </div>
            </dl>

            {path.units.length > 0 ? (
              <nav aria-label="Practicar" className="grid grid-cols-3 gap-3">
                {PRACTICE.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className="flex flex-col items-center gap-1.5 rounded-2xl border border-line bg-surface p-3 text-center transition hover:border-brand"
                  >
                    <Icon name={item.icon} className="h-6 w-6 text-brand" />
                    <span className="text-sm font-semibold leading-tight">{item.label}</span>
                  </Link>
                ))}
              </nav>
            ) : null}

            {path.units.length === 0 ? (
              <section className="rounded-3xl border border-dashed border-line p-8 text-center">
                <Apruvi className="mx-auto h-24 w-24" />
                <p className="mt-3 font-semibold">Todavía no hay lecciones publicadas.</p>
                <p className="text-sm text-muted">
                  Mientras tanto, revisa qué entra en el examen en la{" "}
                  <Link href="/temario" className="font-semibold text-brand hover:underline">
                    guía del temario
                  </Link>
                  .
                </p>
              </section>
            ) : (
              path.units.map((unit, i) => (
                <UnitPath
                  key={unit.subject}
                  number={i + 1}
                  subject={unit.subject}
                  lessons={unit.lessons}
                  mastered={unit.mastered}
                  total={unit.total}
                  withApruvi={i === activeUnit}
                  isAdmin={isAdmin}
                />
              ))
            )}
          </>
        )}
      </main>
    </div>
  );
}

function UnitPath({
  number,
  subject,
  lessons,
  mastered,
  total,
  withApruvi,
  isAdmin,
}: {
  number: number;
  subject: string;
  lessons: LessonSummary[];
  mastered: number;
  total: number;
  withApruvi: boolean;
  isAdmin: boolean;
}) {
  const lessonStates = states(lessons);
  const current = lessonStates.indexOf("current");
  const [selected, setSelected] = useState<number | null>(null);
  const done = lessonStates.filter((s) => s === "done").length;
  const points = lessons.map((_, i) => ({ x: X[i % X.length], y: TOP + i * ROW }));
  // Espacio extra abajo para la burbuja de la última lección.
  const height = TOP * 2 + Math.max(0, lessons.length - 1) * ROW + BUBBLE_SPACE;
  // Sin elección, la burbuja se abre en la lección siguiente; -1 = cerrada.
  const picked = selected ?? (current >= 0 ? current : -1);
  const chosen = picked >= 0 ? picked : null;

  return (
    <section aria-label={`Unidad ${number}: ${subject}`} className="overflow-hidden rounded-3xl border border-line bg-surface">
      <header className="bg-brand px-5 py-4 text-on-brand">
        <p className="text-xs font-semibold uppercase tracking-wide opacity-80">Unidad {number}</p>
        <div className="flex flex-wrap items-baseline justify-between gap-x-3">
          <h2 className="text-xl font-semibold">{subject}</h2>
          <p className="text-sm font-semibold" title="Preguntas de esta cédula que acertaste en tu último intento">
            Preparación {total ? Math.round((mastered / total) * 100) : 0} %
          </p>
        </div>
        <div className="mt-2 flex items-center gap-3">
          <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-white/25">
            <div
              className="h-full rounded-full bg-accent transition-all duration-500"
              style={{ width: `${lessons.length ? (done / lessons.length) * 100 : 0}%` }}
            />
          </div>
          <span className="text-sm font-semibold">
            {done}/{lessons.length}
          </span>
        </div>
      </header>

      <div className="relative mx-auto w-full max-w-md" style={{ height }}>
        <ol aria-label="Lecciones">
          {lessons.map((lesson, i) => {
            const p = points[i];
            const state = lessonStates[i];
            return (
              <li
                key={lesson.id}
                className="absolute"
                style={{ left: `${p.x}%`, top: p.y, transform: "translate(-50%, -50%)" }}
              >
                <button
                  type="button"
                  onClick={() => setSelected(i)}
                  aria-pressed={chosen === i}
                  aria-label={`Lección ${i + 1}: ${lesson.title}. ${LABEL[state]}`}
                  className={`relative flex h-16 w-16 items-center justify-center rounded-full border-b-[6px] transition focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand ${
                    state === "done"
                      ? "border-[#b86e00] bg-accent text-white"
                      : state === "current"
                        ? "border-brand-strong bg-brand text-on-brand ring-8 ring-brand/15"
                        : state === "open"
                          ? "border-brand-strong bg-brand/80 text-on-brand"
                          : "border-[#d6cfc2] bg-[#ece7de] text-muted"
                  } ${chosen === i ? "scale-110" : "hover:scale-105"}`}
                >
                  <Icon name={state === "done" ? "check" : state === "locked" ? "lock" : "book"} className="h-7 w-7" />
                </button>
                {state === "done" ? <Stars count={lesson.stars} className="absolute left-1/2 top-full mt-1 -translate-x-1/2" /> : null}
              </li>
            );
          })}
        </ol>
        {chosen !== null ? (
          // Burbuja bajo la lección elegida, como en Duolingo; tapa las filas de abajo.
          <div
            className="absolute left-1/2 z-10 w-[min(22rem,calc(100%-2rem))] -translate-x-1/2"
            style={{ top: points[chosen].y + (lessonStates[chosen] === "done" ? 64 : 48) }}
          >
            <LessonCard
              index={chosen}
              lesson={lessons[chosen]}
              state={lessonStates[chosen]}
              isAdmin={isAdmin}
              onClose={() => setSelected(-1)}
            />
          </div>
        ) : null}
        {withApruvi && current >= 0 ? (
          <div
            className="pointer-events-none absolute transition-all duration-700 ease-out"
            style={{
              left: `${points[current].x}%`,
              top: points[current].y,
              transform: `translate(${points[current].x >= 50 ? "calc(-100% - 40px)" : "40px"}, -60%)`,
            }}
          >
            <Apruvi className="h-14 w-14" />
          </div>
        ) : null}
      </div>

    </section>
  );
}

const LABEL: Record<State, string> = {
  done: "Completada",
  current: "Siguiente",
  open: "Disponible",
  locked: "Bloqueada",
};

function LessonCard({
  index,
  lesson,
  state,
  isAdmin,
  onClose,
}: {
  index: number;
  lesson: LessonSummary;
  state: State;
  isAdmin: boolean;
  onClose: () => void;
}) {
  const href = `/practica?leccion=${encodeURIComponent(lesson.id)}`;
  const canOpen = state !== "locked" || isAdmin;
  return (
    <div className="pop-in relative" aria-live="polite">
      <span aria-hidden="true" className="absolute -top-2 left-1/2 h-4 w-4 -translate-x-1/2 rotate-45 border-l border-t border-line bg-surface" />
      <div className="rounded-2xl border border-line bg-surface p-4 shadow-lg">
        <div className="flex items-start justify-between gap-2">
          <p className="text-xs font-semibold text-brand">
            Lección {index + 1} · {lesson.total} preguntas · {LABEL[state]}
          </p>
          <button type="button" onClick={onClose} aria-label="Cerrar" className="-mr-1 -mt-1 rounded-lg px-1.5 text-muted hover:text-foreground">
            ✕
          </button>
        </div>
        <p className="mt-1 font-semibold leading-snug">{lesson.subtopics.join(" · ")}</p>
        {state === "done" ? (
          <p className="mt-1 text-sm text-muted">
            Acertaste {lesson.correct} de {lesson.total} en tu último intento.
          </p>
        ) : state === "locked" ? (
          <p className="mt-1 text-sm text-muted">Completa la lección anterior para desbloquearla.</p>
        ) : (
          <p className="mt-1 text-sm text-muted">
            {lesson.answered > 0
              ? `Llevas ${lesson.answered} de ${lesson.total}. ¡Termínala!`
              : "Si te equivocas, verás la explicación y la fuente."}
          </p>
        )}
        {canOpen ? (
          <ButtonLink href={href} className="mt-3 w-full" variant={state === "done" ? "secondary" : "primary"}>
            {state === "done"
              ? "Repasar"
              : state === "locked"
                ? "Abrir (administrador)"
                : lesson.answered > 0
                  ? "Continuar"
                  : "Empezar"}
          </ButtonLink>
        ) : null}
      </div>
    </div>
  );
}

function Stars({ count, className = "" }: { count: number; className?: string }) {
  return (
    <span className={`flex gap-0.5 ${className}`} aria-label={`${count} de 3 estrellas`} role="img">
      {[0, 1, 2].map((i) => (
        <svg key={i} viewBox="0 0 24 24" className={`h-4 w-4 ${i < count ? "text-accent" : "text-line"}`} aria-hidden="true">
          <path
            fill="currentColor"
            d="m12 2.5 2.9 6 6.6.8-4.9 4.6 1.3 6.6L12 17.2l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8z"
          />
        </svg>
      ))}
    </span>
  );
}
