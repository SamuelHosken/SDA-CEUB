import { useState } from "react";
import { SegmentedControlField } from "../common/FormField";
import { Label } from "../ui/label";
export function SignupStep0_5({ values, errors, updateValue }) {
  const [fileName, setFileName] = useState("");
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.type !== "application/pdf") {
        alert("Por favor, selecione apenas arquivos PDF.");
        e.target.value = "";
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        alert("O arquivo deve ter no máximo 10MB.");
        e.target.value = "";
        return;
      }
      setFileName(file.name);
      updateValue("dieta_pdf", file);
    }
  };
  const temDieta = values.tem_dieta === "sim";
  return (
    <div className="space-y-6">
      <SegmentedControlField
        label="Você já tem uma dieta criada por um nutricionista?"
        value={values.tem_dieta || ""}
        onChange={(value) => {
          updateValue("tem_dieta", value);
          if (value === "nao") {
            updateValue("dieta_pdf", null);
            setFileName("");
          }
        }}
        data={[
          { label: "Sim", value: "sim" },
          { label: "Não", value: "nao" },
        ]}
        error={errors.tem_dieta}
      />
      {temDieta && (
        <div className="space-y-2">
          <Label htmlFor="dieta_pdf" className="text-sm font-medium text-white">
            Envie o arquivo PDF da sua dieta
          </Label>
          <div className="flex items-center gap-3">
            <label
              htmlFor="dieta_pdf"
              className="flex-1 h-10 rounded-md border border-zinc-800 bg-black px-3 py-2 text-sm text-white hover:bg-zinc-900 cursor-pointer transition-colors flex items-center justify-center"
            >
              {fileName || "Selecionar arquivo PDF"}
            </label>
            <input
              id="dieta_pdf"
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
              className="hidden"
            />
            {fileName && (
              <button
                type="button"
                onClick={() => {
                  updateValue("dieta_pdf", null);
                  setFileName("");
                  const input = document.getElementById("dieta_pdf");
                  if (input) input.value = "";
                }}
                className="text-xs text-zinc-400 hover:text-white underline"
              >
                Remover
              </button>
            )}
          </div>
          {errors.dieta_pdf && (
            <p className="text-xs text-red-400 mt-1">{errors.dieta_pdf}</p>
          )}
          <p className="text-xs text-zinc-500 mt-1">
            Arquivo PDF da sua dieta (máximo 10MB)
          </p>
        </div>
      )}
    </div>
  );
}