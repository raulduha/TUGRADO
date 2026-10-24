import type { Metadata } from "next";
import Link from "next/link";

import { ButtonLink } from "@/components/button";
import { Icon, Logo } from "@/components/illustrations";
import { CEDULAS, type Cedula, TEMARIO_SOURCE } from "@/lib/temario";

export const metadata: Metadata = {
  title: "Qué entra en el examen de grado",
  description: "Las cédulas del examen de grado de Derecho UC: las obligatorias, las electivas y sus temas.",
};

const FACTS = [
  { icon: "list", title: "Tres cédulas", text: "Derecho Civil y Derecho Procesal, obligatorias, y una electiva a tu elección." },
  { icon: "mic", title: "Examen oral", text: "Una comisión te interroga en cada cédula y luego delibera tu nota." },
  { icon: "target", title: "Acto único", text: "Una vez interrogado en las cédulas, el examen ya no se puede suspender." },
] as const;

/** Guía del examen de grado: el temario oficial de la UC como índice de lo que hay que estudiar. */
export default function TemarioPage() {
  const required = CEDULAS.filter((c) => c.kind === "obligatoria");
  const electives = CEDULAS.filter((c) => c.kind === "electiva");
  const suspended = CEDULAS.filter((c) => c.kind === "suspendida");

  return (
    <div className="flex flex-1 flex-col">
      <header className="mx-auto flex w-full max-w-4xl items-center justify-between gap-4 px-4 py-5">
        <Link href="/" className="rounded-lg focus-visible:outline-2 focus-visible:outline-brand">
          <Logo />
        </Link>
        <Link href="/ruta" className="text-sm font-semibold text-brand hover:underline">
          Ir a mi ruta →
        </Link>
      </header>

      <main className="mx-auto w-full max-w-4xl flex-1 space-y-10 px-4 pb-16">
        <section className="space-y-4">
          <p className="text-sm font-semibold uppercase tracking-wide text-brand">Guía del examen</p>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Qué entra en el examen de grado</h1>
          <p className="max-w-2xl text-muted">
            Este es el temario oficial de la Facultad de Derecho UC, vigente desde abril de 2021. Si
            estudias en otra universidad, revisa también tu propio cedulario: los temas se parecen,
            pero no son idénticos.
          </p>
          <ul className="grid gap-3 sm:grid-cols-3">
            {FACTS.map((fact) => (
              <li key={fact.title} className="rounded-2xl border border-line bg-surface p-4">
                <Icon name={fact.icon} className="h-6 w-6 text-brand" />
                <p className="mt-2 font-semibold">{fact.title}</p>
                <p className="text-sm text-muted">{fact.text}</p>
              </li>
            ))}
          </ul>
        </section>

        <section aria-labelledby="obligatorias" className="space-y-4">
          <h2 id="obligatorias" className="text-2xl font-semibold tracking-tight">
            Cédulas obligatorias
          </h2>
          <div className="grid gap-4 lg:grid-cols-2">
            {required.map((cedula) => (
              <CedulaCard key={cedula.number} cedula={cedula} open />
            ))}
          </div>
        </section>

        <section aria-labelledby="electivas" className="space-y-4">
          <div>
            <h2 id="electivas" className="text-2xl font-semibold tracking-tight">
              Cédulas electivas
            </h2>
            <p className="text-muted">Eliges una. Toca una cédula para ver sus temas.</p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {electives.map((cedula) => (
              <CedulaCard key={cedula.number} cedula={cedula} />
            ))}
          </div>
          {suspended.map((cedula) => (
            <p key={cedula.number} className="text-sm text-muted">
              Cédula {cedula.number}, {cedula.name}: suspendida.
            </p>
          ))}
        </section>

        <section className="flex flex-col items-start gap-4 rounded-3xl border border-line bg-brand-soft p-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold">Practica tema por tema</h2>
            <p className="text-muted">
              Tu ruta de estudio sigue este temario, con lecciones cortas y explicaciones en cada
              respuesta.
            </p>
          </div>
          <ButtonLink href="/ruta" className="whitespace-nowrap">
            Empezar mi ruta
          </ButtonLink>
        </section>

        <p className="text-xs text-muted">
          Fuente:{" "}
          <a href={TEMARIO_SOURCE} className="underline" target="_blank" rel="noreferrer">
            Facultad de Derecho UC, examen de grado
          </a>
          . Es un índice de materias: el detalle de cada cédula está en su PDF oficial. Aprueba tu
          examen no garantiza la aprobación del examen.
        </p>
      </main>
    </div>
  );
}

function CedulaCard({ cedula, open = false }: { cedula: Cedula; open?: boolean }) {
  return (
    <details open={open} className="group rounded-2xl border border-line bg-surface p-5 [&_summary::-webkit-details-marker]:hidden">
      <summary className="flex cursor-pointer list-none items-start gap-3">
        <span className="flex h-9 w-9 flex-none items-center justify-center rounded-full bg-brand text-sm font-bold text-on-brand">
          {cedula.number}
        </span>
        <span className="flex-1">
          <span className="block font-semibold leading-snug">{cedula.name}</span>
          <span className="text-sm text-muted">
            {cedula.chapters.length} {cedula.chapters.length === 1 ? "parte" : "partes"}
          </span>
        </span>
        <span aria-hidden="true" className="text-muted transition group-open:rotate-90">
          ›
        </span>
      </summary>
      <ol className="mt-4 space-y-3 border-t border-line pt-4 text-sm">
        {cedula.chapters.map((chapter) => (
          <li key={chapter.title}>
            <p className="font-medium">{chapter.title}</p>
            {chapter.topics ? (
              <ul className="mt-1 list-disc space-y-0.5 pl-5 text-muted">
                {chapter.topics.map((topic) => (
                  <li key={topic}>{topic}</li>
                ))}
              </ul>
            ) : null}
          </li>
        ))}
      </ol>
      {cedula.pdf ? (
        <a
          href={cedula.pdf}
          target="_blank"
          rel="noreferrer"
          className="mt-4 inline-flex text-sm font-semibold text-brand hover:underline"
        >
          Ver la cédula oficial (PDF) →
        </a>
      ) : null}
    </details>
  );
}
