/** Estrellas de una lección (0 a 3). `className` ubica la fila; `starClassName`, el tamaño. */
export function Stars({
  count,
  className = "",
  starClassName = "h-4 w-4",
}: {
  count: number;
  className?: string;
  starClassName?: string;
}) {
  return (
    <span className={`flex ${className}`} aria-label={`${count} de 3 estrellas`} role="img">
      {[0, 1, 2].map((i) => (
        <svg key={i} viewBox="0 0 24 24" className={`${starClassName} ${i < count ? "text-accent" : "text-line"}`} aria-hidden="true">
          <path
            fill="currentColor"
            d="m12 2.5 2.9 6 6.6.8-4.9 4.6 1.3 6.6L12 17.2l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8z"
          />
        </svg>
      ))}
    </span>
  );
}
