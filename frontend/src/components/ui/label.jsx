import * as React from "react";
import { twMerge } from "tailwind-merge";
export function Label({ className = "", ...props }) {
  return (
    <label
      className={twMerge("text-sm font-medium text-white", className)}
      {...props}
    />
  );
}
export default Label;