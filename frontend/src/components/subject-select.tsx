/** Selector de materia de la prueba, las flashcards y el rosco. "" significa todas. */
export function SubjectSelect({
  subjects,
  value,
  onChange,
}: {
  subjects: string[];
  value: string;
  onChange: (subject: string) => void;
}) {
  return (
    <label className="block">
      <span className="text-sm font-semibold">Materia</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 block w-full rounded-xl border border-line bg-surface px-3 py-2"
      >
        <option value="">Todas las materias</option>
        {subjects.map((name) => (
          <option key={name} value={name}>
            {name}
          </option>
        ))}
      </select>
    </label>
  );
}
