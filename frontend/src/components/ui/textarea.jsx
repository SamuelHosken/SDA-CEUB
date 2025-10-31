import * as React from "react";
import { twMerge } from "tailwind-merge";
export const Textarea = React.forwardRef(function Textarea(
  { className = "", rows = 3, ...props },
  ref
) {
  return (
    <textarea
      ref={ref}
      rows={rows}
      className={twMerge(
        "w-full rounded-md border border-zinc-800 bg-black px-3 py-2 text-sm text-white placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-300 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  );
});
export default Textarea;