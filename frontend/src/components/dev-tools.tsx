"use client";

import { useState } from "react";

import { type DevSim, setDevSim } from "@/lib/devsim";

const PRESETS: Array<{ label: string; percent: number; streak: number }> = [
  { label: "Nuevo", percent: 0, streak: 1 },
  { label: "A mitad de camino", percent: 50, streak: 12 },
  { label: "Listo para el examen", percent: 100, streak: 45 },
];

/** Panel flotante para administradores: simula el avance de un estudiante en la propia vista
 * para recorrer el journey completo. No guarda nada en el servidor. */
export function DevTools({ sim }: { sim: DevSim }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-6 left-4 z-40 flex flex-col items-start gap-2">
      {open ? (
        <section
          aria-label="Herramientas de administrador"
          className="pop-in w-72 space-y-4 rounded-2xl border border-line bg-surface p-4 shadow-xl"
        >
          <div className="flex items-center justify-between">
            <h2 className="font-semibold">Simular estudiante</h2>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={sim.enabled}
                onChange={(e) => setDevSim({ ...sim, enabled: e.target.checked })}
                className="h-4 w-4 accent-[var(--brand)]"
              />
              Activa
            </label>
          </div>
          <label className="block text-sm">
            <span className="flex justify-between font-medium">
              Avance del mapa <span>{sim.percent} %</span>
            </span>
            <input
              type="range"
              min={0}
              max={100}
              step={5}
              value={sim.percent}
              onChange={(e) => setDevSim({ ...sim, enabled: true, percent: Number(e.target.value) })}
              className="mt-1 w-full accent-[var(--brand)]"
              aria-label="Avance del mapa"
            />
          </label>
          <label className="block text-sm">
            <span className="flex justify-between font-medium">
              Días de racha <span>{sim.streak}</span>
            </span>
            <input
              type="range"
              min={0}
              max={60}
              value={sim.streak}
              onChange={(e) => setDevSim({ ...sim, enabled: true, streak: Number(e.target.value) })}
              className="mt-1 w-full accent-[var(--accent)]"
              aria-label="Días de racha"
            />
          </label>
          <div className="flex flex-wrap gap-2">
            {PRESETS.map((p) => (
              <button
                key={p.label}
                type="button"
                onClick={() => setDevSim({ enabled: true, percent: p.percent, streak: p.streak })}
                className="rounded-full border border-line px-3 py-1 text-xs font-semibold hover:border-brand"
              >
                {p.label}
              </button>
            ))}
          </div>
          <p className="text-xs text-muted">
            Solo cambia tu vista, en este navegador. No guarda datos ni lo ven los estudiantes.
          </p>
        </section>
      ) : null}
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-label="Herramientas de administrador"
        className={`flex h-12 w-12 items-center justify-center rounded-full shadow-lg transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand ${
          sim.enabled ? "bg-accent text-foreground" : "bg-foreground text-white"
        }`}
      >
        <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4 2.5-2.5Z" />
        </svg>
      </button>
    </div>
  );
}

/** Aviso visible mientras la simulación está activa. */
export function DevSimBanner({ sim }: { sim: DevSim }) {
  if (!sim.enabled) return null;
  return (
    <p className="rounded-2xl border border-accent bg-accent-soft px-4 py-2 text-sm">
      <span className="font-semibold">Modo simulación (solo tú lo ves):</span> estudiante con{" "}
      {sim.percent} % del mapa y {sim.streak} días de racha.
    </p>
  );
}
