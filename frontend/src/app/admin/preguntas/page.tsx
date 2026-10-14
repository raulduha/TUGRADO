"use client";

import { useCallback, useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { ApruviLoader } from "@/components/apruvi-loader";
import { buttonStyles } from "@/components/button";
import { api } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

type Status = "draft" | "in_review" | "approved" | "published" | "retired";

type Summary = {
  id: string;
  number: number;
  status: Status;
  subject: string;
  subtopic: string | null;
  difficulty: number;
  prompt: string;
  author: string;
  is_author: boolean;
};

type Detail = Summary & {
  options: string[];
  correct_position: number;
  explanation: string;
  source: string;
  reviews: Array<{ decision: string; comment: string | null; reviewer: string; created_at: string }>;
};

type ImportResult = { imported: number; errors: Array<{ row: number; message: string }> };

const STATUS: Record<Status, { label: string; className: string }> = {
  draft: { label: "Borrador", className: "bg-background text-muted" },
  in_review: { label: "En revisión", className: "bg-accent-soft text-[#9a5b00]" },
  approved: { label: "Aprobada", className: "bg-brand-soft text-brand-strong" },
  published: { label: "Publicada", className: "bg-success/10 text-success" },
  retired: { label: "Retirada", className: "bg-line text-muted" },
};
const FILTERS: Array<Status | "all"> = ["all", "draft", "in_review", "approved", "published", "retired"];
const LETTERS = "ABCDE";
const DIFFICULTY = ["", "Fácil", "Media", "Difícil"];

/** Banco de preguntas (FR-013, FR-014): importar la planilla y llevar cada versión por
 * revisión y publicación. El backend impide que quien creó una versión la apruebe o publique. */
export default function QuestionBankPage() {
  const { me, setMe } = useRequireUser("/admin/preguntas");
  const isAdmin = me?.roles.includes("administrator") ?? false;
  const [filter, setFilter] = useState<Status | "all">("all");
  const [items, setItems] = useState<Summary[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [importing, setImporting] = useState(false);
  const [importResult, setImportResult] = useState<ImportResult | null>(null);
  const [open, setOpen] = useState<Detail | null>(null);

  const load = useCallback(async () => {
    const query = filter === "all" ? "" : `?status=${filter}`;
    const result = await api<Summary[]>(`/admin/questions${query}`);
    if (result.ok) setItems(result.data);
    else setError(result.error.message);
  }, [filter]);

  useEffect(() => {
    if (!isAdmin) return;
    let cancelled = false;
    const query = filter === "all" ? "" : `?status=${filter}`;
    api<Summary[]>(`/admin/questions${query}`).then((result) => {
      if (cancelled) return;
      if (result.ok) setItems(result.data);
      else setError(result.error.message);
    });
    return () => {
      cancelled = true;
    };
  }, [isAdmin, filter]);

  async function upload(file: File) {
    setImporting(true);
    setImportResult(null);
    setError(null);
    const result = await api<ImportResult>("/admin/questions/import", { body: file });
    setImporting(false);
    if (!result.ok) {
      setError(result.error.message);
      return;
    }
    setImportResult(result.data);
    if (result.data.imported > 0) await load();
  }

  async function show(id: string) {
    const result = await api<Detail>(`/admin/questions/${id}`);
    if (result.ok) setOpen(result.data);
    else setError(result.error.message);
  }

  async function act(id: string, action: string, body?: unknown) {
    setError(null);
    const result = await api(`/admin/questions/${id}/${action}`, { method: "POST", body });
    if (!result.ok) {
      setError(result.error.message);
      return;
    }
    await Promise.all([load(), show(id)]);
  }

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-6xl flex-1 space-y-6 px-4 pb-16 pt-6">
        {!me ? (
          <ApruviLoader label="Cargando el banco de preguntas…" />
        ) : !isAdmin ? (
          <Alert tone="error">Esta sección es solo para administradores.</Alert>
        ) : (
          <>
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Banco de preguntas</h1>
                <p className="text-muted">
                  Importa la planilla, envía a revisión y publica. Otra persona debe aprobar y
                  publicar lo que tú creaste.
                </p>
              </div>
              <label className={`cursor-pointer ${buttonStyles.primary}`}>
                {importing ? "Importando…" : "Importar planilla (.xlsx)"}
                <input
                  type="file"
                  accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  className="sr-only"
                  disabled={importing}
                  onChange={(event) => {
                    const file = event.currentTarget.files?.[0];
                    event.currentTarget.value = "";
                    if (file) void upload(file);
                  }}
                />
              </label>
            </div>

            {error ? <Alert tone="error">{error}</Alert> : null}
            {importResult ? (
              importResult.errors.length === 0 ? (
                <Alert tone="success">
                  Se importaron {importResult.imported} preguntas como borradores.
                </Alert>
              ) : (
                <Alert tone="error">
                  <p className="font-semibold">No se importó nada: corrige estas filas y vuelve a subir.</p>
                  <ul className="mt-2 list-disc pl-5">
                    {importResult.errors.map((e) => (
                      <li key={`${e.row}-${e.message}`}>
                        {e.row > 0 ? `Fila ${e.row}: ` : ""}
                        {e.message}
                      </li>
                    ))}
                  </ul>
                </Alert>
              )
            ) : null}

            <div className="flex flex-wrap gap-2" role="tablist" aria-label="Filtrar por estado">
              {FILTERS.map((f) => (
                <button
                  key={f}
                  type="button"
                  role="tab"
                  aria-selected={filter === f}
                  onClick={() => setFilter(f)}
                  className={`rounded-full border px-3 py-1.5 text-sm font-medium ${
                    filter === f ? "border-brand bg-brand text-on-brand" : "border-line bg-surface hover:border-brand"
                  }`}
                >
                  {f === "all" ? "Todas" : STATUS[f].label}
                </button>
              ))}
            </div>

            <div className="grid gap-6 lg:grid-cols-[3fr_2fr]">
              <section aria-label="Versiones" className="space-y-2">
                {items === null ? (
                  <p className="text-muted">Cargando…</p>
                ) : items.length === 0 ? (
                  <p className="rounded-2xl border border-dashed border-line p-6 text-center text-muted">
                    No hay preguntas en este estado. Importa la plantilla de
                    docs/plantillas/preguntas-alternativas.xlsx.
                  </p>
                ) : (
                  items.map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => void show(item.id)}
                      className={`flex w-full items-start gap-3 rounded-2xl border bg-surface p-4 text-left transition hover:border-brand ${
                        open?.id === item.id ? "border-brand" : "border-line"
                      }`}
                    >
                      <span className={`flex-none rounded-full px-2.5 py-1 text-xs font-semibold ${STATUS[item.status].className}`}>
                        {STATUS[item.status].label}
                      </span>
                      <span className="min-w-0 flex-1">
                        <span className="block text-xs text-muted">
                          {item.subject}
                          {item.subtopic ? ` · ${item.subtopic}` : ""} · {DIFFICULTY[item.difficulty]} · v
                          {item.number}
                        </span>
                        <span className="block font-medium">{item.prompt}</span>
                      </span>
                    </button>
                  ))
                )}
              </section>

              <section aria-label="Detalle" className="lg:sticky lg:top-4 lg:self-start">
                {open ? (
                  <Review detail={open} onAct={act} />
                ) : (
                  <p className="rounded-2xl border border-dashed border-line p-6 text-center text-muted">
                    Elige una pregunta para revisarla.
                  </p>
                )}
              </section>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

function Review({
  detail,
  onAct,
}: {
  detail: Detail;
  onAct: (id: string, action: string, body?: unknown) => Promise<void>;
}) {
  const [comment, setComment] = useState("");
  const canDecide = !detail.is_author;

  return (
    <div className="space-y-4 rounded-3xl border border-line bg-surface p-5">
      <div className="flex items-center justify-between">
        <span className={`whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-semibold ${STATUS[detail.status].className}`}>
          {STATUS[detail.status].label} · v{detail.number}
        </span>
        <span className="text-xs text-muted">Autor: {detail.is_author ? "tú" : detail.author}</span>
      </div>
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

      <div className="space-y-2 border-t border-line pt-4">
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
              <div className="flex gap-2">
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
        {detail.status === "published" ? (
          <button type="button" onClick={() => void onAct(detail.id, "retire")} className={`w-full ${buttonStyles.secondary}`}>
            Retirar de la práctica
          </button>
        ) : null}
      </div>
    </div>
  );
}
