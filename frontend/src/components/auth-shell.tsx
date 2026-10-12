import Link from "next/link";
import type { ReactNode } from "react";

import { Icon, Logo, PathIllustration } from "@/components/illustrations";

const BENEFITS = [
  "Preguntas revisadas por personas, con su explicación",
  "Simulación oral con tiempos reales",
  "Un plan que se ajusta a tu avance",
];

export function AuthShell({
  title,
  description,
  children,
  footer,
}: {
  title: string;
  description?: ReactNode;
  children: ReactNode;
  footer?: ReactNode;
}) {
  return (
    <div className="flex flex-1">
      {/* Panel ilustrado: solo en pantallas grandes, para no empujar el formulario en móvil. */}
      <aside className="relative hidden w-[42%] flex-col justify-between overflow-hidden bg-brand p-10 text-on-brand lg:flex">
        <Link href="/" className="rounded-lg focus-visible:outline-2 focus-visible:outline-on-brand">
          <span className="inline-flex items-center gap-2 text-lg font-semibold tracking-tight">
            TUGRADO
          </span>
        </Link>
        <div>
          <PathIllustration className="w-full max-w-sm" />
          <p className="mt-8 text-3xl font-semibold leading-tight tracking-tight">
            Paso a paso, hasta tu examen de grado.
          </p>
          <ul className="mt-6 space-y-3">
            {BENEFITS.map((benefit) => (
              <li key={benefit} className="flex items-start gap-3 opacity-90">
                <span className="mt-0.5 flex h-5 w-5 flex-none items-center justify-center rounded-full bg-on-brand/20">
                  <Icon name="check" className="h-3.5 w-3.5" />
                </span>
                {benefit}
              </li>
            ))}
          </ul>
        </div>
        <p className="text-xs opacity-75">
          Orientativo: no es una calificación oficial ni garantiza la aprobación.
        </p>
      </aside>

      <main className="flex flex-1 items-start justify-center px-4 py-10 sm:items-center sm:py-16">
        <div className="w-full max-w-md">
          <Link
            href="/"
            className="mb-8 inline-block rounded-lg focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand lg:hidden"
          >
            <Logo />
          </Link>
          <div className="rounded-2xl border border-line bg-surface p-6 shadow-sm sm:p-8">
            <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
            {description ? <div className="mt-2 text-sm text-muted">{description}</div> : null}
            <div className="mt-6">{children}</div>
          </div>
          {footer ? <div className="mt-6 text-center text-sm text-muted">{footer}</div> : null}
        </div>
      </main>
    </div>
  );
}
