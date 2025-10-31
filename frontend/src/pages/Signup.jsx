import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Button } from "../components/ui/button";
import { AuthLayout } from "../components/common/AuthLayout";
import {
  SignupStepper,
  SignupStep0,
  SignupStep0_5,
  SignupStep1,
  SignupStep2,
  SignupStep2_5,
  SignupStep3,
} from "../components/Signup";
import { useSignupForm, TOTAL_STEPS } from "../hooks/useSignupForm";
const STEP_TITLES = [
  "Informações de Acesso",
  "Dieta Existente",
  "Dados Pessoais",
  "Atividades Físicas",
  "Restrições e Preferências",
  "Preferências Alimentares",
];
function Signup() {
  const location = useLocation();
  const {
    step,
    loading,
    errors,
    values,
    progress,
    updateValue,
    next,
    back,
    handleCreate,
    skipEmailStep,
    isGoogleSignup,
  } = useSignupForm(location.state);
  const renderStep = () => {
    const stepProps = { values, errors, updateValue };
    switch (step) {
      case 0:
        return isGoogleSignup ? null : <SignupStep0 {...stepProps} />;
      case 1:
        return <SignupStep0_5 {...stepProps} />;
      case 2:
        return <SignupStep1 {...stepProps} />;
      case 3:
        return <SignupStep2 {...stepProps} />;
      case 4:
        return <SignupStep2_5 {...stepProps} />;
      case 5:
        return <SignupStep3 {...stepProps} />;
      default:
        return null;
    }
  };
  return (
    <AuthLayout
      title="Criar conta"
      subtitle={STEP_TITLES[step]}
      maxWidth="lg"
      footer={
        <div className="flex items-center justify-end gap-3 w-full">
          {step > 0 && !(isGoogleSignup && step === 1) && (
            <Button
              type="button"
              variant="outline"
              onClick={back}
              className="h-10"
            >
              Voltar
            </Button>
          )}
          {step < 5 ? (
            <Button type="button" onClick={next} className="h-10">
              Seguinte
            </Button>
          ) : (
            <Button
              type="button"
              onClick={handleCreate}
              disabled={loading}
              className="h-10"
            >
              {loading ? "Criando conta..." : "Finalizar cadastro"}
            </Button>
          )}
        </div>
      }
    >
      <div className="space-y-6">
        <SignupStepper
          step={step}
          progress={progress}
          totalSteps={TOTAL_STEPS}
        />
        {renderStep()}
        <div className="pt-4 border-t border-zinc-800">
          <p className="text-xs text-zinc-500 text-center">
            Usaremos suas respostas para montar sua dieta personalizada
          </p>
        </div>
      </div>
    </AuthLayout>
  );
}
export default Signup;