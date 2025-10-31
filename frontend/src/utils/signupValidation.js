export function validateStep(step, values) {
  const errors = {};
  switch (step) {
    case 0:
      if (!values.email) {
        errors.email = "Email obrigatório";
      } else if (!/^\S+@\S+$/.test(values.email)) {
        errors.email = "Email inválido";
      }
      if (!values.password) {
        errors.password = "Senha obrigatória";
      } else if (values.password.length < 6) {
        errors.password = "Mínimo 6 caracteres";
      }
      if (values.confirmPassword !== values.password) {
        errors.confirmPassword = "As senhas precisam ser iguais";
      }
      break;
    case 1:
      if (!values.tem_dieta) {
        errors.tem_dieta = "Por favor, selecione uma opção";
      } else if (values.tem_dieta === "sim" && !values.dieta_pdf) {
        errors.dieta_pdf = "Por favor, envie o arquivo PDF da sua dieta";
      }
      break;
    case 2:
      if (!values.sexo) {
        errors.sexo = "Informe seu sexo";
      }
      if (!values.idade || Number(values.idade) <= 0) {
        errors.idade = "Idade inválida";
      }
      if (!values.altura || Number(values.altura) <= 0) {
        errors.altura = "Altura inválida";
      }
      if (!values.peso || Number(values.peso) <= 0) {
        errors.peso = "Peso inválido";
      }
      if (!values.objetivo) {
        errors.objetivo = "Informe seu objetivo";
      }
      break;
    case 3:
      if (!values.treino_freq) {
        errors.treino_freq = "Informe a frequência";
      }
      if (!values.treino_tipo) {
        errors.treino_tipo = "Informe o tipo de treino";
      }
      if (!values.rotina) {
        errors.rotina = "Selecione a opção que mais se aproxima do seu dia a dia";
      }
      break;
    case 4:
      break;
    case 5:
      break;
    default:
      break;
  }
  return {
    errors,
    hasErrors: Object.keys(errors).length > 0,
  };
}