import {
  FormField,
  SelectField,
  SegmentedControlField,
} from "../common/FormField";
export function SignupStep1({ values, errors, updateValue }) {
  return (
    <div className="space-y-4">
      <SelectField
        id="sexo"
        label="Sexo"
        value={values.sexo}
        onChange={(e) => updateValue("sexo", e.target.value)}
        data={["Masculino", "Feminino", "Outro", "Prefiro não informar"]}
        placeholder="Selecione seu sexo"
        error={errors.sexo}
      />
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <FormField
          id="idade"
          label="Idade (anos)"
          type="number"
          value={values.idade || ""}
          onChange={(e) => updateValue("idade", parseInt(e.target.value) || 0)}
          error={errors.idade}
          inputMode="numeric"
          min={1}
          max={120}
          placeholder="25"
          required
        />
        <FormField
          id="altura"
          label="Altura (cm)"
          type="number"
          value={values.altura || ""}
          onChange={(e) => updateValue("altura", parseInt(e.target.value) || 0)}
          error={errors.altura}
          inputMode="numeric"
          min={80}
          max={250}
          placeholder="175"
          required
        />
        <FormField
          id="peso"
          label="Peso (kg)"
          type="number"
          value={values.peso || ""}
          onChange={(e) => updateValue("peso", parseFloat(e.target.value) || 0)}
          error={errors.peso}
          inputMode="numeric"
          min={20}
          max={400}
          step={0.5}
          placeholder="70.5"
          required
        />
      </div>
      <SegmentedControlField
        label="Objetivo"
        value={values.objetivo}
        onChange={(value) => updateValue("objetivo", value)}
        data={[
          { label: "Ganhar massa", value: "ganhar massa" },
          { label: "Perder gordura", value: "perder gordura" },
          { label: "Manter", value: "manter" },
          { label: "Performance", value: "performance" },
        ]}
        error={errors.objetivo}
      />
    </div>
  );
}