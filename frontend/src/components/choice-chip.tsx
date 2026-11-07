/** Botón de una opción entre varias (meta diaria, largo de la prueba): marcado con `selected`. */
export function ChoiceChip({
  selected,
  onClick,
  children,
}: {
  selected: boolean;
  onClick: () => void;
  children: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={selected}
      className={`rounded-xl border-2 px-4 py-2 text-sm font-semibold transition ${
        selected ? "border-brand bg-brand-soft text-brand" : "border-line bg-surface hover:border-brand/50"
      }`}
    >
      {children}
    </button>
  );
}
