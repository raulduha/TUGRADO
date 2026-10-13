// Ilustraciones propias en SVG: sin archivos externos y con los colores del tema (claro/oscuro).
// Son decorativas: aria-hidden, el texto de la página lleva la información.

type Props = { className?: string };

export function LogoMark({ className }: Props) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden="true">
      <rect width="32" height="32" rx="9" fill="var(--brand)" />
      {/* Birrete de graduación */}
      <path d="M16 8 5 13l11 5 11-5-11-5Z" fill="var(--on-brand)" />
      <path
        d="M9.5 15.2v4.6c0 1.6 2.9 3.2 6.5 3.2s6.5-1.6 6.5-3.2v-4.6L16 18.1l-6.5-2.9Z"
        fill="var(--on-brand)"
        opacity=".85"
      />
      <path d="M26 13.5v5.5" stroke="var(--on-brand)" strokeWidth="1.6" strokeLinecap="round" />
      <circle cx="26" cy="20" r="1.4" fill="var(--accent)" />
    </svg>
  );
}

export function Logo({ className = "" }: Props) {
  return (
    <span className={`inline-flex items-center gap-2 ${className}`}>
      <LogoMark className="h-8 w-8" />
      <span className="text-lg font-semibold tracking-tight">Aprueba tu examen</span>
    </span>
  );
}

/** Estudiante con libros, balanza y burbuja de voz: práctica + simulación oral. */
export function HeroIllustration({ className }: Props) {
  return (
    <svg viewBox="0 0 420 340" className={className} aria-hidden="true">
      <circle cx="210" cy="175" r="150" fill="var(--brand)" opacity=".08" />
      <circle cx="330" cy="70" r="38" fill="var(--accent)" opacity=".25" />
      <circle cx="70" cy="270" r="26" fill="var(--success)" opacity=".2" />

      {/* Libros */}
      <rect x="70" y="232" width="150" height="26" rx="6" fill="var(--brand)" />
      <rect x="82" y="206" width="132" height="26" rx="6" fill="var(--accent)" />
      <rect x="64" y="180" width="140" height="26" rx="6" fill="var(--surface)" stroke="var(--line)" strokeWidth="2" />
      <path d="M80 193h80M96 219h70M86 245h96" stroke="var(--on-brand)" strokeWidth="3" strokeLinecap="round" opacity=".5" />
      <path d="M80 193h80" stroke="var(--muted)" strokeWidth="3" strokeLinecap="round" opacity=".5" />

      {/* Balanza */}
      <path d="M300 130v118" stroke="var(--foreground)" strokeWidth="5" strokeLinecap="round" />
      <path d="M262 248h76" stroke="var(--foreground)" strokeWidth="6" strokeLinecap="round" />
      <path d="M250 150h100" stroke="var(--foreground)" strokeWidth="5" strokeLinecap="round" />
      <circle cx="300" cy="128" r="9" fill="var(--accent)" />
      <path d="M250 150 236 190M250 150l14 40M350 150l-14 40M350 150l14 40" stroke="var(--muted)" strokeWidth="2" />
      <path d="M230 190a20 9 0 0 0 40 0Z" fill="var(--brand)" />
      <path d="M330 190a20 9 0 0 0 40 0Z" fill="var(--brand)" />

      {/* Burbuja de voz con onda */}
      <rect x="120" y="58" width="150" height="76" rx="22" fill="var(--surface)" stroke="var(--line)" strokeWidth="2" />
      <path d="m150 132-8 22 26-20Z" fill="var(--surface)" stroke="var(--line)" strokeWidth="2" strokeLinejoin="round" />
      <path d="M150 128h22" stroke="var(--surface)" strokeWidth="4" />
      <g stroke="var(--brand)" strokeWidth="6" strokeLinecap="round">
        <path d="M152 88v20M168 80v36M184 90v16M200 76v44M216 86v24M232 92v12M248 84v28" />
      </g>

      {/* Marca de verificación */}
      <circle cx="96" cy="112" r="24" fill="var(--success)" />
      <path d="m85 112 7 7 15-15" stroke="#fff" strokeWidth="5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

/** Camino con hitos: la ruta hacia el examen. */
export function PathIllustration({ className }: Props) {
  return (
    <svg viewBox="0 0 320 220" className={className} aria-hidden="true">
      <path
        d="M30 190c60 0 40-70 110-70s60-70 120-70"
        fill="none"
        stroke="var(--on-brand)"
        strokeWidth="6"
        strokeDasharray="2 14"
        strokeLinecap="round"
        opacity=".7"
      />
      <circle cx="30" cy="190" r="14" fill="var(--on-brand)" />
      <circle cx="140" cy="120" r="14" fill="var(--on-brand)" opacity=".85" />
      <circle cx="260" cy="50" r="22" fill="var(--accent)" />
      <path d="M252 40v22M252 41h18l-5 6 5 6h-18" fill="var(--on-brand)" stroke="var(--on-brand)" strokeWidth="2" strokeLinejoin="round" />
      <path d="m24 190 4 4 8-8" stroke="var(--brand)" strokeWidth="3" fill="none" strokeLinecap="round" />
      <path d="m134 120 4 4 8-8" stroke="var(--brand)" strokeWidth="3" fill="none" strokeLinecap="round" />
    </svg>
  );
}

// Íconos de línea (24×24) para tarjetas y pasos.
const ICON_PATHS = {
  check: "m5 12 5 5L20 7",
  mail: "M4 6h16v12H4zM4 7l8 6 8-6",
  user: "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4 20a8 8 0 0 1 16 0",
  book: "M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5ZM8 7h7",
  list: "M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01",
  mic: "M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3ZM19 11a7 7 0 0 1-14 0M12 18v3",
  calendar: "M4 6h16v14H4zM4 10h16M9 3v4M15 3v4",
  target: "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM12 12h.01",
  flame: "M12 21c4 0 7-3 7-7 0-5-5-7-5-11-3 2-4 5-4 7-1-1-2-2-2-4-2 2-3 5-3 8 0 4 3 7 7 7Z",
  clock: "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 7v5l3 2",
  chart: "M4 20V10M10 20V4M16 20v-7M22 20H2",
  lock: "M6 11h12v9H6zM8 11V8a4 4 0 0 1 8 0v3",
  cap: "M12 4 2 9l10 5 10-5-10-5ZM6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5M22 9v5",
  repeat: "M4 12a8 8 0 0 1 14-5.3M20 4v4h-4M20 12a8 8 0 0 1-14 5.3M4 20v-4h4",
} as const;

export type IconName = keyof typeof ICON_PATHS;

export function Icon({ name, className = "h-5 w-5" }: { name: IconName; className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={ICON_PATHS[name]} />
    </svg>
  );
}
