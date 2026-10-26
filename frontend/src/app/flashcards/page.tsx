"use client";

import { useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { Apruvi } from "@/components/apruvi";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink, buttonStyles } from "@/components/button";
import { api, type Flashcard } from "@/lib/api";
import { useStudyAccess } from "@/lib/use-access";
import { useSubjects } from "@/lib/use-subjects";

const LETTERS = ["A", "B", "C", "D", "E"];

const STATUS: Record<Flashcard["status"], string> = {
  review: "Toca repasar",
  pending: "Por dominar",
  mastered: "Ya la dominas",
};

/** Flashcards (FR-037): tarjetas del banco publicado para repasar en pocos minutos. Primero lo
 * que toca repasar hoy; la tarjeta que no sabías vuelve al final de la ronda. No registran
 * respuestas: para eso están la práctica y la prueba. */
export default function FlashcardsPage() {
  const { me, setMe, hasAccess } = useStudyAccess("/flashcards");
  const subjects = useSubjects(hasAccess);
  const [subject, setSubject] = useState("");
  const [deck, setDeck] = useState<Flashcard[] | null>(null);
  const [position, setPosition] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [known, setKnown] = useState(0);
  const [requeued, setRequeued] = useState<Set<string>>(new Set());
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function start() {
    setBusy(true);
    setError(null);
    const params = new URLSearchParams({ limit: "20" });
    if (subject) params.set("subject", subject);
    const response = await api<Flashcard[]>(`/practice/flashcards?${params}`);
    setBusy(false);
    if (!response.ok) return setError(response.error.message);
    if (response.data.length === 0) return setError("Todavía no hay preguntas publicadas de esa materia.");
    setDeck(response.data);
    setPosition(0);
    setFlipped(false);
    setKnown(0);
    setRequeued(new Set());
  }

  function next(knewIt: boolean) {
    if (!deck) return;
    const card = deck[position];
    if (knewIt) setKnown((k) => k + 1);
    else if (!requeued.has(card.id)) {
      // Una sola vez por ronda: la tarjeta que no sabías vuelve al final.
      setDeck([...deck, card]);
      setRequeued(new Set(requeued).add(card.id));
    }
    setPosition(position + 1);
    setFlipped(false);
  }

  const card = deck?.[position];
  const firstPass = deck ? deck.length - requeued.size : 0;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-xl flex-1 space-y-6 px-4 pb-16 pt-6">
        {error ? <Alert tone="error">{error}</Alert> : null}
        {!hasAccess || !subjects ? (
          <ApruviLoader label="Barajando tus tarjetas…" />
        ) : deck && !card ? (
          <section className="pop-in rounded-3xl border border-line bg-surface p-8 text-center">
            <Apruvi className="mx-auto h-24 w-24" />
            <h1 className="mt-3 text-2xl font-semibold tracking-tight">¡Ronda terminada!</h1>
            <p className="mt-1 text-muted">
              Sabías {known} de {firstPass} tarjetas.
              {requeued.size > 0 ? " Las que no, practícalas en la ruta o en una prueba para fijarlas." : ""}
            </p>
            <div className="mt-5 flex flex-col gap-2 sm:flex-row sm:justify-center">
              <button type="button" onClick={start} className={buttonStyles.primary}>
                Otra ronda
              </button>
              <ButtonLink href="/ruta" variant="secondary">
                Volver a mi ruta
              </ButtonLink>
            </div>
          </section>
        ) : deck && card ? (
          <section className="space-y-4" aria-label="Flashcards">
            <div className="flex items-center justify-between text-sm text-muted">
              <span>
                Tarjeta {Math.min(position + 1, deck.length)} de {deck.length}
              </span>
              <span className="rounded-full bg-brand-soft px-2.5 py-0.5 text-xs font-semibold text-brand">
                {STATUS[card.status]}
              </span>
            </div>
            <button
              type="button"
              onClick={() => setFlipped(!flipped)}
              aria-label={flipped ? "Ver la pregunta" : "Ver la respuesta"}
              className="pop-in block min-h-64 w-full rounded-3xl border-2 border-b-[6px] border-line bg-surface p-6 text-left transition hover:border-brand/50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand"
            >
              <p className="text-xs font-semibold text-brand">
                {card.subject}
                {card.subtopic ? ` · ${card.subtopic}` : ""}
              </p>
              {flipped ? (
                <>
                  <p className="mt-3 font-semibold leading-snug">{card.prompt}</p>
                  <ul className="mt-3 space-y-1 text-sm">
                    {card.options.map((option, i) => (
                      <li
                        key={i}
                        className={i === card.correct_position ? "font-semibold text-success" : "text-muted"}
                      >
                        {LETTERS[i]}. {option}
                      </li>
                    ))}
                  </ul>
                  <p className="mt-3 text-sm">{card.explanation}</p>
                  <p className="mt-2 text-xs text-muted">Fuente: {card.source}</p>
                </>
              ) : (
                <>
                  <p className="mt-3 text-xl font-semibold leading-snug">{card.prompt}</p>
                  <p className="mt-6 text-sm text-muted">Piensa la respuesta y toca la tarjeta para verla.</p>
                </>
              )}
            </button>
            {flipped ? (
              <div className="flex gap-2">
                <button type="button" onClick={() => next(false)} className={`flex-1 ${buttonStyles.secondary}`}>
                  No la sabía
                </button>
                <button type="button" onClick={() => next(true)} className={`flex-1 ${buttonStyles.primary}`}>
                  La sabía
                </button>
              </div>
            ) : (
              <button type="button" onClick={() => setFlipped(true)} className={`w-full ${buttonStyles.primary}`}>
                Ver respuesta
              </button>
            )}
          </section>
        ) : (
          <section className="space-y-5 rounded-3xl border border-line bg-surface p-6">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Flashcards</h1>
              <p className="text-muted">
                Repasa en pocos minutos: lee la pregunta, piensa la respuesta y da vuelta la tarjeta.
                Primero salen las que te toca repasar.
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
            <button type="button" onClick={start} disabled={busy} className={`w-full ${buttonStyles.primary}`}>
              {busy ? "Barajando…" : "Empezar"}
            </button>
          </section>
        )}
      </main>
    </div>
  );
}
