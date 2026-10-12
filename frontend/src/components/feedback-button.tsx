"use client";

import { usePathname } from "next/navigation";
import { useActionState, useRef, useState } from "react";

import { Alert } from "@/components/alert";
import { SubmitButton } from "@/components/submit-button";
import { api } from "@/lib/api";

export const FEEDBACK_MAX_LENGTH = 2000;

const CATEGORIES = [
  { value: "suggestion", label: "Sugerencia" },
  { value: "problem", label: "Problema" },
  { value: "other", label: "Otro" },
] as const;

// `key` identifica la apertura del cuadro: al reabrirlo se muestra un formulario nuevo.
type State =
  | { status: "idle" }
  | { status: "sent"; key: number }
  | { status: "error"; key: number; message: string };

export function FeedbackButton() {
  const dialog = useRef<HTMLDialogElement>(null);
  const pathname = usePathname();
  const [length, setLength] = useState(0);
  const [formKey, setFormKey] = useState(0);
  const [state, action, pending] = useActionState(
    async (_: State, form: FormData): Promise<State> => {
      const result = await api("/feedback", {
        body: {
          category: form.get("category"),
          message: String(form.get("message") ?? ""),
          page: pathname,
        },
      });
      const key = Number(form.get("key"));
      return result.ok
        ? { status: "sent", key }
        : { status: "error", key, message: result.error.message };
    },
    { status: "idle" },
  );

  function open() {
    // Cada apertura empieza con el formulario limpio.
    setFormKey((k) => k + 1);
    setLength(0);
    dialog.current?.showModal();
  }

  return (
    <>
      <button
        type="button"
        onClick={open}
        className="fixed bottom-4 right-4 z-10 inline-flex items-center gap-2 rounded-full bg-brand p-3.5 font-semibold sm:px-4 sm:py-3 text-on-brand shadow-lg transition hover:bg-brand-strong focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand sm:bottom-6 sm:right-6"
      >
        <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z" />
        </svg>
        {/* En móvil solo el ícono, para no tapar contenido; el nombre accesible no cambia. */}
        <span className="sr-only sm:not-sr-only">Enviar comentarios</span>
      </button>

      <dialog
        ref={dialog}
        aria-labelledby="feedback-title"
        className="m-auto w-[calc(100%-2rem)] max-w-lg rounded-2xl border border-line bg-surface p-0 text-foreground shadow-xl backdrop:bg-foreground/40"
      >
        <div className="p-6">
          <div className="flex items-start justify-between gap-4">
            <h2 id="feedback-title" className="text-xl font-semibold tracking-tight">
              ¿Cómo te está yendo?
            </h2>
            <button
              type="button"
              onClick={() => dialog.current?.close()}
              aria-label="Cerrar"
              className="-m-2 rounded-lg p-2 text-muted hover:text-foreground focus-visible:outline-2 focus-visible:outline-brand"
            >
              <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
                <path d="M6 6l12 12M18 6 6 18" />
              </svg>
            </button>
          </div>

          {state.status === "sent" && state.key === formKey ? (
            <div className="mt-4 space-y-4">
              <Alert tone="success">¡Gracias! Leemos todos los comentarios.</Alert>
              <button
                type="button"
                onClick={() => dialog.current?.close()}
                className="w-full rounded-lg border border-line px-4 py-2.5 font-semibold hover:border-brand"
              >
                Cerrar
              </button>
            </div>
          ) : (
            <form key={formKey} action={action} className="mt-4 space-y-5">
              <p className="text-sm text-muted">
                Cuéntanos qué mejorarías o si algo no funcionó. No incluyas datos personales
                sensibles.
              </p>
              {state.status === "error" && state.key === formKey ? (
                <Alert tone="error">{state.message}</Alert>
              ) : null}
              <input type="hidden" name="key" value={formKey} />
              <fieldset>
                <legend className="text-sm font-medium">Tipo de comentario</legend>
                <div className="mt-2 flex flex-wrap gap-2">
                  {CATEGORIES.map((category, index) => (
                    <label
                      key={category.value}
                      className="cursor-pointer rounded-full border border-line px-4 py-2 text-sm has-[:checked]:border-brand has-[:checked]:bg-brand-soft has-[:checked]:text-brand has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-brand"
                    >
                      <input
                        type="radio"
                        name="category"
                        value={category.value}
                        defaultChecked={index === 0}
                        className="sr-only"
                      />
                      {category.label}
                    </label>
                  ))}
                </div>
              </fieldset>
              <div className="space-y-1.5">
                <label htmlFor="feedback-message" className="block text-sm font-medium">
                  Tu comentario
                </label>
                <textarea
                  id="feedback-message"
                  name="message"
                  required
                  rows={5}
                  maxLength={FEEDBACK_MAX_LENGTH}
                  onChange={(event) => setLength(event.target.value.length)}
                  aria-describedby="feedback-count"
                  className="block w-full resize-y rounded-lg border border-line bg-background px-3 py-2.5 text-base outline-none focus:border-brand focus:ring-2 focus:ring-brand/30"
                />
                <p id="feedback-count" className="text-right text-xs text-muted">
                  {length} / {FEEDBACK_MAX_LENGTH}
                </p>
              </div>
              <SubmitButton pending={pending}>Enviar</SubmitButton>
            </form>
          )}
        </div>
      </dialog>
    </>
  );
}
