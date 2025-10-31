export function Progress({ value = 0, className = "" }) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div
      className={["h-2 rounded bg-zinc-800 overflow-hidden", className].join(
        " "
      )}
    >
      <div className="h-full bg-white" style={{ width: `${clamped}%` }} />
    </div>
  );
}
export default Progress;