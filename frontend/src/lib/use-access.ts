"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { api, type Subscription } from "@/lib/api";
import { useRequireUser } from "@/lib/use-user";

/** Sesión + acceso al estudio (suscripción, cortesía o administrador). Sin acceso lleva a
 * /suscripcion; el backend decide en cada visita. */
export function useStudyAccess(next: string) {
  const router = useRouter();
  const user = useRequireUser(next);
  const [hasAccess, setHasAccess] = useState(false);

  useEffect(() => {
    if (!user.me) return;
    let cancelled = false;
    api<Subscription>("/billing/subscription").then((result) => {
      if (cancelled || !result.ok) return;
      if (result.data.has_access) setHasAccess(true);
      else router.replace("/suscripcion");
    });
    return () => {
      cancelled = true;
    };
  }, [user.me, router]);

  return { ...user, hasAccess };
}
