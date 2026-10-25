"use client";

import { useState } from "react";

import { buttonStyles } from "@/components/button";

import { type Detail, LETTERS, StatusBadge } from "./shared";

/** Detalle de una versión: contenido, revisiones, historial y las acciones que permite su
 * estado. Las reglas las aplica el backend (quien crea no aprueba ni publica, AC-029). */
export function QuestionDetail({
  detail,
  busy,
  onAct,
  onEdit,
  onOpen,
}: {
  detail: Detail;
  /** Hay una acción en curso: los botones se deshabilitan para evitar dobles envíos. */
  busy: boolean;
  onAct: (id: string, action: string, body?: unknown) => Promise<void>;
  onEdit: () => void;
  onOpen: (id: string) => void;
}) {
  const [comment, setComment] = useState("");
  const canDecide = !detail.is_author;
  const active = detail.history.some((h) => h.status !== "retired");

  function confirmAndAct(message: string, action: string) {
    if (window.confirm(message)) void onAct(detail.id, action);
  }

  return (
    <div className="space-y-4 rounded-3xl border border-line bg-surface p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <StatusBadge status={detail.status} number={detail.number} />
        <span className="text-xs text-muted">Autor: {detail.is_author ? "tú" : detail.author}</span>
      </div>
      <p className="text-xs font-semibold text-brand">
        {detail.subject}
        {detail.subtopic ? ` · ${detail.subtopic}` : ""}
      </p>
      <h2 className="text-lg font-semibold leading-snug">{detail.prompt}</h2>
      <ol className="space-y-1.5">
        {detail.options.map((option, i) => (
          <li
            key={`${detail.id}-${i}`}
            className={`rounded-xl border px-3 py-2 text-sm ${
              i === detail.correct_position ? "border-success bg-success/10 font-medium" : "border-line"
            }`}
          >
            {LETTERS[i]}. {option}
          </li>
        ))}
      </ol>
      <p className="text-sm">
        <span className="font-semibold">Explicación:</span> {detail.explanation}
      </p>
      <p className="text-sm text-muted">Fuente: {detail.source}</p>

      {detail.reviews.length > 0 ? (
        <ul className="space-y-1 border-t border-line pt-3 text-xs text-muted">
          {detail.reviews.map((r) => (
            <li key={r.created_at}>
              {r.decision === "approved" ? "Aprobada" : "Cambios pedidos"} por {r.reviewer}
              {r.comment ? `: «${r.comment}»` : ""}
            </li>
          ))}
        </ul>
      ) : null}

      <fieldset disabled={busy} className="space-y-2 border-t border-line pt-4">
        {detail.status === "draft" ? (
          <button type="button" onClick={() => void onAct(detail.id, "submit")} className={`w-full ${buttonStyles.primary}`}>
            Enviar a revisión
          </button>
        ) : null}
        {detail.status === "in_review" ? (
          canDecide ? (
            <>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Comentario (obligatorio si pides cambios)"
                rows={2}
                className="w-full rounded-lg border border-line bg-background px-3 py-2 text-sm"
              />
              <div className="flex flex-col gap-2 sm:flex-row">
                <button
                  type="button"
                  onClick={() => void onAct(detail.id, "review", { decision: "approved", comment: comment || null })}
                  className={`flex-1 ${buttonStyles.primary}`}
                >
                  Aprobar
                </button>
                <button
                  type="button"
                  onClick={() => void onAct(detail.id, "review", { decision: "changes_requested", comment })}
                  className={`flex-1 ${buttonStyles.secondary}`}
                >
                  Pedir cambios
                </button>
              </div>
            </>
          ) : (
            <p className="text-sm text-muted">Tú creaste esta versión: otro administrador debe revisarla.</p>
          )
        ) : null}
        {detail.status === "approved" ? (
          canDecide ? (
            <button type="button" onClick={() => void onAct(detail.id, "publish")} className={`w-full ${buttonStyles.primary}`}>
              Publicar
            </button>
          ) : (
            <p className="text-sm text-muted">Tú creaste esta versión: otro administrador debe publicarla.</p>
          )
        ) : null}

        <button type="button" onClick={onEdit} className={`w-full ${buttonStyles.secondary}`}>
          {detail.status === "retired" ? "Reactivar como versión nueva" : "Editar (crea una versión nueva)"}
        </button>

        {detail.status === "published" ? (
          <button
            type="button"
            onClick={() => confirmAndAct("La pregunta dejará de aparecer en la práctica. ¿Retirar esta versión?", "retire")}
            className={`w-full ${buttonStyles.secondary}`}
          >
            Retirar de la práctica
          </button>
        ) : detail.status !== "retired" ? (
          <button
            type="button"
            onClick={() => confirmAndAct("Esta versión quedará descartada (no se borra). ¿Continuar?", "retire")}
            className={`w-full ${buttonStyles.secondary}`}
          >
            Descartar esta versión
          </button>
        ) : null}
      </fieldset>

      <section aria-label="Historial de versiones" className="border-t border-line pt-4">
        <h3 className="text-sm font-semibold">Historial</h3>
        <ol className="mt-2 space-y-1.5">
          {detail.history.map((h) => (
            <li key={h.id}>
              <button
                type="button"
                onClick={() => onOpen(h.id)}
                aria-current={h.id === detail.id ? "true" : undefined}
                className={`flex w-full flex-wrap items-center justify-between gap-2 rounded-xl border px-3 py-2 text-left text-xs ${
                  h.id === detail.id ? "border-brand bg-brand-soft/40" : "border-line hover:border-brand"
                }`}
              >
                <StatusBadge status={h.status} number={h.number} />
                <span className="text-muted">
                  {new Date(h.created_at).toLocaleDateString("es-CL")} · {h.author}
                </span>
              </button>
            </li>
          ))}
        </ol>
        {active ? (
          <button
            type="button"
            onClick={() =>
              confirmAndAct(
                "Se retirarán todas las versiones vigentes de esta pregunta y saldrá de la práctica. Queda en el historial. ¿Continuar?",
                "retire-question",
              )
            }
            className="mt-3 text-sm font-semibold text-danger hover:underline"
          >
            Retirar la pregunta completa
          </button>
        ) : null}
      </section>
    </div>
  );
}
