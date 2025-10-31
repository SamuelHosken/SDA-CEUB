import * as React from "react";
import { twMerge } from "tailwind-merge";
export function Card({ className = "", ...props }) {
  return (
    <div
      className={twMerge(
        "rounded-md border border-zinc-800 bg-zinc-950 text-white",
        className
      )}
      {...props}
    />
  );
}
export function CardHeader({ className = "", ...props }) {
  return <div className={twMerge("p-6 pb-4", className)} {...props} />;
}
export function CardTitle({ className = "", ...props }) {
  return (
    <h3 className={twMerge("text-lg font-semibold", className)} {...props} />
  );
}
export function CardContent({ className = "", ...props }) {
  return <div className={twMerge("p-6 pt-0", className)} {...props} />;
}
export function CardFooter({ className = "", ...props }) {
  return <div className={twMerge("p-6 pt-0", className)} {...props} />;
}
export default Card;