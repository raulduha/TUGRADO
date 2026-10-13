"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";

import { Logo } from "@/components/illustrations";
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
        <Link href="/panel" className="rounded-lg focus-visible:outline-2 focus-visible:outline-brand">
          <Logo />
        </Link>
        {me ? (
          <div className="flex min-w-0 items-center gap-3">
            <span className="hidden truncate text-sm text-muted md:inline">{me.email}</span>
            <Link href="/suscripcion" className="text-sm font-medium text-brand hover:underline">
              Suscripción
            </Link>
            <button
              type="button"
              onClick={logout}
              className="rounded-lg border border-line px-3 py-1.5 text-sm font-medium hover:border-brand focus-visible:outline-2 focus-visible:outline-brand"
            >
              Cerrar sesión
            </button>
          </div>
        ) : null}
      </div>
    </header>
  );
}
