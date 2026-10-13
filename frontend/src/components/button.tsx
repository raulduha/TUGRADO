import Link from "next/link";

// Estilos de botón compartidos: un solo lugar para el aspecto de las acciones principales.
const BASE =
  "flex items-center justify-center rounded-xl px-5 py-2.5 text-center font-semibold transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand disabled:cursor-not-allowed disabled:opacity-60";

export const buttonStyles = {
  primary: `${BASE} bg-brand text-on-brand shadow-sm hover:bg-brand-strong`,
  secondary: `${BASE} border border-line bg-surface hover:border-brand`,
} as const;

export function ButtonLink({
  href,
  children,
  variant = "primary",
  className = "",
}: {
  href: string;
  children: string;
  variant?: keyof typeof buttonStyles;
  className?: string;
}) {
  return (
    <Link href={href} className={`${buttonStyles[variant]} ${className}`}>
      {children}
    </Link>
  );
}
