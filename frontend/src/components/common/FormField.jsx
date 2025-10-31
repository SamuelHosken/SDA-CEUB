import React from "react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { Textarea } from "../ui/textarea";
export function FormField({
  id,
  label,
  error,
  hint,
  type = "text",
  component = "input",
  className = "",
  ...inputProps
}) {
  const InputComponent = component === "textarea" ? Textarea : Input;
  return (
    <div className={`space-y-2 ${className}`}>
      {label && (
        <Label htmlFor={id} className="text-sm font-medium text-white">
          {label}
        </Label>
      )}
      <InputComponent
        id={id}
        type={type}
        className={`${component === "textarea" ? "min-h-[80px]" : "h-10"} ${
          error ? "border-red-500 focus-visible:ring-red-500" : ""
        }`}
        aria-invalid={error ? "true" : "false"}
        aria-describedby={
          error ? `${id}-error` : hint ? `${id}-hint` : undefined
        }
        {...inputProps}
      />
      {error && (
        <p id={`${id}-error`} className="text-xs text-red-400 mt-1">
          {error}
        </p>
      )}
      {hint && !error && (
        <p id={`${id}-hint`} className="text-xs text-zinc-500 mt-1">
          {hint}
        </p>
      )}
    </div>
  );
}
export function SelectField({
  id,
  label,
  value,
  onChange,
  data = [],
  placeholder,
  error,
  hint,
  className = "",
}) {
  return (
    <div className={`space-y-2 ${className}`}>
      {label && (
        <Label htmlFor={id} className="text-sm font-medium text-white">
          {label}
        </Label>
      )}
      <select
        id={id}
        value={value}
        onChange={onChange}
        className={`w-full h-10 rounded-md border ${
          error ? "border-red-500" : "border-zinc-800"
        } bg-black px-3 py-2 text-sm text-white placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-1 ${
          error ? "focus-visible:ring-red-500" : "focus-visible:ring-zinc-300"
        } disabled:cursor-not-allowed disabled:opacity-50`}
        aria-invalid={error ? "true" : "false"}
        aria-describedby={
          error ? `${id}-error` : hint ? `${id}-hint` : undefined
        }
      >
        <option value="" disabled>
          {placeholder || "Selecione..."}
        </option>
        {data.map((opt) => (
          <option key={opt.value || opt} value={opt.value || opt}>
            {opt.label || opt}
          </option>
        ))}
      </select>
      {error && (
        <p id={`${id}-error`} className="text-xs text-red-400 mt-1">
          {error}
        </p>
      )}
      {hint && !error && (
        <p id={`${id}-hint`} className="text-xs text-zinc-500 mt-1">
          {hint}
        </p>
      )}
    </div>
  );
}
export function SegmentedControlField({
  label,
  value,
  onChange,
  data = [],
  error,
  hint,
  className = "",
}) {
  return (
    <div className={`space-y-2 ${className}`}>
      {label && (
        <Label className="text-sm font-medium text-white">{label}</Label>
      )}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {data.map((d) => (
          <button
            key={d.value}
            type="button"
            onClick={() => onChange(d.value)}
            className={`h-10 w-full border rounded-md px-3 text-sm transition-colors whitespace-nowrap flex items-center justify-center ${
              value === d.value
                ? "bg-white text-black border-white"
                : "bg-zinc-900 text-white border-zinc-800 hover:bg-zinc-800"
            }`}
          >
            {d.label}
          </button>
        ))}
      </div>
      {error && <p className="text-xs text-red-400 mt-1">{error}</p>}
      {hint && !error && <p className="text-xs text-zinc-500 mt-1">{hint}</p>}
    </div>
  );
}
export default FormField;