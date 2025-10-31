export function LoadingSpinner() {
  return (
    <div className="flex items-center gap-2 justify-center">
      <div className="spinner" />
      <span className="text-xs text-zinc-400">Processando...</span>
    </div>
  );
}
export function TypingIndicator() {
  return (
    <div className="flex items-start gap-1 p-3 bg-zinc-900 border border-zinc-800 rounded-md">
      <span className="w-1.5 h-1.5 rounded-full bg-white animate-bounce [animation-delay:0ms]" />
      <span className="w-1.5 h-1.5 rounded-full bg-white animate-bounce [animation-delay:150ms]" />
      <span className="w-1.5 h-1.5 rounded-full bg-white animate-bounce [animation-delay:300ms]" />
    </div>
  );
}