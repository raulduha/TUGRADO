"use client";

import { useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { Apruvi } from "@/components/apruvi";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink, buttonStyles } from "@/components/button";
import { DemoBanner } from "@/components/demo-banner";
import { Icon } from "@/components/illustrations";
import { api, type PracticeQuestion, type PracticeResult } from "@/lib/api";
import { SAMPLE_QUESTIONS } from "@/lib/practice-sample";
import { useStudyAccess } from "@/lib/use-access";

const LETTERS = ["A", "B", "C", "D", "E", "F"];

// Sin preguntas publicadas todavía, la práctica muestra las de ejemplo (vista previa).
const SAMPLE: PracticeQuestion[] = SAMPLE_QUESTIONS.map((q) => ({
  id: q.id,
  subject: q.subject,
  subtopic: null,
  difficulty: 1,
  prompt: q.prompt,
  options: q.options,
}));

function sampleResult(id: string, position: number): PracticeResult {
  const q = SAMPLE_QUESTIONS.find((s) => s.id === id)!;
  return {
    correct: position === q.correct,
    correct_position: q.correct,
    explanation: q.explanation,
    source: q.source,
  };
}

/** Práctica de alternativas (FR-006): preguntas publicadas del banco; la respuesta correcta
 * la entrega el backend recién al responder. */
export default function PracticePage() {
  const { me, setMe, hasAccess } = useStudyAccess("/practica");
  const [questions, setQuestions] = useState<PracticeQuestion[] | null>(null);
  const [demo, setDemo] = useState(false);
  const [index, setIndex] = useState(0);
  const [picked, setPicked] = useState<number | null>(null);
  const [result, setResult] = useState<PracticeResult | null>(null);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [score, setScore] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!hasAccess) return;
    let cancelled = false;
    api<PracticeQuestion[]>("/practice/questions?limit=10").then((response) => {
      if (cancelled) return;
      if (response.ok && response.data.length > 0) {
        setQuestions(response.data);
        setDemo(false);
      } else {
        setQuestions(SAMPLE);
        setDemo(true);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [hasAccess]);

  const question = questions?.[index];
  const total = questions?.length ?? 0;
  const checked = result !== null;
  const correct = result?.correct ?? false;

  async function check() {
    if (picked === null || !question) return;
    setError(null);
    let outcome: PracticeResult;
    if (demo) {
      outcome = sampleResult(question.id, picked);
    } else {
      setChecking(true);
      const response = await api<PracticeResult>("/practice/answers", {
        body: { version_id: question.id, position: picked },
      });
      setChecking(false);
      if (!response.ok) {
        setError(response.error.message);
        return;
      }
      outcome = response.data;
    }
    setResult(outcome);
    if (outcome.correct) setScore((s) => s + 1);
  }

  function next() {
    if (index + 1 >= total) {
      setDone(true);
      return;
    }
    setIndex(index + 1);
    setPicked(null);
    setResult(null);
  }

  function restart() {
    setIndex(0);
    setPicked(null);
    setResult(null);
    setScore(0);
    setDone(false);
  }

  const ready = me && hasAccess && question;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-2xl flex-1 px-4 pb-40 pt-6">
        {!ready ? (
          <ApruviLoader label="Preparando tu práctica…" />
        ) : done ? (
          <section className="pop-in mt-6 rounded-3xl border border-line bg-surface p-8 text-center">
            <Apruvi className="mx-auto h-28 w-28" />
            <h1 className="mt-4 text-3xl font-semibold tracking-tight">¡Práctica terminada!</h1>
            <p className="mt-2 text-lg">
              Acertaste <span className="font-semibold text-success">{score}</span> de {total}.
            </p>
            <p className="mt-1 text-sm text-muted">
              {score === total
                ? "¡Impecable! Sigue así."
                : "Repasa las explicaciones de las que fallaste: así se fija lo aprendido."}
            </p>
            <div className="mt-6 flex flex-col gap-2 sm:flex-row sm:justify-center">
              <button type="button" onClick={restart} className={buttonStyles.primary}>
                Practicar de nuevo
              </button>
              <ButtonLink href="/panel" variant="secondary">
                Volver al mapa
              </ButtonLink>
            </div>
          </section>
        ) : (
          <>
            {demo ? (
              <DemoBanner>Aún no hay preguntas publicadas; estas son de ejemplo.</DemoBanner>
            ) : null}

            <div className="mt-5 flex items-center gap-3">
              <ButtonLink href="/panel" variant="secondary" className="!px-3 !py-2">
                ✕
              </ButtonLink>
              <div
                className="h-4 flex-1 overflow-hidden rounded-full bg-line"
                role="progressbar"
                aria-label="Avance de la práctica"
                aria-valuemin={0}
                aria-valuemax={total}
                aria-valuenow={index + (checked ? 1 : 0)}
              >
                <div
                  className="h-full rounded-full bg-success transition-all duration-500"
                  style={{ width: `${((index + (checked ? 1 : 0)) / total) * 100}%` }}
                />
              </div>
              <span className="text-sm font-semibold text-muted">
                {index + 1}/{total}
              </span>
            </div>

            <div className="mt-6 flex items-end gap-3">
              <Apruvi className="h-20 w-20 flex-none" />
              <div className="relative flex-1 rounded-2xl border border-line bg-surface px-4 py-3">
                <p className="text-xs font-semibold text-brand">
                  {question.subject}
                  {question.subtopic ? ` · ${question.subtopic}` : ""}
                </p>
                <h1 className="mt-1 text-xl font-semibold leading-snug">{question.prompt}</h1>
              </div>
            </div>

            {error ? (
              <div className="mt-4">
                <Alert tone="error">{error}</Alert>
              </div>
            ) : null}

            <ol className="mt-6 space-y-3" aria-label="Alternativas">
              {question.options.map((option, i) => {
                const isPicked = picked === i;
                const isRight = checked && i === result.correct_position;
                const isWrong = checked && isPicked && !result.correct;
                return (
                  <li key={`${question.id}-${i}`}>
                    <button
                      type="button"
                      disabled={checked || checking}
                      onClick={() => setPicked(i)}
                      aria-pressed={isPicked}
                      className={`flex w-full items-center gap-3 rounded-2xl border-2 border-b-[5px] px-4 py-3 text-left font-medium transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand ${
                        isRight
                          ? "border-success bg-success/10"
                          : isWrong
                            ? "border-danger bg-danger/10"
                            : isPicked
                              ? "border-brand bg-brand-soft"
                              : "border-line bg-surface hover:border-brand/50"
                      }`}
                    >
                      <span
                        className={`flex h-8 w-8 flex-none items-center justify-center rounded-lg border-2 text-sm font-bold ${
                          isPicked || isRight ? "border-current" : "border-line text-muted"
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
          </>
        )}
      </main>

      {ready && !done ? (
        <div
          className={`fixed inset-x-0 bottom-0 border-t px-4 py-4 ${
            !checked
              ? "border-line bg-surface"
              : correct
                ? "border-success/30 bg-[#e7f6ee]"
                : "border-danger/30 bg-[#fdecea]"
          }`}
          aria-live="polite"
        >
          <div className="mx-auto flex max-w-2xl flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            {checked ? (
              <div className="pop-in flex items-start gap-3">
                <span
                  className={`flex h-10 w-10 flex-none items-center justify-center rounded-full text-white ${
                    correct ? "bg-success" : "bg-danger"
                  }`}
                >
                  <Icon name={correct ? "check" : "repeat"} />
                </span>
                <div>
                  <p className={`font-semibold ${correct ? "text-success" : "text-danger"}`}>
                    {correct ? "¡Correcto!" : `Respuesta correcta: ${LETTERS[result.correct_position]}`}
                  </p>
                  <p className="text-sm">{result.explanation}</p>
                  <p className="mt-0.5 text-xs text-muted">Fuente: {result.source}</p>
                </div>
              </div>
            ) : (
              <p className="hidden text-sm text-muted sm:block">Elige una alternativa.</p>
            )}
            <button
              type="button"
              onClick={checked ? next : check}
              disabled={picked === null || checking}
              className={`sm:w-48 ${buttonStyles.primary} ${checked && !correct ? "!bg-danger" : ""} ${
                checked && correct ? "!bg-success" : ""
              }`}
            >
              {checked
                ? index + 1 >= total
                  ? "Ver resultado"
                  : "Continuar"
                : checking
                  ? "Comprobando…"
                  : "Comprobar"}
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
