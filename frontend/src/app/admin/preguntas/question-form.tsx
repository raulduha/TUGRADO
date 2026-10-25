"use client";

import { type FormEvent, useState } from "react";

import { Alert } from "@/components/alert";
import { buttonStyles } from "@/components/button";

import {
  DIFFICULTY,
  type Detail,
  LETTERS,
  MAX_OPTIONS,
  MIN_OPTIONS,
  type QuestionInput,
  type SubjectOption,
} from "./shared";

const EMPTY: QuestionInput = {
  subject: "",
  subtopic: null,
  difficulty: 1,
  prompt: "",
  options: ["", "", "", ""],
  correct_position: 0,
  explanation: "",
  source: "",
};

const FIELD = "w-full rounded-xl border border-line bg-background px-3 py-2 text-sm focus:border-brand focus:outline-none";
// Los textos largos se ven completos: el campo crece con su contenido.
const GROWING = `${FIELD} [field-sizing:content] min-h-10`;

/** Formulario para crear una pregunta o una versión nueva de una existente. Al editar nunca se
 * modifica la versión de origen: se guarda la siguiente como borrador. */
export function QuestionForm({
  base,
  subjects,
  onSubmit,
  onCancel,
}: {
  /** Versión de la que parte la edición; sin ella, es una pregunta nueva. */
  base?: Detail;
  subjects: SubjectOption[];
  onSubmit: (content: QuestionInput) => Promise<string | null>;
  onCancel: () => void;
}) {
  const [value, setValue] = useState<QuestionInput>(
    base
      ? {
          subject: base.subject,
          subtopic: base.subtopic,
          difficulty: base.difficulty,
          prompt: base.prompt,
          options: base.options,
          correct_position: base.correct_position,
          explanation: base.explanation,
          source: base.source,
        }
      : EMPTY,
  );
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const subtopics = subjects.find((s) => s.name === value.subject)?.subtopics ?? [];
  const nextNumber = base ? Math.max(...base.history.map((h) => h.number)) + 1 : 1;

  function set<K extends keyof QuestionInput>(key: K, v: QuestionInput[K]) {
    setValue((current) => ({ ...current, [key]: v }));
  }

  function setOption(i: number, text: string) {
    set("options", value.options.map((o, j) => (j === i ? text : o)));
  }

  function removeOption(i: number) {
    const options = value.options.filter((_, j) => j !== i);
    const correct = value.correct_position;
    set("options", options);
    set("correct_position", correct === i ? 0 : correct > i ? correct - 1 : correct);
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    const options = value.options.map((o) => o.trim());
    if (options.some((o) => !o)) return setError("Completa todas las alternativas o elimina las vacías.");
    if (new Set(options.map((o) => o.toLowerCase())).size !== options.length) {
      return setError("Hay alternativas repetidas.");
    }
    setError(null);
    setSaving(true);
    const message = await onSubmit({ ...value, options, subtopic: value.subtopic?.trim() || null });
    setSaving(false);
    if (message) setError(message);
  }

  return (
    <form onSubmit={submit} className="space-y-4 rounded-3xl border border-line bg-surface p-5" aria-label={base ? "Editar pregunta" : "Nueva pregunta"}>
      <div>
        <h2 className="text-lg font-semibold">{base ? "Editar pregunta" : "Nueva pregunta"}</h2>
        <p className="text-sm text-muted">
          {base
            ? `Se guardará como versión ${nextNumber} en borrador. La versión ${base.number} no cambia y, si está publicada, sigue visible hasta que se publique la nueva.`
            : "Se guardará como borrador. Otro administrador debe aprobarla y publicarla."}
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <label className="block text-sm font-medium">
          Materia
          <input
            required
            maxLength={120}
            list="admin-subjects"
            value={value.subject}
            onChange={(e) => set("subject", e.target.value)}
            className={`mt-1 ${FIELD}`}
          />
          <datalist id="admin-subjects">
            {subjects.map((s) => (
              <option key={s.name} value={s.name} />
            ))}
          </datalist>
        </label>
        <label className="block text-sm font-medium">
          Subtema <span className="font-normal text-muted">(opcional)</span>
          <input
            maxLength={160}
            list="admin-subtopics"
            value={value.subtopic ?? ""}
            onChange={(e) => set("subtopic", e.target.value)}
            className={`mt-1 ${FIELD}`}
          />
          <datalist id="admin-subtopics">
            {subtopics.map((s) => (
              <option key={s} value={s} />
            ))}
          </datalist>
        </label>
      </div>

      <label className="block text-sm font-medium">
        Dificultad
        <select
          value={value.difficulty}
          onChange={(e) => set("difficulty", Number(e.target.value))}
          className={`mt-1 ${FIELD}`}
        >
          {[1, 2, 3].map((d) => (
            <option key={d} value={d}>
              {d} · {DIFFICULTY[d]}
            </option>
          ))}
        </select>
      </label>

      <label className="block text-sm font-medium">
        Enunciado
        <textarea required rows={3} value={value.prompt} onChange={(e) => set("prompt", e.target.value)} className={`mt-1 ${GROWING}`} />
      </label>

      <fieldset className="space-y-2">
        <legend className="text-sm font-medium">Alternativas (marca la correcta)</legend>
        {value.options.map((option, i) => (
          <div key={i} className="flex items-start gap-2">
            <label className="flex h-10 flex-none items-center gap-1.5 text-sm font-semibold">
              <input
                type="radio"
                name="correcta"
                checked={value.correct_position === i}
                onChange={() => set("correct_position", i)}
                aria-label={`La ${LETTERS[i]} es la correcta`}
              />
              {LETTERS[i]}
            </label>
            <textarea
              required
              rows={1}
              value={option}
              onChange={(e) => setOption(i, e.target.value)}
              aria-label={`Alternativa ${LETTERS[i]}`}
              className={`min-w-0 flex-1 ${GROWING}`}
            />
            {value.options.length > MIN_OPTIONS ? (
              <button
                type="button"
                onClick={() => removeOption(i)}
                aria-label={`Eliminar la alternativa ${LETTERS[i]}`}
                className="h-10 flex-none rounded-lg px-2 text-muted hover:text-danger"
              >
                ✕
              </button>
            ) : null}
          </div>
        ))}
        {value.options.length < MAX_OPTIONS ? (
          <button type="button" onClick={() => set("options", [...value.options, ""])} className="text-sm font-semibold text-brand hover:underline">
            + Agregar alternativa
          </button>
        ) : null}
      </fieldset>

      <label className="block text-sm font-medium">
        Explicación
        <textarea required rows={4} value={value.explanation} onChange={(e) => set("explanation", e.target.value)} className={`mt-1 ${GROWING}`} />
      </label>

      <label className="block text-sm font-medium">
        Fuente
        <input required maxLength={300} value={value.source} onChange={(e) => set("source", e.target.value)} className={`mt-1 ${FIELD}`} />
      </label>

      {error ? <Alert tone="error">{error}</Alert> : null}

      <div className="flex flex-col gap-2 sm:flex-row">
        <button type="submit" disabled={saving} className={`flex-1 ${buttonStyles.primary}`}>
          {saving ? "Guardando…" : base ? `Guardar como versión ${nextNumber}` : "Crear borrador"}
        </button>
        <button type="button" onClick={onCancel} className={`flex-1 ${buttonStyles.secondary}`}>
          Cancelar
        </button>
      </div>
    </form>
  );
}
