"use client";

import { useSyncExternalStore } from "react";

// Herramientas de admin: "simular estudiante". Solo cambia lo que el administrador ve en su
// navegador (localStorage); no toca la base de datos ni lo ven los estudiantes.

export type DevSim = { enabled: boolean; percent: number; streak: number };

const KEY = "tugrado.devsim";
const EVENT = "tugrado-devsim";
const OFF: DevSim = { enabled: false, percent: 0, streak: 0 };

let cachedRaw: string | null = null;
let cached: DevSim = OFF;

function read(): DevSim {
  let raw: string | null = null;
  try {
    raw = window.localStorage.getItem(KEY);
  } catch {
    return OFF;
  }
  if (raw === cachedRaw) return cached;
  cachedRaw = raw;
  try {
    const parsed = raw ? (JSON.parse(raw) as Partial<DevSim>) : {};
    cached = {
      enabled: parsed.enabled === true,
      percent: Math.min(100, Math.max(0, Number(parsed.percent) || 0)),
      streak: Math.min(365, Math.max(0, Number(parsed.streak) || 0)),
    };
  } catch {
    cached = OFF;
  }
  return cached;
}

function subscribe(callback: () => void): () => void {
  window.addEventListener(EVENT, callback);
  window.addEventListener("storage", callback);
  return () => {
    window.removeEventListener(EVENT, callback);
    window.removeEventListener("storage", callback);
  };
}

export function setDevSim(next: DevSim): void {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(next));
  } catch {
    // Sin almacenamiento (modo privado): la simulación no se guarda.
  }
  window.dispatchEvent(new Event(EVENT));
}

/** Estado de la simulación; `isAdmin` falso la desactiva siempre. */
export function useDevSim(isAdmin: boolean): DevSim {
  const sim = useSyncExternalStore(subscribe, read, () => OFF);
  return isAdmin ? sim : OFF;
}
