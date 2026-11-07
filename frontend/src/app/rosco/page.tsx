"use client";

import { useEffect, useRef, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { Apruvi } from "@/components/apruvi";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink, buttonStyles } from "@/components/button";
import { api, type RoscoItem } from "@/lib/api";
import { useStudyAccess } from "@/lib/use-access";
import { useSubjects } from "@/lib/use-subjects";

const SECONDS = 180;

type Outcome = { correct: boolean; term: string; answer: string };
type Game = { items: RoscoItem[]; deadline: number };

function clock(seconds: number) {
  const s = Math.max(0, Math.ceil(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Rosco legal (FR-038): una definición por letra con los términos publicados del glosario.
 * «Pasapalabra» deja la letra para la siguiente vuelta. Es un juego: no registra intentos. */
export default function RoscoPage() {
  const { me, setMe, hasAccess } = useStudyAccess("/rosco");
  const subjects = useSubjects(hasAccess);
  const [subject, setSubject] = useState("");
  const [game, setGame] = useState<Game | null>(null);
  const [outcomes, setOutcomes] = useState<Record<string, Outcome>>({});
  const [current, setCurrent] = useState(0);
  const [answer, setAnswer] = useState("");
  const [finished, setFinished] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [now, setNow] = useState(0); // se fija al empezar: Date.now() no puede ir en el prerender
  const finishRef = useRef<() => void>(() => {});

  async function start() {
    setBusy(true);
    setError(null);
    const params = subject ? `?${new URLSearchParams({ subject })}` : "";
    const response = await api<RoscoItem[]>(`/practice/rosco${params}`);
    setBusy(false);
    if (!response.ok) return setError(response.error.message);
    if (response.data.length === 0) return setError("Todavía no hay términos publicados para el rosco.");
    setOutcomes({});
    setCurrent(0);
    setAnswer("");
    setFinished(false);
    setNow(Date.now());
    setGame({ items: response.data, deadline: Date.now() + SECONDS * 1000 });
  }

  async function check(item: RoscoItem, text: string): Promise<Outcome | null> {
    const response = await api<{ correct: boolean; term: string }>("/practice/rosco/check", {
      body: { id: item.id, answer: text },
    });
    if (!response.ok) {
      setError(response.error.message);
      return null;
    }
    return { ...response.data, answer: text };
  }

  /** Siguiente letra sin responder después de `from`, dando la vuelta; -1 si no queda ninguna. */
  function nextPending(from: number, done: Record<string, Outcome>) {
    if (!game) return -1;
    const n = game.items.length;
    for (let step = 1; step <= n; step++) {
      const i = (from + step) % n;
      if (!done[game.items[i].id]) return i;
    }
    return -1;
  }

  async function finish(done: Record<string, Outcome>) {
    if (!game) return;
    // Al terminar se revelan los términos de las letras que quedaron pendientes.
    const pending = game.items.filter((item) => !done[item.id]);
    const revealed = { ...done };
    for (const item of pending) {
      const outcome = await check(item, "");
      if (outcome) revealed[item.id] = outcome;
    }
    setOutcomes(revealed);
    setFinished(true);
  }

  useEffect(() => {
    finishRef.current = () => void finish(outcomes);
  });

  // El reloj sale de la hora límite, así sobrevive a que la página se oculte y vuelva.
  useEffect(() => {
    if (!game || finished) return;
    const timer = setInterval(() => {
      const t = Date.now();
      setNow(t);
      if (t >= game.deadline) {
        clearInterval(timer);
        finishRef.current();
      }
    }, 250);
    return () => clearInterval(timer);
  }, [game, finished]);

  async function respond(event: React.FormEvent) {
    event.preventDefault();
    if (!game || busy || !answer.trim()) return;
    const item = game.items[current];
    setBusy(true);
    const outcome = await check(item, answer.trim());
    setBusy(false);
    if (!outcome) return;
    const done = { ...outcomes, [item.id]: outcome };
    setOutcomes(done);
    setAnswer("");
    const next = nextPending(current, done);
    if (next < 0) await finish(done);
    else setCurrent(next);
  }

  function pass() {
    if (!game) return;
    setAnswer("");
    const next = nextPending(current, outcomes);
    if (next >= 0) setCurrent(next);
  }

  const item = game?.items[current];
  const correct = Object.values(outcomes).filter((o) => o.correct).length;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-xl flex-1 space-y-6 px-4 pb-16 pt-6">
        {error ? <Alert tone="error">{error}</Alert> : null}
        {!hasAccess || !subjects ? (
          <ApruviLoader label="Armando tu rosco…" />
        ) : game && item ? (
          <section className="space-y-5" aria-label={finished ? "Resultado del rosco" : "Rosco en curso"}>
            <Wheel items={game.items} outcomes={outcomes} current={finished ? -1 : current} />
            {finished ? (
              <div className="pop-in space-y-4 rounded-3xl border border-line bg-surface p-6 text-center">
                <Apruvi className="mx-auto h-20 w-20" />
                <h1 className="text-3xl font-semibold tracking-tight">
                  {correct} de {game.items.length}
                </h1>
                <ol className="space-y-1 text-left text-sm" aria-label="Respuestas">
                  {game.items.map((it) => {
                    const o = outcomes[it.id];
                    return (
                      <li key={it.id} className={o?.correct ? "text-success" : "text-danger"}>
                        <span className="font-bold">{it.letter}</span> · {o?.term}
                        {o && !o.correct && o.answer ? <span className="text-muted"> (dijiste «{o.answer}»)</span> : null}
                      </li>
                    );
                  })}
                </ol>
                <div className="flex flex-col gap-2 sm:flex-row sm:justify-center">
                  <button type="button" onClick={start} className={buttonStyles.primary}>
                    Otro rosco
                  </button>
                  <ButtonLink href="/ruta" variant="secondary">
                    Volver a mi ruta
                  </ButtonLink>
                </div>
              </div>
            ) : (
              <form onSubmit={respond} className="space-y-3 rounded-3xl border border-line bg-surface p-5">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold text-brand">
                    {item.mode === "starts" ? "Empieza con la" : "Contiene la"} {item.letter}
                  </p>
                  <span role="timer" aria-label="Tiempo restante" className="font-mono font-bold">
                    {clock((game.deadline - now) / 1000)}
                  </span>
                </div>
                <p className="text-lg font-semibold leading-snug">{item.definition}</p>
                <p className="text-xs text-muted">{item.subject}</p>
                <input
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  aria-label="Tu respuesta"
                  autoComplete="off"
                  autoFocus
                  className="block w-full rounded-xl border border-line bg-surface px-3 py-2"
                />
                <div className="flex gap-2">
                  <button type="button" onClick={pass} className={`flex-1 ${buttonStyles.secondary}`}>
                    Pasapalabra
                  </button>
                  <button type="submit" disabled={busy || !answer.trim()} className={`flex-1 ${buttonStyles.primary}`}>
                    Responder
                  </button>
                </div>
              </form>
            )}
          </section>
        ) : (
          <section className="space-y-5 rounded-3xl border border-line bg-surface p-6">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Rosco legal</h1>
              <p className="text-muted">
                Una definición por letra y {SECONDS / 60} minutos. Si no la sabes, di «pasapalabra»
                y vuelve a ella en la siguiente vuelta.
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
              {busy ? "Armando…" : "Empezar"}
            </button>
          </section>
        )}
      </main>
    </div>
  );
}

function Wheel({
  items,
  outcomes,
  current,
}: {
  items: RoscoItem[];
  outcomes: Record<string, Outcome>;
  current: number;
}) {
  return (
    <div className="relative mx-auto aspect-square w-full max-w-[20rem]" aria-label="Letras del rosco" role="img">
      {items.map((it, i) => {
        const angle = (i / items.length) * 2 * Math.PI - Math.PI / 2;
        const o = outcomes[it.id];
        return (
          <span
            key={it.id}
            aria-hidden="true"
            className={`absolute flex h-8 w-8 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full text-sm font-bold text-white transition ${
              o ? (o.correct ? "bg-success" : "bg-danger") : "bg-brand"
            } ${i === current ? "scale-125 ring-4 ring-accent" : ""}`}
            style={{ left: `${50 + 44 * Math.cos(angle)}%`, top: `${50 + 44 * Math.sin(angle)}%` }}
          >
            {it.letter}
          </span>
        );
      })}
      <Apruvi className="absolute left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2" />
    </div>
  );
}
