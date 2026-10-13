"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { api, type Me } from "@/lib/api";

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
