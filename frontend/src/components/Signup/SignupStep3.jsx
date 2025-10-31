import { Label } from "../ui/label";
import { FormField, SelectField } from "../common/FormField";
export function SignupStep3({ values, errors, updateValue }) {
  const suplementosOptions = [
    "Creatina",
    "Whey",
    "BCAA",
    "Vitaminas",
    "Omega-3",
    "Pré-treino",
  ];
  return (
    <div className="space-y-4">
      <FormField
        id="alimentos_preferidos"
        label="Alimentos/Refeições que mais gosta (opcional)"
        component="textarea"
        value={values.alimentos_preferidos}
        onChange={(e) => updateValue("alimentos_preferidos", e.target.value)}
        error={errors.alimentos_preferidos}
        placeholder="Ex: frango grelhado, salada, etc."
        rows={3}
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <FormField
          id="refeicoes_dia"
          label="Refeições por dia"
          type="number"
          value={values.refeicoes_dia || ""}
          onChange={(e) =>
            updateValue("refeicoes_dia", parseInt(e.target.value) || 3)
          }
          error={errors.refeicoes_dia}
          inputMode="numeric"
          min={1}
          max={10}
          placeholder="3"
        />
        <SelectField
          id="onde_come"
          label="Onde come"
          value={values.onde_come}
          onChange={(e) => updateValue("onde_come", e.target.value)}
          data={["Casa", "Fora", "Misto"]}
          placeholder="Selecione"
          error={errors.onde_come}
        />
      </div>
      <div className="space-y-2">
        <Label className="text-sm font-medium text-white">
          Suplementos (opcional)
        </Label>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {suplementosOptions.map((opt) => {
            const isSelected = values.suplementos?.includes(opt) || false;
            return (
              <button
                key={opt}
                type="button"
                onClick={() => {
                  const currentSuplementos = values.suplementos || [];
                  if (isSelected) {
                    updateValue(
                      "suplementos",
                      currentSuplementos.filter((s) => s !== opt)
                    );
                  } else {
                    updateValue("suplementos", [...currentSuplementos, opt]);
                  }
                }}
                className={`w-full text-left p-3 rounded-md border transition-all ${
                  isSelected
                    ? "border-white bg-white/10"
                    : "border-zinc-800 bg-zinc-900/50 hover:border-zinc-700 hover:bg-zinc-900"
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-4 h-4 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                      isSelected
                        ? "border-white bg-white"
                        : "border-zinc-600 bg-transparent"
                    }`}
                  >
                    {isSelected && (
                      <svg
                        className="w-3 h-3 text-black"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={3}
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    )}
                  </div>
                  <span
                    className={`text-sm font-medium ${
                      isSelected ? "text-white" : "text-zinc-300"
                    }`}
                  >
                    {opt}
                  </span>
                </div>
              </button>
            );
          })}
        </div>
        {values.suplementos?.length > 0 && (
          <p className="text-xs text-zinc-500 mt-1">
            {values.suplementos.length} suplemento(s) selecionado(s)
          </p>
        )}
      </div>
    </div>
  );
}