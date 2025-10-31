import { Link } from "react-router-dom";
import { FormField } from "../common/FormField";
export function SignupStep0({ values, errors, updateValue }) {
  return (
    <div className="space-y-4">
      <FormField
        id="email"
        label="Email"
        type="email"
        value={values.email}
        onChange={(e) => updateValue("email", e.target.value)}
        error={errors.email}
        autoComplete="email"
        placeholder="seu@email.com"
        required
      />
      <FormField
        id="apelido"
        label="Apelido (opcional)"
        type="text"
        value={values.apelido}
        onChange={(e) => updateValue("apelido", e.target.value)}
        error={errors.apelido}
        autoComplete="nickname"
        placeholder="Como você gostaria de ser chamado?"
      />
      <FormField
        id="password"
        label="Senha"
        type="password"
        value={values.password}
        onChange={(e) => updateValue("password", e.target.value)}
        error={errors.password}
        autoComplete="new-password"
        placeholder="Mínimo 6 caracteres"
        required
      />
      <FormField
        id="confirmPassword"
        label="Confirmar senha"
        type="password"
        value={values.confirmPassword}
        onChange={(e) => updateValue("confirmPassword", e.target.value)}
        error={errors.confirmPassword}
        autoComplete="new-password"
        placeholder="Digite a senha novamente"
        required
      />
      <div className="text-center text-xs text-zinc-400 pt-2">
        Já tem conta?{" "}
        <Link to="/login" className="underline text-white hover:text-zinc-300">
          Entrar
        </Link>
      </div>
    </div>
  );
}