import Link from "next/link";
import type { ReactNode } from "react";

import { Logo } from "@/components/illustrations";
import { LEGAL } from "@/lib/legal";

export function LegalPage({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="flex flex-1 flex-col">
      <header className="mx-auto flex w-full max-w-3xl items-center justify-between px-4 py-5">
        <Link href="/" className="rounded-lg focus-visible:outline-2 focus-visible:outline-brand">
          <Logo />
        </Link>
      </header>
      <main className="mx-auto w-full max-w-3xl flex-1 px-4 pb-16">
        <article className="rounded-2xl border border-line bg-surface p-6 sm:p-10">
          <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
          <p className="mt-2 text-sm text-muted">Última actualización: {LEGAL.updatedAt}</p>
          <div className="mt-8 space-y-6 leading-relaxed [&_h2]:mt-10 [&_h2]:text-xl [&_h2]:font-semibold [&_li]:ml-5 [&_li]:list-disc [&_li]:pl-1 [&_ul]:space-y-2">
            {children}
          </div>
        </article>
      </main>
    </div>
  );
}

export function LegalLinks({ className = "" }: { className?: string }) {
  return (
    <nav aria-label="Información legal" className={`flex flex-wrap gap-x-4 gap-y-1 text-xs ${className}`}>
      <Link href="/privacidad" className="hover:underline">
        Privacidad
      </Link>
      <Link href="/terminos" className="hover:underline">
        Términos
      </Link>
      <span>© {LEGAL.owner}</span>
    </nav>
  );
}
