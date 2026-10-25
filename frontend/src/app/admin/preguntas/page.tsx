"use client";

import { useCallback, useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { ApruviLoader } from "@/components/apruvi-loader";
import { buttonStyles } from "@/components/button";
import { api } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

import { QuestionDetail } from "./question-detail";
import { QuestionForm } from "./question-form";
import {
  DIFFICULTY,
  type Detail,
  type QuestionInput,
  STATUS,
  type Status,
  StatusBadge,
  type SubjectOption,
  type Summary,
} from "./shared";

type ImportResult = {
  created: number;
  updated: number;
  retired: number;
  unchanged: number;
  errors: Array<{ row: number; message: string }>;
};

function plural(n: number, one: string, many: string) {
  return `${n} ${n === 1 ? one : many}`;
}

/** Resumen de lo que hizo la planilla, sin mencionar lo que no aplica. */
function summary(r: ImportResult) {
  const parts = [
    r.created ? plural(r.created, "pregunta nueva", "preguntas nuevas") : "",
    r.updated ? plural(r.updated, "pregunta modificada", "preguntas modificadas") : "",
    r.retired ? plural(r.retired, "pregunta retirada", "preguntas retiradas") : "",
  ].filter(Boolean);
  if (parts.length === 0) return "La planilla no trae cambios.";
  const drafts = r.created + r.updated > 0 ? " Lo nuevo y lo modificado queda como borrador." : "";
  return `Listo: ${parts.join(", ")}.${drafts}`;
}

// Acción masiva disponible según el filtro: el backend aplica las mismas reglas que a una sola.
const BULK: Partial<Record<Status, { action: string; label: string }>> = {
  draft: { action: "submit", label: "Enviar todas a revisión" },
  in_review: { action: "approve", label: "Aprobar todas" },
  approved: { action: "publish", label: "Publicar todas" },
};
type BulkResult = { done: number; skipped: Array<{ id: string; message: string }> };

const FILTERS: Array<Status | "all"> = ["all", "draft", "in_review", "approved", "published", "retired"];
const PAGE = 50;

type Filters = { status: Status | "all"; subject: string; q: string };
type Panel = { kind: "detail"; detail: Detail } | { kind: "create" } | { kind: "edit"; base: Detail } | null;

function query(filters: Filters, limit: number, offset: number) {
  const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
  if (filters.status !== "all") params.set("status", filters.status);
  if (filters.subject) params.set("subject", filters.subject);
  if (filters.q.trim()) params.set("q", filters.q.trim());
  return `/admin/questions?${params}`;
}

/** Banco de preguntas (FR-013, FR-014, AC-044, AC-046): crear, editar como versión nueva,
 * descartar o retirar, buscar y revisar; también la planilla de ida y vuelta. Nada se borra y
 * el backend impide que quien creó una versión la apruebe o publique. */
export default function QuestionBankPage() {
  const { me, setMe } = useRequireUser("/admin/preguntas");
  const isAdmin = me?.roles.includes("administrator") ?? false;
  const [filters, setFilters] = useState<Filters>({ status: "all", subject: "", q: "" });
  const [search, setSearch] = useState("");
  const [items, setItems] = useState<Summary[] | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [subjects, setSubjects] = useState<SubjectOption[]>([]);
  const [panel, setPanel] = useState<Panel>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [importing, setImporting] = useState(false);
  const [importResult, setImportResult] = useState<ImportResult | null>(null);
  const [bulking, setBulking] = useState(false);

  // La búsqueda se aplica al dejar de escribir.
  useEffect(() => {
    const timer = setTimeout(() => setFilters((f) => (f.q === search ? f : { ...f, q: search })), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const load = useCallback(async () => {
    const [list, subjectList] = await Promise.all([
      api<Summary[]>(query(filters, PAGE, 0)),
      api<SubjectOption[]>("/admin/questions/subjects"),
    ]);
    if (list.ok) {
      setItems(list.data);
      setHasMore(list.data.length === PAGE);
    } else setError(list.error.message);
    if (subjectList.ok) setSubjects(subjectList.data);
  }, [filters]);

  useEffect(() => {
    if (!isAdmin) return;
    let cancelled = false;
    Promise.all([api<Summary[]>(query(filters, PAGE, 0)), api<SubjectOption[]>("/admin/questions/subjects")]).then(
      ([list, subjectList]) => {
        if (cancelled) return;
        if (list.ok) {
          setItems(list.data);
          setHasMore(list.data.length === PAGE);
        } else setError(list.error.message);
        if (subjectList.ok) setSubjects(subjectList.data);
      },
    );
    return () => {
      cancelled = true;
    };
  }, [isAdmin, filters]);

  async function loadMore() {
    if (!items) return;
    const result = await api<Summary[]>(query(filters, PAGE, items.length));
    if (!result.ok) return setError(result.error.message);
    setItems([...items, ...result.data]);
    setHasMore(result.data.length === PAGE);
  }

  async function upload(file: File) {
    setImporting(true);
    setImportResult(null);
    setError(null);
    const result = await api<ImportResult>("/admin/questions/import", { body: file });
    setImporting(false);
    if (!result.ok) return setError(result.error.message);
    setImportResult(result.data);
    const { created, updated, retired } = result.data;
    if (created + updated + retired > 0) await load();
  }

  /** Aplica la acción a todas las versiones del filtro, no solo a las cargadas en pantalla. */
  async function bulk(action: string) {
    setError(null);
    setNotice(null);
    setBulking(true);
    const ids: string[] = [];
    for (let offset = 0; ; offset += 500) {
      const page = await api<Summary[]>(query(filters, 500, offset));
      if (!page.ok) {
        setBulking(false);
        return setError(page.error.message);
      }
      ids.push(...page.data.map((i) => i.id));
      if (page.data.length < 500) break;
    }
    const result = ids.length
      ? await api<BulkResult>("/admin/questions/bulk", { body: { action, ids } })
      : null;
    setBulking(false);
    if (result && !result.ok) return setError(result.error.message);
    const done = result?.data.done ?? 0;
    const skipped = result?.data.skipped ?? [];
    const reasons = [...new Set(skipped.map((s) => s.message))];
    setNotice(
      `${done} ${done === 1 ? "pregunta avanzó" : "preguntas avanzaron"}.` +
        (skipped.length ? ` ${skipped.length} no se pudieron mover: ${reasons.join(" ")}` : ""),
    );
    setPanel(null);
    await load();
  }

  async function show(id: string) {
    setError(null);
    const result = await api<Detail>(`/admin/questions/${id}`);
    if (result.ok) setPanel({ kind: "detail", detail: result.data });
    else setError(result.error.message);
  }

  async function act(id: string, action: string, body?: unknown) {
    setError(null);
    setNotice(null);
    const result = await api(`/admin/questions/${id}/${action}`, { method: "POST", body });
    if (!result.ok) return setError(result.error.message);
    await Promise.all([load(), show(id)]);
  }

  /** Guarda el formulario. Devuelve el mensaje de error para mostrarlo en el formulario. */
  async function save(content: QuestionInput): Promise<string | null> {
    const path = panel?.kind === "edit" ? `/admin/questions/${panel.base.id}/edit` : "/admin/questions";
    const result = await api<{ id: string }>(path, { body: content });
    if (!result.ok) return result.error.message;
    setNotice(panel?.kind === "edit" ? "Se guardó la versión nueva como borrador." : "Se creó la pregunta como borrador.");
    await Promise.all([load(), show(result.data.id)]);
    return null;
  }

  const selectedId = panel?.kind === "detail" ? panel.detail.id : panel?.kind === "edit" ? panel.base.id : null;
  const bulkAction = filters.status !== "all" ? BULK[filters.status] : undefined;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-6xl flex-1 space-y-5 px-4 pb-16 pt-6">
        {!me ? (
          <ApruviLoader label="Cargando el banco de preguntas…" />
        ) : !isAdmin ? (
          <Alert tone="error">Esta sección es solo para administradores.</Alert>
        ) : (
          <>
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Banco de preguntas</h1>
                <p className="text-muted">
                  Crea, edita o retira preguntas una a una, o en bloque con la planilla. Cada cambio
                  es una versión nueva y otra persona debe aprobarla y publicarla.
                </p>
              </div>
              <div className="grid shrink-0 grid-cols-2 gap-2 sm:flex">
                <button
                  type="button"
                  onClick={() => setPanel({ kind: "create" })}
                  className={`col-span-2 whitespace-nowrap ${buttonStyles.primary}`}
                >
                  Nueva pregunta
                </button>
                {/* Descargas directas: el backend responde el .xlsx como adjunto. */}
                <a href="/api/admin/questions/template" download className={`!px-3 sm:whitespace-nowrap ${buttonStyles.secondary}`}>
                  Plantilla vacía
                </a>
                <a href="/api/admin/questions/export" download className={`!px-3 sm:whitespace-nowrap ${buttonStyles.secondary}`}>
                  Descargar banco (.xlsx)
                </a>
                <label className={`col-span-2 cursor-pointer sm:whitespace-nowrap ${buttonStyles.secondary}`}>
                  {importing ? "Subiendo…" : "Subir planilla (.xlsx)"}
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
            </div>

            <details className="rounded-2xl border border-line bg-surface p-4 text-sm">
              <summary className="cursor-pointer font-semibold">Cómo usar la planilla</summary>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-muted">
                <li>Fila sin id: pregunta nueva.</li>
                <li>
                  Fila con id y algún cambio: nueva versión en borrador. La publicada sigue visible
                  hasta que se publique la nueva.
                </li>
                <li>Escribe «sí» en la columna retirar para sacar una pregunta. No se borra: queda en el historial.</li>
                <li>Borrar una fila del Excel no retira la pregunta. No modifiques la columna id.</li>
                <li>Si una fila tiene un error, no se aplica nada y se indica cada fila.</li>
              </ul>
            </details>

            {error ? <Alert tone="error">{error}</Alert> : null}
            {notice ? <Alert tone="success">{notice}</Alert> : null}
            {importResult ? (
              importResult.errors.length === 0 ? (
                <Alert tone="success">{summary(importResult)}</Alert>
              ) : (
                <Alert tone="error">
                  <p className="font-semibold">No se aplicó ningún cambio: corrige estas filas y vuelve a subir.</p>
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

            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                type="search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Buscar por enunciado o subtema"
                aria-label="Buscar preguntas"
                className="min-w-0 flex-1 rounded-xl border border-line bg-surface px-3 py-2 text-sm focus:border-brand focus:outline-none"
              />
              <select
                value={filters.subject}
                onChange={(e) => setFilters({ ...filters, subject: e.target.value })}
                aria-label="Filtrar por materia"
                className="rounded-xl border border-line bg-surface px-3 py-2 text-sm sm:w-64"
              >
                <option value="">Todas las materias</option>
                {subjects.map((s) => (
                  <option key={s.name} value={s.name}>
                    {s.name}
                  </option>
                ))}
              </select>
            </div>

            {/* En móvil los estados se desplazan dentro de su fila, sin mover la página. */}
            <div className="-mx-4 overflow-x-auto px-4">
              <div className="flex w-max gap-2" role="tablist" aria-label="Filtrar por estado">
                {FILTERS.map((f) => (
                  <button
                    key={f}
                    type="button"
                    role="tab"
                    aria-selected={filters.status === f}
                    onClick={() => setFilters({ ...filters, status: f })}
                    className={`whitespace-nowrap rounded-full border px-3 py-1.5 text-sm font-medium ${
                      filters.status === f ? "border-brand bg-brand text-on-brand" : "border-line bg-surface hover:border-brand"
                    }`}
                  >
                    {f === "all" ? "Todas" : STATUS[f].label}
                  </button>
                ))}
              </div>
            </div>

            {bulkAction && items && items.length > 0 ? (
              <div className="flex flex-col gap-2 rounded-2xl border border-line bg-surface p-4 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-sm text-muted">
                  Se aplica a todas las preguntas de este filtro. Lo que tú creaste debe aprobarlo y
                  publicarlo otro administrador.
                </p>
                <button
                  type="button"
                  disabled={bulking}
                  onClick={() => void bulk(bulkAction.action)}
                  className={`whitespace-nowrap ${buttonStyles.primary}`}
                >
                  {bulking ? "Aplicando…" : bulkAction.label}
                </button>
              </div>
            ) : null}

            <div className="grid gap-6 lg:grid-cols-[3fr_2fr]">
              <section aria-label="Versiones" className="min-w-0 space-y-2">
                {items === null ? (
                  <p className="text-muted">Cargando…</p>
                ) : items.length === 0 ? (
                  <p className="rounded-2xl border border-dashed border-line p-6 text-center text-muted">
                    No hay preguntas con estos filtros. Crea una con «Nueva pregunta» o sube la
                    planilla.
                  </p>
                ) : (
                  <>
                    {items.map((item) => (
                      <button
                        key={item.id}
                        type="button"
                        onClick={() => void show(item.id)}
                        className={`flex w-full flex-col gap-2 rounded-2xl border bg-surface p-4 text-left transition hover:border-brand sm:flex-row sm:items-start sm:gap-3 ${
                          selectedId === item.id ? "border-brand" : "border-line"
                        }`}
                      >
                        <span className="flex-none">
                          <StatusBadge status={item.status} />
                        </span>
                        <span className="min-w-0 flex-1">
                          <span className="block text-xs text-muted">
                            {item.subject}
                            {item.subtopic ? ` · ${item.subtopic}` : ""} · {DIFFICULTY[item.difficulty]} · v{item.number}
                          </span>
                          <span className="block break-words font-medium">{item.prompt}</span>
                        </span>
                      </button>
                    ))}
                    {hasMore ? (
                      <button type="button" onClick={() => void loadMore()} className={`w-full ${buttonStyles.secondary}`}>
                        Cargar más
                      </button>
                    ) : null}
                  </>
                )}
              </section>

              {/* En escritorio el panel va al lado; en móvil se abre a pantalla completa. */}
              <section
                aria-label="Detalle"
                className={
                  panel
                    ? "fixed inset-0 z-40 overflow-y-auto bg-background px-4 pb-10 pt-4 lg:static lg:z-auto lg:self-start lg:overflow-visible lg:bg-transparent lg:p-0 lg:sticky lg:top-4"
                    : "hidden lg:block lg:sticky lg:top-4 lg:self-start"
                }
              >
                {panel ? (
                  <button
                    type="button"
                    onClick={() => setPanel(null)}
                    className="mb-3 text-sm font-semibold text-brand lg:hidden"
                  >
                    ← Volver a la lista
                  </button>
                ) : null}
                {panel?.kind === "detail" ? (
                  <QuestionDetail
                    key={panel.detail.id}
                    detail={panel.detail}
                    onAct={act}
                    onEdit={() => setPanel({ kind: "edit", base: panel.detail })}
                    onOpen={(id) => void show(id)}
                  />
                ) : panel?.kind === "create" ? (
                  <QuestionForm key="create" subjects={subjects} onSubmit={save} onCancel={() => setPanel(null)} />
                ) : panel?.kind === "edit" ? (
                  <QuestionForm
                    key={`edit-${panel.base.id}`}
                    base={panel.base}
                    subjects={subjects}
                    onSubmit={save}
                    onCancel={() => setPanel({ kind: "detail", detail: panel.base })}
                  />
                ) : (
                  <p className="rounded-2xl border border-dashed border-line p-6 text-center text-muted">
                    Elige una pregunta para revisarla, o crea una nueva.
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
