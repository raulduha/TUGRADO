// Tipos y etiquetas compartidas del panel del banco de preguntas.

export type Status = "draft" | "in_review" | "approved" | "published" | "retired";

export type Summary = {
  id: string;
  question_id: string;
  number: number;
  status: Status;
  subject: string;
  subtopic: string | null;
  difficulty: number;
  prompt: string;
  author: string;
  is_author: boolean;
};

export type Detail = Summary & {
  options: string[];
  correct_position: number;
  explanation: string;
  source: string;
  reviews: Array<{ decision: string; comment: string | null; reviewer: string; created_at: string }>;
  history: Array<{ id: string; number: number; status: Status; author: string; created_at: string }>;
};

export type SubjectOption = { name: string; subtopics: string[] };

/** Contenido que se envía al crear o editar (POST /admin/questions y /{id}/edit). */
export type QuestionInput = {
  subject: string;
  subtopic: string | null;
  difficulty: number;
  prompt: string;
  options: string[];
  correct_position: number;
  explanation: string;
  source: string;
};

export const STATUS: Record<Status, { label: string; className: string }> = {
  draft: { label: "Borrador", className: "bg-background text-muted" },
  in_review: { label: "En revisión", className: "bg-accent-soft text-[#9a5b00]" },
  approved: { label: "Aprobada", className: "bg-brand-soft text-brand-strong" },
  published: { label: "Publicada", className: "bg-success/10 text-success" },
  retired: { label: "Retirada", className: "bg-line text-muted" },
};

export const LETTERS = "ABCDE";
export const DIFFICULTY = ["", "Fácil", "Media", "Difícil"];
export const MIN_OPTIONS = 2;
export const MAX_OPTIONS = 5;

export function StatusBadge({ status, number }: { status: Status; number?: number }) {
  return (
    <span className={`whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-semibold ${STATUS[status].className}`}>
      {STATUS[status].label}
      {number ? ` · v${number}` : ""}
    </span>
  );
}
