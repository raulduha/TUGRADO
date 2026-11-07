"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { Alert } from "@/components/alert";
import { AppHeader } from "@/components/app-header";
import { ApruviLoader } from "@/components/apruvi-loader";
import { buttonStyles } from "@/components/button";
import { api, type GlossaryTerm } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

type Status = GlossaryTerm["status"];

const TABS: Array<{ status: Status; label: string }> = [
  { status: "draft", label: "Borrador" },
  { status: "approved", label: "Aprobados" },
  { status: "published", label: "Publicados" },
  { status: "retired", label: "Retirados" },
];

// Acción que avanza cada estado; quien cargó el término no puede aprobarlo ni publicarlo.
const NEXT: Partial<Record<Status, { action: "approve" | "publish"; label: string }>> = {
  draft: { action: "approve", label: "Aprobar" },
  approved: { action: "publish", label: "Publicar" },
};

/** Glosario del rosco legal (FR-038): cargar la planilla, aprobar y publicar en bloque. */
export default function GlossaryAdminPage() {
  const { me, setMe } = useRequireUser("/admin/glosario");
  const isAdmin = me?.roles.includes("administrator") ?? false;
  const [tab, setTab] = useState<Status>("draft");
  const [terms, setTerms] = useState<GlossaryTerm[] | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [message, setMessage] = useState<{ tone: "success" | "error"; text: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [reload, setReload] = useState(0);
  const latest = useRef(0);

  useEffect(() => {
    if (!isAdmin) return;
    const request = ++latest.current;
    api<GlossaryTerm[]>(`/admin/glossary?status=${tab}`).then((result) => {
      if (request !== latest.current) return; // solo cuenta la última respuesta
      setTerms(result.ok ? result.data : []);
      setSelected(new Set());
    });
  }, [isAdmin, tab, reload]);

  async function upload(file: File) {
    setBusy(true);
    setMessage(null);
    const result = await api<{ created: number; errors: Array<{ row: number; message: string }> }>(
      "/admin/glossary/import",
      { body: file },
    );
    setBusy(false);
    if (!result.ok) return setMessage({ tone: "error", text: result.error.message });
    if (result.data.errors.length) {
      const text = result.data.errors.map((e) => (e.row ? `Fila ${e.row}: ${e.message}` : e.message)).join(" ");
      return setMessage({ tone: "error", text: `No se cargó nada. ${text}` });
    }
    setMessage({ tone: "success", text: `Se cargaron ${result.data.created} términos en borrador.` });
    setTab("draft");
    setReload((n) => n + 1);
  }

  async function bulk(action: "approve" | "publish" | "retire") {
    setBusy(true);
    setMessage(null);
    const result = await api<{ done: number; skipped: Array<{ reason: string }> }>("/admin/glossary/bulk", {
      body: { action, ids: [...selected] },
    });
    setBusy(false);
    if (!result.ok) return setMessage({ tone: "error", text: result.error.message });
    const { done, skipped } = result.data;
    const reasons = [...new Set(skipped.map((s) => s.reason))].join(" ");
    setMessage({
      tone: skipped.length ? "error" : "success",
      text: `Listo: ${done}.${skipped.length ? ` Se saltaron ${skipped.length}: ${reasons}` : ""}`,
    });
    setReload((n) => n + 1);
  }

  const next = NEXT[tab];
  const allSelected = !!terms?.length && selected.size === terms.length;

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader me={me} onLoggedOut={() => setMe(null)} />
      <main className="mx-auto w-full max-w-5xl flex-1 space-y-5 px-4 pb-16 pt-6">
        {!me ? (
          <ApruviLoader label="Cargando el glosario…" />
        ) : !isAdmin ? (
          <Alert tone="error">Esta sección es solo para administradores.</Alert>
        ) : (
          <>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Glosario del rosco</h1>
                <p className="text-muted">
                  Carga términos con la planilla; otra persona los aprueba y luego los publica. Solo
                  los publicados aparecen en el rosco.
                </p>
                <Link href="/admin/preguntas" className="text-sm font-semibold text-brand hover:underline">
                  ← Banco de preguntas
                </Link>
              </div>
              <div className="flex gap-2">
                <a href="/api/admin/glossary/template" download className={`!px-3 ${buttonStyles.secondary}`}>
                  Plantilla
                </a>
                <label className={`!px-3 cursor-pointer ${buttonStyles.primary}`}>
                  Subir planilla
                  <input
                    type="file"
                    accept=".xlsx"
                    className="sr-only"
                    disabled={busy}
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      e.target.value = "";
                      if (file) void upload(file);
                    }}
                  />
                </label>
              </div>
            </div>

            {message ? <Alert tone={message.tone}>{message.text}</Alert> : null}

            <div role="tablist" aria-label="Estado" className="flex flex-wrap gap-2">
              {TABS.map((t) => (
                <button
                  key={t.status}
                  type="button"
                  role="tab"
                  aria-selected={tab === t.status}
                  onClick={() => setTab(t.status)}
                  className={`rounded-xl border-2 px-3 py-1.5 text-sm font-semibold ${
                    tab === t.status ? "border-brand bg-brand-soft text-brand" : "border-line bg-surface"
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>

            {terms === null ? (
              <ApruviLoader label="Cargando…" />
            ) : terms.length === 0 ? (
              <p className="rounded-2xl border border-dashed border-line p-6 text-center text-muted">
                No hay términos en este estado.
              </p>
            ) : (
              <fieldset disabled={busy} className="space-y-3">
                <div className="flex flex-wrap items-center gap-2">
                  <label className="flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={allSelected}
                      onChange={() => setSelected(allSelected ? new Set() : new Set(terms.map((t) => t.id)))}
                    />
                    Seleccionar todos ({terms.length})
                  </label>
                  {next ? (
                    <button
                      type="button"
                      onClick={() => bulk(next.action)}
                      disabled={!selected.size}
                      className={`!py-1.5 ${buttonStyles.primary}`}
                    >
                      {`${next.label} (${selected.size})`}
                    </button>
                  ) : null}
                  {tab !== "retired" ? (
                    <button
                      type="button"
                      onClick={() => bulk("retire")}
                      disabled={!selected.size}
                      className={`!py-1.5 ${buttonStyles.secondary}`}
                    >
                      {`Retirar (${selected.size})`}
                    </button>
                  ) : null}
                </div>
                <ul className="divide-y divide-line rounded-2xl border border-line bg-surface" aria-label="Términos">
                  {terms.map((t) => (
                    <li key={t.id} className="flex gap-3 p-3">
                      <input
                        type="checkbox"
                        aria-label={`Seleccionar ${t.term}`}
                        checked={selected.has(t.id)}
                        onChange={() => {
                          const copy = new Set(selected);
                          if (copy.has(t.id)) copy.delete(t.id);
                          else copy.add(t.id);
                          setSelected(copy);
                        }}
                        className="mt-1"
                      />
                      <div className="min-w-0">
                        <p className="font-semibold">
                          {t.term} <span className="text-sm font-normal text-muted">· {t.subject}</span>
                        </p>
                        <p className="text-sm">{t.definition}</p>
                        <p className="text-xs text-muted">
                          {t.source} · cargó {t.mine ? "tú" : t.author}
                        </p>
                      </div>
                    </li>
                  ))}
                </ul>
              </fieldset>
            )}
          </>
        )}
      </main>
    </div>
  );
}
