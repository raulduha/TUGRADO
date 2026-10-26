"use client";

import { useEffect, useRef, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { Apruvi } from "@/components/apruvi";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink, buttonStyles } from "@/components/button";
import { api, type ExamResult, type PracticeQuestion } from "@/lib/api";
import { useStudyAccess } from "@/lib/use-access";
import { useSubjects } from "@/lib/use-subjects";

const SIZES = [10, 20, 40];
const SECONDS_PER_QUESTION = 90;
const LETTERS = ["A", "B", "C", "D", "E"];

type Exam = { questions: PracticeQuestion[]; deadline: number; startedAt: number };

function clock(seconds: number) {
  const s = Math.max(0, Math.round(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Prueba cronometrada (FR-037): preguntas al azar del banco publicado, se corrige al entregar.
 * El tiempo es orientativo: al acabarse, la prueba se entrega con lo respondido. */
export default function ExamPage() {
  const { me, setMe, hasAccess } = useStudyAccess("/prueba");
  const subjects = useSubjects(hasAccess);
  const [subject, setSubject] = useState("");
  const [size, setSize] = useState(20);
  const [exam, setExam] = useState<Exam | null>(null);
  const [chosen, setChosen] = useState<Record<string, number>>({});
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState<ExamResult | null>(null);
  const [usedSeconds, setUsedSeconds] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function start() {
    setBusy(true);
    setError(null);
    const params = new URLSearchParams({ size: String(size) });
    if (subject) params.set("subject", subject);
    const response = await api<PracticeQuestion[]>(`/practice/exam?${params}`);
    setBusy(false);
    if (!response.ok) return setError(response.error.message);
    if (response.data.length === 0) return setError("Todavía no hay preguntas publicadas de esa materia.");
    const now = Date.now();
    setChosen({});
    setIndex(0);
    setResult(null);
    setExam({
      questions: response.data,
      startedAt: now,
      deadline: now + response.data.length * SECONDS_PER_QUESTION * 1000,
    });
  }

  async function submit() {
    if (!exam || busy) return;
    setBusy(true);
    setError(null);
    const response = await api<ExamResult>("/practice/exam/grade", {
      body: { answers: exam.questions.map((q) => ({ version_id: q.id, position: chosen[q.id] ?? null })) },
    });
    setBusy(false);
    if (!response.ok) return setError(response.error.message);
    setUsedSeconds(Math.min((Date.now() - exam.startedAt) / 1000, (exam.deadline - exam.startedAt) / 1000));
    setResult(response.data);
  }

  function reset() {
    setExam(null);
    setResult(null);
  }

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-2xl flex-1 space-y-6 px-4 pb-16 pt-6">
        {error ? <Alert tone="error">{error}</Alert> : null}
        {!hasAccess || !subjects ? (
          <ApruviLoader label="Preparando tu prueba…" />
        ) : result && exam ? (
          <Results exam={exam} chosen={chosen} result={result} usedSeconds={usedSeconds} onRestart={reset} />
        ) : exam ? (
          <Running
            exam={exam}
            chosen={chosen}
            index={index}
            busy={busy}
            onChoose={(id, position) => setChosen((c) => ({ ...c, [id]: position }))}
            onGo={setIndex}
            onSubmit={submit}
          />
        ) : (
          <section className="space-y-5 rounded-3xl border border-line bg-surface p-6">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Prueba cronometrada</h1>
              <p className="text-muted">
                Responde contra el reloj, como en el examen. Al entregar verás tu resultado, la
                explicación de cada pregunta y en qué subtemas te conviene reforzar.
              </p>
            </div>
            <label className="block">
              <span className="text-sm font-semibold">Materia</span>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="mt-1 block w-full rounded-xl border border-line bg-surface px-3 py-2"
              >
                <option value="">Todas las materias</option>
                {subjects.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </label>
            <fieldset>
              <legend className="text-sm font-semibold">Preguntas</legend>
              <div className="mt-1 flex flex-wrap gap-2">
                {SIZES.map((value) => (
                  <button
                    key={value}
                    type="button"
                    aria-pressed={size === value}
                    onClick={() => setSize(value)}
                    className={`rounded-xl border-2 px-4 py-2 text-sm font-semibold transition ${
                      size === value ? "border-brand bg-brand-soft text-brand" : "border-line bg-surface hover:border-brand/50"
                    }`}
                  >
                    {`${value} · ${clock(value * SECONDS_PER_QUESTION)} min`}
                  </button>
                ))}
              </div>
            </fieldset>
            <button type="button" onClick={start} disabled={busy} className={`w-full ${buttonStyles.primary}`}>
              {busy ? "Preparando…" : "Comenzar prueba"}
            </button>
          </section>
        )}
      </main>
    </div>
  );
}

function Running({
  exam,
  chosen,
  index,
  busy,
  onChoose,
  onGo,
  onSubmit,
}: {
  exam: Exam;
  chosen: Record<string, number>;
  index: number;
  busy: boolean;
  onChoose: (id: string, position: number) => void;
  onGo: (index: number) => void;
  onSubmit: () => void;
}) {
  const [now, setNow] = useState(() => Date.now());
  const submitRef = useRef(onSubmit);
  useEffect(() => {
    submitRef.current = onSubmit;
  });
  // El reloj sale de la hora límite, así que sobrevive a cambios de página y recargas del estado.
  useEffect(() => {
    const timer = setInterval(() => {
      const current = Date.now();
      setNow(current);
      if (current >= exam.deadline) {
        clearInterval(timer);
        submitRef.current();
      }
    }, 500);
    return () => clearInterval(timer);
  }, [exam.deadline]);

  const question = exam.questions[index];
  const total = exam.questions.length;
  const remaining = (exam.deadline - now) / 1000;
  const unanswered = exam.questions.filter((q) => chosen[q.id] === undefined).length;

  return (
    <section className="space-y-5" aria-label="Prueba en curso">
      <div className="flex items-center justify-between gap-3 rounded-2xl border border-line bg-surface px-4 py-3">
        <span className="text-sm font-semibold text-muted">
          Pregunta {index + 1} de {total}
        </span>
        <span
          role="timer"
          aria-label="Tiempo restante"
          className={`font-mono text-lg font-bold ${remaining < 60 ? "text-danger" : "text-foreground"}`}
        >
          {clock(remaining)}
        </span>
      </div>

      <div className="rounded-2xl border border-line bg-surface px-4 py-4">
        <p className="text-xs font-semibold text-brand">
          {question.subject}
          {question.subtopic ? ` · ${question.subtopic}` : ""}
        </p>
        <h1 className="mt-1 text-xl font-semibold leading-snug">{question.prompt}</h1>
      </div>

      <ol className="space-y-3" aria-label="Alternativas">
        {question.options.map((option, i) => {
          const picked = chosen[question.id] === i;
          return (
            <li key={`${question.id}-${i}`}>
              <button
                type="button"
                aria-pressed={picked}
                onClick={() => onChoose(question.id, i)}
                className={`flex w-full items-center gap-3 rounded-2xl border-2 border-b-[5px] px-4 py-3 text-left font-medium transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand ${
                  picked ? "border-brand bg-brand-soft" : "border-line bg-surface hover:border-brand/50"
                }`}
              >
                <span
                  className={`flex h-8 w-8 flex-none items-center justify-center rounded-lg border-2 text-sm font-bold ${
                    picked ? "border-current" : "border-line text-muted"
                  }`}
                >
                  {LETTERS[i]}
                </span>
                {option}
              </button>
            </li>
          );
        })}
      </ol>

      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => onGo(index - 1)}
          disabled={index === 0}
          className={`flex-1 ${buttonStyles.secondary}`}
        >
          Anterior
        </button>
        <button
          type="button"
          onClick={() => onGo(index + 1)}
          disabled={index + 1 >= total}
          className={`flex-1 ${buttonStyles.secondary}`}
        >
          Siguiente
        </button>
      </div>

      <nav aria-label="Ir a una pregunta" className="flex flex-wrap gap-1.5">
        {exam.questions.map((q, i) => (
          <button
            key={q.id}
            type="button"
            onClick={() => onGo(i)}
            aria-label={`Pregunta ${i + 1}${chosen[q.id] === undefined ? ", sin responder" : ", respondida"}`}
            aria-current={i === index ? "step" : undefined}
            className={`h-9 w-9 rounded-lg border text-sm font-semibold ${
              i === index
                ? "border-brand bg-brand text-on-brand"
                : chosen[q.id] !== undefined
                  ? "border-brand/40 bg-brand-soft text-brand"
                  : "border-line bg-surface text-muted"
            }`}
          >
            {i + 1}
          </button>
        ))}
      </nav>

      <div className="space-y-2">
        {unanswered > 0 ? (
          <p className="text-sm text-muted">
            {unanswered === 1 ? "Te queda 1 pregunta sin responder." : `Te quedan ${unanswered} preguntas sin responder.`}
          </p>
        ) : null}
        <button type="button" onClick={onSubmit} disabled={busy} className={`w-full ${buttonStyles.primary}`}>
          {busy ? "Corrigiendo…" : "Entregar prueba"}
        </button>
      </div>
    </section>
  );
}

function Results({
  exam,
  chosen,
  result,
  usedSeconds,
  onRestart,
}: {
  exam: Exam;
  chosen: Record<string, number>;
  result: ExamResult;
  usedSeconds: number;
  onRestart: () => void;
}) {
  const percent = result.total ? Math.round((result.correct / result.total) * 100) : 0;
  const items = new Map(result.items.map((item) => [item.id, item]));

  return (
    <section className="space-y-6" aria-label="Resultado de la prueba">
      <div className="pop-in rounded-3xl border border-line bg-surface p-6 text-center">
        <Apruvi className="mx-auto h-24 w-24" />
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">
          {result.correct} de {result.total}
        </h1>
        <p className="text-lg">
          <span className={`font-semibold ${percent >= 60 ? "text-success" : "text-danger"}`}>{percent} %</span> de
          respuestas correctas · {clock(usedSeconds)} min
        </p>
        <p className="mt-1 text-sm text-muted">
          Las que fallaste vuelven mañana en tu repaso. Las sin responder no cuentan como intento.
        </p>
        <div className="mt-5 flex flex-col gap-2 sm:flex-row sm:justify-center">
          <button type="button" onClick={onRestart} className={buttonStyles.primary}>
            Nueva prueba
          </button>
          <ButtonLink href="/ruta" variant="secondary">
            Volver a mi ruta
          </ButtonLink>
        </div>
      </div>

      <div className="rounded-3xl border border-line bg-surface p-5">
        <h2 className="font-semibold">Por subtema</h2>
        <p className="text-sm text-muted">Primero, los que más te conviene reforzar.</p>
        <ul className="mt-3 space-y-3">
          {result.by_subtopic.map((s) => (
            <li key={`${s.subject}-${s.subtopic}`}>
              <div className="flex justify-between gap-3 text-sm">
                <span>
                  {s.subtopic ?? "General"} <span className="text-muted">· {s.subject}</span>
                </span>
                <span className="font-semibold">
                  {s.correct}/{s.total}
                </span>
              </div>
              <div className="mt-1 h-2 overflow-hidden rounded-full bg-line">
                <div className="h-full rounded-full bg-accent" style={{ width: `${(s.correct / s.total) * 100}%` }} />
              </div>
            </li>
          ))}
        </ul>
      </div>

      <ol className="space-y-4" aria-label="Revisión">
        {exam.questions.map((q, i) => {
          const item = items.get(q.id);
          if (!item) return null; // dejó de estar publicada durante la prueba
          return (
            <li key={q.id} className="rounded-2xl border border-line bg-surface p-4">
              <p className="text-xs font-semibold text-brand">
                {i + 1}. {item.correct ? "Correcta" : chosen[q.id] === undefined ? "Sin responder" : "Incorrecta"}
              </p>
              <p className="mt-1 font-semibold">{q.prompt}</p>
              <ul className="mt-2 space-y-1 text-sm">
                {q.options.map((option, j) => (
                  <li
                    key={j}
                    className={
                      j === item.correct_position
                        ? "font-semibold text-success"
                        : j === item.chosen
                          ? "text-danger line-through"
                          : "text-muted"
                    }
                  >
                    {LETTERS[j]}. {option}
                  </li>
                ))}
              </ul>
              <p className="mt-2 text-sm">{item.explanation}</p>
              <p className="mt-0.5 text-xs text-muted">Fuente: {item.source}</p>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
