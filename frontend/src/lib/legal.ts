// Datos del responsable del servicio, usados en Privacidad y Términos.
export const LEGAL = {
  owner: "proda.cl",
  legalName: "PRODA SpA" as string | null,
  rut: "78.470.644-3" as string | null,
  contactEmail: "contacto@proda.cl" as string | null,
  updatedAt: "13 de octubre de 2026",
};

export function ownerLabel(): string {
  const parts = [LEGAL.legalName, LEGAL.rut ? `RUT ${LEGAL.rut}` : null].filter(Boolean);
  return parts.length ? `${parts.join(", ")} (${LEGAL.owner})` : LEGAL.owner;
}

export function contactLabel(): string {
  return LEGAL.contactEmail ?? "[correo de contacto pendiente]";
}
