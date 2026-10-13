/** Apruvi, la mascota de Aprueba tu examen: una bolita azul con birrete que acompaña al
 * estudiante por el mapa. Respira, parpadea y mece la borla (animaciones en globals.css,
 * desactivadas con `prefers-reduced-motion`). */
export function Apruvi({ className = "h-24 w-24" }: { className?: string }) {
  return (
    <svg viewBox="0 0 120 130" className={className} aria-hidden="true">
      {/* Sombra en el suelo: se achica un poco al inhalar. */}
      <ellipse className="apruvi-shadow" cx="60" cy="122" rx="30" ry="5" fill="var(--foreground)" opacity=".12" />

      <g className="apruvi-breathe">
        {/* Pies */}
        <ellipse cx="46" cy="116" rx="9" ry="5" fill="var(--brand-strong)" />
        <ellipse cx="74" cy="116" rx="9" ry="5" fill="var(--brand-strong)" />

        {/* Cuerpo y guatita */}
        <path
          d="M60 38c24 0 38 18 38 42 0 22-16 36-38 36S22 102 22 80c0-24 14-42 38-42Z"
          fill="var(--brand)"
        />
        <ellipse cx="60" cy="90" rx="22" ry="19" fill="#ffffff" opacity=".9" />

        {/* Bracitos */}
        <path d="M24 82c-7 2-10 8-8 13" stroke="var(--brand)" strokeWidth="8" strokeLinecap="round" fill="none" />
        <path d="M96 82c7 2 10 8 8 13" stroke="var(--brand)" strokeWidth="8" strokeLinecap="round" fill="none" />

        {/* Ojos con brillo */}
        <g className="apruvi-blink">
          <ellipse cx="47" cy="66" rx="9" ry="10.5" fill="#ffffff" />
          <ellipse cx="73" cy="66" rx="9" ry="10.5" fill="#ffffff" />
          <circle cx="48.5" cy="68" r="5.5" fill="var(--foreground)" />
          <circle cx="71.5" cy="68" r="5.5" fill="var(--foreground)" />
          <circle cx="50.5" cy="65.5" r="2" fill="#ffffff" />
          <circle cx="73.5" cy="65.5" r="2" fill="#ffffff" />
        </g>

        {/* Mejillas y sonrisa */}
        <ellipse cx="37" cy="78" rx="5.5" ry="3.5" fill="#f7a8b8" opacity=".9" />
        <ellipse cx="83" cy="78" rx="5.5" ry="3.5" fill="#f7a8b8" opacity=".9" />
        <path d="M53 79c3.5 4 10.5 4 14 0" stroke="var(--foreground)" strokeWidth="2.6" strokeLinecap="round" fill="none" />

        {/* Birrete */}
        <path d="M60 14 26 28l34 14 34-14-34-14Z" fill="#1f2a4d" />
        <path d="M40 34v8c0 4 9 7 20 7s20-3 20-7v-8l-20 8-20-8Z" fill="#2b3864" />
        <g className="apruvi-tassel">
          <path d="M88 30v14" stroke="var(--accent)" strokeWidth="2.4" strokeLinecap="round" />
          <circle cx="88" cy="46" r="3.6" fill="var(--accent)" />
        </g>
        <circle cx="60" cy="28" r="2.4" fill="var(--accent)" />
      </g>
    </svg>
  );
}
