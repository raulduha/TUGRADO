"use client";

import { useId, useState } from "react";

type FieldProps = {
  label: string;
  name: string;
  type?: "email" | "password" | "text";
  autoComplete?: string;
  hint?: string;
  error?: string;
  defaultValue?: string;
  required?: boolean;
};

export function Field({
  label,
  name,
  type = "text",
  autoComplete,
  hint,
  error,
  defaultValue,
  required = true,
}: FieldProps) {
  const id = useId();
  const [visible, setVisible] = useState(false);
  const isPassword = type === "password";
  const describedBy = [hint ? `${id}-hint` : null, error ? `${id}-error` : null]
    .filter(Boolean)
    .join(" ");

  return (
    <div className="space-y-1.5">
      <label htmlFor={id} className="block text-sm font-medium">
        {label}
      </label>
      <div className="relative">
        <input
          id={id}
          name={name}
          type={isPassword && visible ? "text" : type}
          autoComplete={autoComplete}
          defaultValue={defaultValue}
          required={required}
          aria-invalid={error ? true : undefined}
          aria-describedby={describedBy || undefined}
          className={`block w-full rounded-lg border bg-background px-3 py-2.5 text-base outline-none transition focus:border-brand focus:ring-2 focus:ring-brand/30 ${
            error ? "border-danger" : "border-line"
          } ${isPassword ? "pr-20" : ""}`}
        />
        {isPassword ? (
          <button
            type="button"
            onClick={() => setVisible((v) => !v)}
            aria-pressed={visible}
            className="absolute inset-y-0 right-0 my-1 mr-1 rounded-md px-3 text-sm font-medium text-brand hover:bg-brand/10 focus-visible:outline-2 focus-visible:outline-brand"
          >
            {visible ? "Ocultar" : "Mostrar"}
          </button>
        ) : null}
      </div>
      {hint ? (
        <p id={`${id}-hint`} className="text-sm text-muted">
          {hint}
        </p>
      ) : null}
      {error ? (
        <p id={`${id}-error`} className="text-sm font-medium text-danger">
          {error}
        </p>
      ) : null}
    </div>
  );
}
