import { FormField } from "../common/FormField";
export function SignupStep2_5({ values, errors, updateValue }) {
  return (
    <div className="space-y-4">
      <FormField
        id="restricoes"
        label="Restrições, alergias ou problemas de saúde (opcional)"
        component="textarea"
        value={values.restricoes}
        onChange={(e) => updateValue("restricoes", e.target.value)}
        error={errors.restricoes}
        placeholder="Ex: alergia a lactose, hipertensão, etc."
        rows={3}
      />
      <FormField
        id="alimentos_evita"
        label="Alimentos que não gosta ou evita (opcional)"
        component="textarea"
        value={values.alimentos_evita}
        onChange={(e) => updateValue("alimentos_evita", e.target.value)}
        error={errors.alimentos_evita}
        placeholder="Ex: brócolis, peixe, etc."
        rows={3}
      />
    </div>
  );
}