// Preguntas de EJEMPLO para el mockup de la práctica (FR-006). No es contenido revisado ni
// publicado: se reemplaza por el banco real (importador + revisión + publicación, FR-013/014)
// cuando estén las preguntas y las decisiones de dificultad, materias y número de alternativas.

export type SampleQuestion = {
  id: string;
  subject: string;
  prompt: string;
  options: string[];
  correct: number;
  explanation: string;
  source: string;
};

export const SAMPLE_QUESTIONS: SampleQuestion[] = [
  {
    id: "q1",
    subject: "Derecho Civil",
    prompt: "¿Cuándo principia la existencia legal de una persona?",
    options: [
      "Desde la concepción",
      "Al nacer, esto es, al separarse completamente de su madre",
      "Al inscribirse en el Registro Civil",
      "A las 24 horas de nacida",
    ],
    correct: 1,
    explanation:
      "La existencia legal principia al nacimiento, es decir, al separarse completamente de la madre.",
    source: "Código Civil, art. 74",
  },
  {
    id: "q2",
    subject: "Derecho Civil",
    prompt: "Según el Código Civil, ¿cuándo constituye derecho la costumbre?",
    options: [
      "Siempre, igual que la ley",
      "Nunca",
      "Solo en los casos en que la ley se remite a ella",
      "Cuando la acepta un juez de letras",
    ],
    correct: 2,
    explanation:
      "La costumbre no constituye derecho sino en los casos en que la ley se remite a ella.",
    source: "Código Civil, art. 2",
  },
  {
    id: "q3",
    subject: "Derecho Civil",
    prompt: "¿A qué edad se alcanza la mayoría de edad en Chile?",
    options: ["16 años", "18 años", "20 años", "21 años"],
    correct: 1,
    explanation: "Es mayor de edad quien ha cumplido dieciocho años.",
    source: "Código Civil, art. 26",
  },
  {
    id: "q4",
    subject: "Derecho Constitucional",
    prompt: "¿Cuánto dura el mandato del Presidente de la República?",
    options: [
      "4 años, sin reelección para el período siguiente",
      "4 años, con reelección inmediata",
      "6 años, sin reelección",
      "5 años, con una reelección",
    ],
    correct: 0,
    explanation:
      "El Presidente dura cuatro años en el ejercicio de sus funciones y no puede ser reelegido para el período siguiente.",
    source: "Constitución Política de la República, art. 25",
  },
  {
    id: "q5",
    subject: "Derecho Civil",
    prompt: "¿Desde cuándo obliga la ley, por regla general?",
    options: [
      "Desde que la aprueba el Congreso",
      "Desde su promulgación",
      "Desde su publicación en el Diario Oficial",
      "Treinta días después de su promulgación",
    ],
    correct: 2,
    explanation:
      "La ley no obliga sino una vez promulgada y publicada; desde la fecha de su publicación en el Diario Oficial se entiende conocida de todos.",
    source: "Código Civil, arts. 6 y 7",
  },
];
