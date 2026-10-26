"use client";

import { useEffect, useState } from "react";

import { Alert } from "@/components/alert";
import { buttonStyles } from "@/components/button";
import { api, type Ranking } from "@/lib/api";

const SHOWN = 5;

/** Ranking mensual voluntario (FR-039): solo quien se inscribe con un apodo, y solo se muestra
 * el apodo. Mide la práctica del mes, no promete aprobar el examen. */
export function RankingCard() {
  const [ranking, setRanking] = useState<Ranking | null>(null);
  const [alias, setAlias] = useState("");
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [reload, setReload] = useState(0);

  useEffect(() => {
    let cancelled = false;
    api<Ranking>("/engagement/ranking").then((result) => {
      if (!cancelled && result.ok) setRanking(result.data);
    });
    return () => {
      cancelled = true;
    };
  }, [reload]);

  async function join(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    const result = await api("/engagement/ranking/profile", { method: "PUT", body: { alias } });
    setBusy(false);
    if (!result.ok) return setError(result.error.message);
    setEditing(false);
    setReload((n) => n + 1);
  }

  async function leave() {
    setBusy(true);
    await api("/engagement/ranking/profile", { method: "DELETE" });
    setBusy(false);
    setReload((n) => n + 1);
  }

  if (!ranking) return null;
  const joined = ranking.alias !== null;
  const top = ranking.entries.slice(0, SHOWN);
  const meOutside = ranking.me && ranking.me.position > SHOWN ? ranking.me : null;

  return (
    <section aria-label="Ranking del mes" className="rounded-3xl border border-line bg-surface p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="font-semibold">Ranking del mes</h2>
          <p className="text-sm text-muted">Por experiencia ganada este mes. Participar es voluntario.</p>
        </div>
        {joined && !editing ? (
          <button type="button" onClick={leave} disabled={busy} className="text-sm font-semibold text-muted hover:underline">
            Salir
          </button>
        ) : null}
      </div>

      {top.length > 0 ? (
        <ol className="mt-3 space-y-1.5">
          {top.map((e) => (
            <li
              key={e.position}
              className={`flex justify-between rounded-xl px-3 py-1.5 text-sm ${e.me ? "bg-brand-soft font-semibold text-brand" : ""}`}
            >
              <span>
                {e.position}. {e.alias}
              </span>
              <span>{e.xp} XP</span>
            </li>
          ))}
          {meOutside ? (
            <li className="flex justify-between rounded-xl bg-brand-soft px-3 py-1.5 text-sm font-semibold text-brand">
              <span>
                {meOutside.position}. {meOutside.alias}
              </span>
              <span>{meOutside.xp} XP</span>
            </li>
          ) : null}
        </ol>
      ) : (
        <p className="mt-3 text-sm text-muted">Todavía nadie se ha inscrito este mes.</p>
      )}

      {!joined || editing ? (
        <form onSubmit={join} className="mt-4 space-y-2">
          {error ? <Alert tone="error">{error}</Alert> : null}
          <div className="flex gap-2">
            <input
              value={alias}
              onChange={(e) => setAlias(e.target.value)}
              aria-label="Tu apodo para el ranking"
              placeholder="Tu apodo (no uses tu nombre si no quieres)"
              maxLength={24}
              className="min-w-0 flex-1 rounded-xl border border-line bg-surface px-3 py-2 text-sm"
            />
            <button type="submit" disabled={busy || alias.trim().length < 3} className={`!px-4 ${buttonStyles.primary}`}>
              Unirme
            </button>
          </div>
        </form>
      ) : null}
    </section>
  );
}
