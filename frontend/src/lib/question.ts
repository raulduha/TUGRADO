/** Letras de las alternativas (el backend acepta de 2 a 5: app/persistence/content_models.py). */
export const LETTERS = "ABCDE";

/** «Materia · subtema», o solo la materia si la pregunta no tiene subtema. */
export function topicLabel(question: { subject: string; subtopic?: string | null }): string {
  return question.subtopic ? `${question.subject} · ${question.subtopic}` : question.subject;
}
