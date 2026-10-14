"use client";

import { useEffect, useState } from "react";

import { AppHeader } from "@/components/app-header";
import { Apruvi } from "@/components/apruvi";
import { ApruviLoader } from "@/components/apruvi-loader";
import { ButtonLink, buttonStyles } from "@/components/button";
import { DemoBanner } from "@/components/demo-banner";
import { Icon } from "@/components/illustrations";
import { grade, ORAL_SAMPLE } from "@/lib/oral-sample";
import { useStudyAccess } from "@/lib/use-access";

type Step = "setup" | "question" | "recording" | "processing" | "result";
type FeedbackMode = "each" | "end";

function mmss(seconds: number): string {
  const s = Math.max(0, seconds);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Simulación oral — mockup sin micrófono ni IA. En la versión real el backend es la
 * autoridad del tiempo (latidos, extensiones, pausas); aquí el reloj es solo ilustrativo. */
export default function OralSimulationPage() {
  const { me, setMe, hasAccess } = useStudyAccess("/simulacion");
  const [step, setStep] = useState<Step>("setup");
  const [mode, setMode] = useState<FeedbackMode>("each");
  const [left, setLeft] = useState(ORAL_SAMPLE.questionSeconds);

  // Reloj ilustrativo: corre mientras se ve la pregunta o se graba.
  useEffect(() => {
    if (step !== "question" && step !== "recording") return;
    const id = window.setInterval(() => setLeft((s) => s - 1), 1000);
    return () => window.clearInterval(id);
  }, [step]);

  // La "transcripción y evaluación" simulada dura un par de segundos (no consume tiempo).
  useEffect(() => {
    if (step !== "processing") return;
    const id = window.setTimeout(() => setStep("result"), 2600);
    return () => window.clearTimeout(id);
  }, [step]);

  const { weighted, mark } = grade(ORAL_SAMPLE.criteria);

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-2xl flex-1 space-y-6 px-4 pb-16 pt-6">
        {!me || !hasAccess ? (
          <ApruviLoader label="Preparando tu simulación…" />
        ) : (
          <>
            <DemoBanner>
              No se usa tu micrófono: la transcripción y la evaluación son de ejemplo.
            </DemoBanner>

            {step === "setup" ? (
              <section className="space-y-5 rounded-3xl border border-line bg-surface p-6 sm:p-8">
                <div className="flex items-center gap-4">
                  <Apruvi className="h-20 w-20 flex-none" />
                  <div>
                    <h1 className="text-2xl font-semibold tracking-tight">Simulación oral</h1>
                    <p className="text-muted">
                      {ORAL_SAMPLE.subject} · {ORAL_SAMPLE.totalMinutes} min en total ·{" "}
                      {mmss(ORAL_SAMPLE.questionSeconds)} por pregunta
                    </p>
                  </div>
                </div>
                <fieldset className="space-y-2">
                  <legend className="font-semibold">¿Cuándo quieres la retroalimentación?</legend>
                  {(
                    [
                      ["each", "Después de cada pregunta"],
                      ["end", "Al final de la simulación"],
                    ] as const
                  ).map(([value, label]) => (
                    <label
                      key={value}
                      className={`flex cursor-pointer items-center gap-3 rounded-2xl border-2 px-4 py-3 ${
                        mode === value ? "border-brand bg-brand-soft" : "border-line"
                      }`}
                    >
                      <input
                        type="radio"
                        name="mode"
                        value={value}
                        checked={mode === value}
                        onChange={() => setMode(value)}
                        className="accent-[var(--brand)]"
                      />
                      {label}
                    </label>
                  ))}
                  <p className="text-xs text-muted">Se fija al comenzar y no cambia durante la sesión.</p>
                </fieldset>
                <button type="button" onClick={() => setStep("question")} className={`w-full ${buttonStyles.primary}`}>
                  Comenzar simulación
                </button>
              </section>
            ) : null}

            {step === "question" || step === "recording" ? (
              <section className="space-y-6 rounded-3xl bg-brand p-6 text-on-brand sm:p-8">
                <div className="flex items-center justify-between text-sm font-semibold">
                  <span>Pregunta 1 de 3</span>
                  <span className="flex items-center gap-2 rounded-full bg-white/15 px-3 py-1" role="timer">
                    <Icon name="clock" className="h-4 w-4" /> {mmss(left)}
                  </span>
                </div>
                <h1 className="text-2xl font-semibold leading-snug">{ORAL_SAMPLE.question}</h1>
                <div className="flex flex-col items-center gap-4 py-4">
                  <button
                    type="button"
                    onClick={() => setStep(step === "question" ? "recording" : "processing")}
                    aria-pressed={step === "recording"}
                    aria-label={step === "question" ? "Responder en voz alta" : "Terminar respuesta"}
                    className={`relative flex h-28 w-28 items-center justify-center rounded-full border-b-8 transition focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-white ${
                      step === "recording"
                        ? "border-[#b42318] bg-[#f04438]"
                        : "border-brand-strong bg-white text-brand"
                    }`}
                  >
                    {step === "recording" ? (
                      <span className="absolute inset-0 animate-ping rounded-full bg-white/30" />
                    ) : null}
                    <Icon name="mic" className="h-12 w-12" />
                  </button>
                  <p className="font-semibold">
                    {step === "question" ? "Toca para responder en voz alta" : "Grabando… toca para terminar"}
                  </p>
                  {step === "recording" ? (
                    <div className="flex h-10 items-center gap-1.5" aria-hidden="true">
                      {[0, 1, 2, 3, 4, 5, 6].map((i) => (
                        <span
                          key={i}
                          className="loader-dot w-2 rounded-full bg-white"
                          style={{ height: `${20 + ((i * 37) % 60)}%`, animationDelay: `${i * 90}ms` }}
                        />
                      ))}
                    </div>
                  ) : null}
                </div>
              </section>
            ) : null}

            {step === "processing" ? (
              <section className="rounded-3xl border border-line bg-surface">
                <ApruviLoader label="Transcribiendo y evaluando tu respuesta…" />
                <p className="pb-6 text-center text-sm text-muted">
                  Este tiempo no se descuenta de tu simulación.
                </p>
              </section>
            ) : null}

            {step === "result" ? (
              <section className="pop-in space-y-6 rounded-3xl border border-line bg-surface p-6 sm:p-8">
                <div className="flex items-center gap-4">
                  <Apruvi className="h-20 w-20 flex-none" />
                  <div>
                    <p className="text-sm font-semibold text-muted">Evaluación orientativa</p>
                    <p className="text-5xl font-semibold tracking-tight">
                      {mark.toFixed(1).replace(".", ",")}
                      <span className="text-xl font-medium text-muted"> / 7,0</span>
                    </p>
                    <p className="text-xs text-muted">
                      Promedio ponderado {weighted.toFixed(1).replace(".", ",")} / 100 · no es una
                      calificación oficial
                    </p>
                  </div>
                </div>

                <div>
                  <h2 className="font-semibold">Tu respuesta (transcripción)</h2>
                  <p className="mt-2 rounded-2xl bg-background p-4 text-sm leading-relaxed">
                    {ORAL_SAMPLE.transcript}
                  </p>
                </div>

                <div>
                  <h2 className="font-semibold">Criterios de la rúbrica</h2>
                  <ul className="mt-3 space-y-4">
                    {ORAL_SAMPLE.criteria.map((c) => (
                      <li key={c.name}>
                        <div className="flex justify-between text-sm font-medium">
                          <span>
                            {c.name} <span className="text-muted">· {c.weight} %</span>
                          </span>
                          <span>{c.score}/100</span>
                        </div>
                        <div className="mt-1.5 h-2.5 overflow-hidden rounded-full bg-line">
                          <div className="h-full rounded-full bg-brand" style={{ width: `${c.score}%` }} />
                        </div>
                        <p className="mt-1 text-sm text-muted">{c.comment}</p>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex flex-col gap-2 sm:flex-row">
                  <button
                    type="button"
                    onClick={() => {
                      setLeft(ORAL_SAMPLE.questionSeconds);
                      setStep("setup");
                    }}
                    className={buttonStyles.primary}
                  >
                    Volver a intentar
                  </button>
                  <ButtonLink href="/panel" variant="secondary">
                    Volver al mapa
                  </ButtonLink>
                </div>
                <p className="text-xs text-muted">
                  ¿No estás de acuerdo con la evaluación? En la versión real podrás reportarla para
                  que el equipo la revise.
                </p>
              </section>
            ) : null}
          </>
        )}
      </main>
    </div>
  );
}
