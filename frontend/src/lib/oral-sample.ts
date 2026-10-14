// Datos de EJEMPLO para el mockup de la simulación oral (FR-007 a FR-009). Ni la pregunta, ni
// la transcripción ni la evaluación vienen de un proveedor de IA: los proveedores son el
// pendiente 3 del README. La escala sí es la decidida: cada criterio de 0 a 100, ponderado
// según la rúbrica y convertido linealmente a 1,0–7,0 con un decimal (AC-034).

export type Criterion = { name: string; weight: number; score: number; comment: string };

export const ORAL_SAMPLE = {
  subject: "Derecho Civil",
  question: "Explique los requisitos de existencia y de validez del acto jurídico.",
  totalMinutes: 20,
  questionSeconds: 180,
  transcript:
    "Los requisitos de existencia son aquellos sin los cuales el acto no nace a la vida del derecho: la voluntad, el objeto, la causa y las solemnidades cuando la ley las exige. Los requisitos de validez, en cambio, permiten que el acto produzca efectos sin vicios: voluntad exenta de vicios, que son el error, la fuerza y el dolo; capacidad de las partes; objeto lícito y causa lícita. El artículo 1445 del Código Civil enumera los requisitos para que una persona se obligue.",
  criteria: [
    {
      name: "Precisión jurídica",
      weight: 40,
      score: 82,
      comment: "Distingue bien existencia y validez y enumera los vicios del consentimiento.",
    },
    {
      name: "Estructura",
      weight: 20,
      score: 75,
      comment: "Orden claro; faltó cerrar con una conclusión breve.",
    },
    {
      name: "Uso de fuentes",
      weight: 20,
      score: 70,
      comment: "Cita el art. 1445; podría mencionar la sanción de nulidad (art. 1681).",
    },
    {
      name: "Claridad oral",
      weight: 20,
      score: 85,
      comment: "Ritmo y vocabulario adecuados.",
    },
  ] satisfies Criterion[],
};

/** Promedio ponderado (0–100) y nota 1,0–7,0 con un decimal. */
export function grade(criteria: Criterion[]): { weighted: number; mark: number } {
  const totalWeight = criteria.reduce((sum, c) => sum + c.weight, 0);
  const weighted = criteria.reduce((sum, c) => sum + c.score * c.weight, 0) / totalWeight;
  const mark = Math.round((1 + (6 * weighted) / 100) * 10) / 10;
  return { weighted, mark };
}
