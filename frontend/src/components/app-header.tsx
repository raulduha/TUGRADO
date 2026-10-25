"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { Logo, LogoMark } from "@/components/illustrations";
import { api, type Me } from "@/lib/api";

/** Encabezado de las páginas con sesión. `onLoggedOut` limpia el estado de la página: con Cache
 * Components las páginas se conservan (Activity) y no deben mostrar al usuario anterior. */
export function AppHeader({ me, onLoggedOut }: { me: Me | null; onLoggedOut?: () => void }) {
  const router = useRouter();

  async function logout() {
    await api("/auth/logout", { method: "POST" });
    onLoggedOut?.();
    router.replace("/iniciar-sesion");
  }

  return (
    <header className="border-b border-line bg-surface">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
        {/* En celular, solo el ícono: así caben los enlaces sin desplazar la página. */}
        <Link
          href="/panel"
          aria-label="Aprueba tu examen: ir al panel"
          className="flex-none rounded-lg focus-visible:outline-2 focus-visible:outline-brand"
        >
          <LogoMark className="h-8 w-8 sm:hidden" />
          <span className="hidden sm:block">
            <Logo />
          </span>
        </Link>
        {me ? (
          <div className="flex min-w-0 items-center gap-2 sm:gap-3">
            <span className="hidden truncate text-sm text-muted md:inline">{me.email}</span>
            <Link href="/ruta" className="hidden whitespace-nowrap text-sm font-medium text-brand hover:underline sm:inline">
              Mi ruta
            </Link>
            {me.roles.includes("administrator") ? (
              <Link href="/admin/preguntas" className="whitespace-nowrap text-sm font-medium text-brand hover:underline">
                Preguntas
              </Link>
            ) : null}
            <Link href="/suscripcion" className="whitespace-nowrap text-sm font-medium text-brand hover:underline">
              Suscripción
            </Link>
            <button
              type="button"
              onClick={logout}
              className="whitespace-nowrap rounded-lg border border-line px-2.5 py-1.5 text-sm font-medium hover:border-brand focus-visible:outline-2 focus-visible:outline-brand sm:px-3"
            >
              Cerrar sesión
            </button>
          </div>
        ) : null}
      </div>
    </header>
  );
}
