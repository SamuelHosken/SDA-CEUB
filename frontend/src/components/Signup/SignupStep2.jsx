import { Label } from "../ui/label";
import { SelectField } from "../common/FormField";
export function SignupStep2({ values, errors, updateValue }) {
  const rotinaOptions = [
    {
      label: "Sedentário / Escritório",
      value: "sedentario",
      description:
        "Passo a maior parte do dia sentado, trabalho em escritório ou estudo.",
    },
    {
      label: "Ativo moderado",
      value: "ativo-moderado",
      description:
        "Fico parte do dia em pé ou em movimento, mas não realizo esforço físico intenso.",
    },
    {
      label: "Fisicamente ativo",
      value: "fisicamente-ativo",
      description:
        "Trabalho ou rotina com esforço físico (ex: construção, enfermagem, estoque, etc.).",
    },
    {
      label: "Agenda variável",
      value: "agenda-variavel",
      description:
        "Minha rotina muda bastante (turnos, viagens, plantões, etc.).",
    },
  ];
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <SelectField
          id="treino_freq"
          label="Frequência semanal de treino"
          value={values.treino_freq}
          onChange={(e) => updateValue("treino_freq", e.target.value)}
          data={[
            "0x semana",
            "1x semana",
            "2x semana",
            "3x semana",
            "4x semana",
            "5x semana",
            "6x semana",
            "7x semana",
          ]}
          placeholder="Selecione a frequência"
          error={errors.treino_freq}
        />
        <SelectField
          id="treino_tipo"
          label="Tipo de treino"
          value={values.treino_tipo}
          onChange={(e) => updateValue("treino_tipo", e.target.value)}
          data={[
            "Musculação",
            "Cross/Funcional",
            "Cardio",
            "Esportes",
            "Outro",
          ]}
          placeholder="Selecione o tipo"
          error={errors.treino_tipo}
        />
      </div>
      <div className="space-y-2">
        <Label>Selecione a opção que mais se aproxima do seu dia a dia</Label>
        <div className="grid grid-cols-1 gap-3">
          {rotinaOptions.map((opt) => {
            const isSelected = values.rotina === opt.value;
            return (
              <button
                key={opt.value}
                type="button"
                onClick={() => updateValue("rotina", opt.value)}
                className={`w-full text-left p-4 rounded-md border transition-all ${
                  isSelected
                    ? "border-white bg-white/10"
                    : "border-zinc-800 bg-zinc-900/50 hover:border-zinc-700 hover:bg-zinc-900"
                }`}
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`mt-0.5 w-4 h-4 rounded-full border-2 flex-shrink-0 ${
                      isSelected
                        ? "border-white bg-white"
                        : "border-zinc-600 bg-transparent"
                    }`}
                  >
                    {isSelected && (
                      <div className="w-full h-full rounded-full bg-black scale-50" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p
                      className={`text-sm font-medium ${
                        isSelected ? "text-white" : "text-zinc-300"
                      }`}
                    >
                      {opt.label}
                    </p>
                    <p className="text-xs text-zinc-500 mt-1">
                      {opt.description}
                    </p>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
        {errors.rotina && (
          <p className="text-xs text-red-400 mt-1">{errors.rotina}</p>
        )}
      </div>
    </div>
  );
}