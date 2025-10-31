import * as React from "react";
import { twMerge } from "tailwind-merge";
export const Button = React.forwardRef(function Button(
  { className = "", variant = "default", size = "md", disabled, ...props },
  ref
) {
  const variants = {
    default: "bg-white text-black border border-white hover:bg-white/90",
    outline:
      "border border-zinc-700 bg-transparent text-white hover:bg-zinc-900",
    destructive: "bg-red-600 text-white hover:bg-red-700",
    ghost: "bg-transparent text-white hover:bg-zinc-900",
  };
  const sizes = {
    sm: "h-8 px-3 text-sm",
    md: "h-9 px-4 text-sm",
    lg: "h-10 px-5 text-sm",
  };
  return (
    <button
      ref={ref}
      disabled={disabled}
      className={twMerge(
        "inline-flex items-center justify-center whitespace-nowrap rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
        variants[variant] || variants.default,
        sizes[size] || sizes.md,
        className
      )}
      {...props}
    />
  );
});
export default Button;