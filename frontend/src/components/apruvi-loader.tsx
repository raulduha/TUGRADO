"use client";

import { useEffect, useState } from "react";

import { Apruvi } from "@/components/apruvi";

const TIPS = [
  "Ordenando tus apuntes…",
  "Afilando el lápiz…",
  "Repasando tu mapa de estudio…",
  "Calentando la voz para el oral…",
];

/** Pantalla de carga con Apruvi saltando sobre su sombra y frases que van rotando. */
export function ApruviLoader({ label }: { label: string }) {
  const [tip, setTip] = useState(0);
  useEffect(() => {
    const id = window.setInterval(() => setTip((t) => (t + 1) % TIPS.length), 1800);
    return () => window.clearInterval(id);
  }, []);

  return (
    <div role="status" className="flex flex-col items-center justify-center gap-4 py-16 text-center">
      <span className="sr-only">{label}</span>
      <div className="relative h-32 w-28" aria-hidden="true">
        <div className="apruvi-hop absolute inset-x-0 top-0">
          <Apruvi className="h-28 w-28" shadow={false} />
        </div>
        <div className="apruvi-hop-shadow absolute bottom-0 left-1/2 h-2.5 w-16 -translate-x-1/2 rounded-full bg-foreground/15" />
      </div>
      <div className="flex gap-1.5" aria-hidden="true">
        <span className="loader-dot h-2 w-2 rounded-full bg-brand" />
        <span className="loader-dot h-2 w-2 rounded-full bg-brand [animation-delay:150ms]" />
        <span className="loader-dot h-2 w-2 rounded-full bg-brand [animation-delay:300ms]" />
      </div>
      <p className="font-semibold">{label}</p>
      <p key={tip} className="loader-tip text-sm text-muted" aria-hidden="true">
        {TIPS[tip]}
      </p>
    </div>
  );
}
