import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { auth } from "../services/firebase";
import {
  createUserWithEmailAndPassword,
  sendPasswordResetEmail,
  updateProfile,
} from "firebase/auth";
import api, { chatAPI } from "../services/api";
import { validateStep } from "../utils/signupValidation";
export const TOTAL_STEPS = 6;
export const initialSignupValues = {
  email: "",
  apelido: "",
  password: "",
  confirmPassword: "",
  tem_dieta: "",
  dieta_pdf: null,
  sexo: "",
  idade: 0,
  altura: 0,
  peso: 0,
  objetivo: "",
  treino_freq: "3x semana",
  treino_tipo: "Musculação",
  rotina: "",
  restricoes: "",
  alimentos_evita: "",
  alimentos_preferidos: "",
  refeicoes_dia: 3,
  onde_come: "Misto",
  suplementos: [],
};
export function useSignupForm(googleState = null) {
  const isGoogleSignup = googleState?.fromGoogle || false;
  const initialStep = isGoogleSignup ? 1 : 0;
  const [step, setStep] = useState(initialStep);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [values, setValues] = useState(() => {
    if (isGoogleSignup) {
      return {
        ...initialSignupValues,
        email: googleState?.email || "",
        apelido: googleState?.displayName || "",
      };
    }
    return initialSignupValues;
  });
  const navigate = useNavigate();
  useEffect(() => {
    if (isGoogleSignup && step < 1) {
      setStep(1);
    }
  }, [step, isGoogleSignup]);
  const updateValue = (name, value) => {
    setValues((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };
  const validateCurrentStep = () => {
    const validation = validateStep(step, values);
    setErrors(validation.errors);
    return validation;
  };
  const next = () => {
    const validation = validateCurrentStep();
    if (!validation.hasErrors) {
      setStep((s) => Math.min(TOTAL_STEPS - 1, s + 1));
    }
  };
  const back = () => {
    const minStep = isGoogleSignup ? 1 : 0;
    setStep((s) => Math.max(minStep, s - 1));
    setErrors({});
  };
  const handleCreate = async () => {
    const validation = validateCurrentStep();
    if (validation.hasErrors) return;
    setLoading(true);
    try {
      let token;
      let user;
      if (isGoogleSignup) {
        user = auth.currentUser;
        if (!user) {
          throw new Error("Usuário não autenticado");
        }
        token = await user.getIdToken();
        if (values.apelido && values.apelido !== user.displayName) {
          try {
            await updateProfile(user, { displayName: values.apelido });
          } catch (_) { }
        }
      } else {
        const cred = await createUserWithEmailAndPassword(
          auth,
          values.email,
          values.password
        );
        if (values.apelido) {
          try {
            await updateProfile(cred.user, { displayName: values.apelido });
          } catch (_) { }
        }
        user = cred.user;
        token = await cred.user.getIdToken();
      }
      await chatAPI.verifyToken(token);
      localStorage.setItem("auth_token", token);
      localStorage.setItem(
        "user",
        JSON.stringify({ uid: user.uid, email: user.email })
      );
      const payload = {
        apelido: values.apelido || null,
        perfil_nutricional: {
          sexo: values.sexo,
          idade: values.idade,
          altura: values.altura,
          peso: values.peso,
          objetivo: values.objetivo,
          treino_freq: values.treino_freq,
          treino_tipo: values.treino_tipo,
          rotina: values.rotina,
          restricoes: values.restricoes,
          alimentos_evita: values.alimentos_evita,
          alimentos_preferidos: values.alimentos_preferidos,
          refeicoes_dia: values.refeicoes_dia,
          onde_come: values.onde_come,
          suplementos: values.suplementos,
        },
      };
      await api.post("/auth/save-user-data", payload, {
        headers: { Authorization: `Bearer ${token}` },
      });
      navigate("/");
    } catch (e) {
      console.error("Erro ao criar conta:", e);
      if (e?.code === "auth/email-already-in-use") {
        const goLogin = confirm(
          "Este email já está cadastrado. Ir para a tela de login?\n\nVocê também pode solicitar redefinição de senha."
        );
        if (goLogin) {
          navigate("/login");
        } else {
          try {
            await sendPasswordResetEmail(auth, values.email);
            alert("Enviamos um email para redefinir sua senha.");
          } catch (err) {
            alert(
              "Não foi possível enviar o email de redefinição. Tente novamente mais tarde."
            );
          }
        }
      } else {
        alert("Erro ao criar conta: " + (e.message || e));
      }
    } finally {
      setLoading(false);
    }
  };
  const progress = isGoogleSignup
    ? ((step + 1) / TOTAL_STEPS) * 100
    : ((step + 1) / TOTAL_STEPS) * 100;
  return {
    step,
    loading,
    errors,
    values,
    progress,
    updateValue,
    next,
    back,
    handleCreate,
    isGoogleSignup,
    skipEmailStep: isGoogleSignup,
  };
}