import Link from "next/link";

import { ButtonLink } from "@/components/button";
import { LegalLinks } from "@/components/legal-page";
import { HeroIllustration, Icon, type IconName, Logo } from "@/components/illustrations";

const ROUTE: Array<{ icon: IconName; title: string; text: string }> = [
  {
    icon: "list",
    title: "Elige qué estudiar",
    text: "Tu programa completo, una materia o solo los subtemas que quieras reforzar.",
  },
  {
    icon: "book",
    title: "Practica",
    text: "Preguntas de alternativas revisadas, con la respuesta correcta y su explicación.",
  },
  {
    icon: "mic",
    title: "Simula el examen oral",
    text: "Responde por voz o por texto, con tiempos como en la comisión.",
  },
  {
    icon: "calendar",
    title: "Sigue tu plan",
    text: "Un plan hasta la fecha de tu examen que se ajusta a cómo vas avanzando.",
  },
];

export default function Home() {
  return (
    <div className="flex flex-1 flex-col">
      <header className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-5">
        <Logo />
        <Link href="/iniciar-sesion" className="text-sm font-semibold text-brand hover:underline">
          Iniciar sesión
        </Link>
      </header>

      <main className="flex-1">
        <section className="relative">
          {/* Formas de color suaves de fondo (decorativas). */}
          <div aria-hidden="true" className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
            <div className="absolute -left-24 top-10 h-72 w-72 rounded-full bg-brand-soft blur-3xl" />
            <div className="absolute -right-16 top-32 h-64 w-64 rounded-full bg-accent-soft blur-3xl" />
          </div>
          <div className="mx-auto grid max-w-6xl items-center gap-10 px-4 pb-16 pt-6 md:grid-cols-2 md:pt-12">
          <div>
            <p className="inline-flex items-center gap-2 rounded-full bg-brand-soft px-3 py-1 text-sm font-medium text-brand">
              <Icon name="target" className="h-4 w-4" />
              Examen de grado de Derecho
            </p>
            <h1 className="mt-5 text-4xl font-semibold tracking-tight text-balance sm:text-5xl">
              Llega a tu examen de grado con confianza
            </h1>
            <p className="mt-5 text-lg text-muted text-pretty">
              Practica con preguntas revisadas, simula el examen oral con tiempos reales y sigue
              un plan de estudio que se ajusta a tu avance.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <ButtonLink href="/registro" className="py-3">
                Crear cuenta gratis
              </ButtonLink>
              <ButtonLink href="/iniciar-sesion" variant="secondary" className="py-3">
                Ya tengo cuenta
              </ButtonLink>
            </div>
          </div>
          <HeroIllustration className="mx-auto w-full max-w-md" />
          </div>
        </section>

        <section className="border-y border-line bg-surface">
          <div className="mx-auto max-w-6xl px-4 py-16">
            <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">Tu ruta al examen</h2>
            <p className="mt-2 text-muted">Cuatro pasos, a tu ritmo.</p>
            <ol className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {ROUTE.map((step, index) => (
                <li
                  key={step.title}
                  className="rounded-2xl border border-line bg-background p-6 transition hover:-translate-y-0.5 hover:shadow-md"
                >
                  <div className="flex items-center gap-3">
                    <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-soft text-brand">
                      <Icon name={step.icon} />
                    </span>
                    <span className="text-sm font-semibold text-muted">Paso {index + 1}</span>
                  </div>
                  <h3 className="mt-4 text-lg font-semibold">{step.title}</h3>
                  <p className="mt-1 text-sm text-muted">{step.text}</p>
                </li>
              ))}
            </ol>
          </div>
        </section>
      </main>

      <footer className="mx-auto w-full max-w-6xl space-y-2 px-4 py-8 text-xs text-muted">
        <p>
          Las evaluaciones son orientativas: no son una calificación oficial ni garantizan la
          aprobación del examen.
        </p>
        <LegalLinks />
      </footer>
    </div>
  );
}
