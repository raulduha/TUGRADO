"use client";

import { useEffect, useState } from "react";

import { api, type StudyPath } from "@/lib/api";

/** Materias con preguntas publicadas (las unidades de la ruta), para elegir qué practicar. */
export function useSubjects(enabled: boolean): string[] | null {
  const [subjects, setSubjects] = useState<string[] | null>(null);

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    api<StudyPath>("/practice/path").then((result) => {
      if (!cancelled) setSubjects(result.ok ? result.data.units.map((u) => u.subject) : []);
    });
    return () => {
      cancelled = true;
    };
  }, [enabled]);

  return subjects;
}
