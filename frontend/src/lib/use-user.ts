"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { api, type Me } from "@/lib/api";

/** Si la cuenta tiene el rol de administrador. La autorización real la decide el backend. */
export function isAdministrator(me: Me | null): boolean {
  return me?.roles.includes("administrator") ?? false;
}

/** Usuario con sesión. Sin sesión válida (401) redirige a iniciar sesión y vuelve a `next`. */
export function useRequireUser(next: string) {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api<Me>("/auth/me").then((result) => {
      if (cancelled) return;
      if (result.ok) setMe(result.data);
      else if (result.status === 401) router.replace(`/iniciar-sesion?next=${encodeURIComponent(next)}`);
      else setError(result.error.message);
    });
    return () => {
      cancelled = true;
    };
  }, [router, next]);

  return { me, setMe, error };
}
