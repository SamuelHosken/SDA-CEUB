export function Separator({ className = "", ...props }) {
  return (
    <div
      className={["w-full h-px bg-zinc-800", className]
        .filter(Boolean)
        .join(" ")}
      {...props}
    />
  );
}
export default Separator;