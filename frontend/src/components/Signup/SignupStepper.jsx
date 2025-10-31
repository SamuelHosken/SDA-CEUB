import { Progress } from "../ui/progress";
export function SignupStepper({ step, progress, totalSteps = 5 }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-xs text-zinc-400">
        <span>
          Passo {step + 1} de {totalSteps}
        </span>
        <span>{Math.round(progress)}%</span>
      </div>
      <Progress value={progress} className="h-1" />
    </div>
  );
}