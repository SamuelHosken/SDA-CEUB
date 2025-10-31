import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signInWithEmailAndPassword } from "firebase/auth";
import {
  signInWithGoogle,
  onAuthStateChanged,
  auth,
} from "../services/firebase";
import api, { chatAPI } from "../services/api";
import { Button } from "../components/ui/button";
import { AuthLayout } from "../components/common/AuthLayout";
import { FormField } from "../components/common/FormField";
import { Separator } from "../components/ui/separator";
function Login() {
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) navigate("/");
    });
    return () => unsubscribe();
  }, [navigate]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);
    try {
      if (!email) {
        setErrors({ email: "Email é obrigatório" });
        setLoading(false);
        return;
      }
      if (!/^\S+@\S+$/.test(email)) {
        setErrors({ email: "Email inválido" });
        setLoading(false);
        return;
      }
      if (!password) {
        setErrors({ password: "Senha é obrigatória" });
        setLoading(false);
        return;
      }
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );
      const token = await userCredential.user.getIdToken();
      const response = await chatAPI.verifyToken(token);
      if (response.valid) {
        localStorage.setItem("auth_token", token);
        localStorage.setItem("user", JSON.stringify(response.user));
        try {
          await api.get("/auth/user-data", {
            headers: { Authorization: `Bearer ${token}` },
          });
        } catch {}
        navigate("/");
      }
    } catch (error) {
      console.error("Erro no login:", error);
      if (error.code === "auth/user-not-found") {
        setErrors({ email: "Usuário não encontrado" });
      } else if (error.code === "auth/wrong-password") {
        setErrors({ password: "Senha incorreta" });
      } else if (error.code === "auth/invalid-email") {
        setErrors({ email: "Email inválido" });
      } else {
        setErrors({ general: "Erro ao fazer login. Tente novamente." });
      }
    } finally {
      setLoading(false);
    }
  };
  const handleGoogleSignIn = async () => {
    setGoogleLoading(true);
    try {
      const user = await signInWithGoogle();
      const token = await user.getIdToken();
      const response = await chatAPI.verifyToken(token);
      if (response.valid) {
        localStorage.setItem("auth_token", token);
        localStorage.setItem("user", JSON.stringify(response.user));
        try {
          const userDataResponse = await api.get("/auth/user-data", {
            headers: { Authorization: `Bearer ${token}` },
          });
          const userData = userDataResponse.data;
          if (!userData?.perfil_nutricional) {
            navigate("/signup", {
              state: {
                fromGoogle: true,
                email: user.email,
                displayName: user.displayName || null,
              },
            });
            return;
          }
        } catch (error) {
          console.error("Erro ao buscar dados do usuário:", error);
          navigate("/signup", {
            state: {
              fromGoogle: true,
              email: user.email,
              displayName: user.displayName || null,
            },
          });
          return;
        }
        navigate("/");
      }
    } catch (error) {
      console.error("Erro no login Google:", error);
    } finally {
      setGoogleLoading(false);
    }
  };
  return (
    <AuthLayout
      title="Sistema Digital de Alimentação"
      subtitle="Faça login para acessar sua conta"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {errors.general && (
          <div className="p-3 rounded-md bg-red-500/10 border border-red-500/20">
            <p className="text-xs text-red-400">{errors.general}</p>
          </div>
        )}
        <FormField
          id="email"
          label="Email"
          type="email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            if (errors.email) setErrors({ ...errors, email: "" });
          }}
          error={errors.email}
          autoComplete="email"
          placeholder="seu@email.com"
          required
        />
        <FormField
          id="password"
          label="Senha"
          type="password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            if (errors.password) setErrors({ ...errors, password: "" });
          }}
          error={errors.password}
          autoComplete="current-password"
          placeholder="••••••••"
          required
        />
        <div className="flex items-center justify-between text-xs">
          <Link
            to="/reset"
            className="text-zinc-400 hover:text-white underline"
          >
            Esqueci minha senha
          </Link>
        </div>
        <Button type="submit" className="w-full h-10" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </Button>
      </form>
      <div className="text-center text-xs text-zinc-400 pt-2">
        Não tem conta?{" "}
        <Link to="/signup" className="underline text-white hover:text-zinc-300">
          Criar conta
        </Link>
      </div>
      <Separator className="my-6" />
      <Button
        variant="outline"
        onClick={handleGoogleSignIn}
        className="w-full h-10"
        disabled={googleLoading}
      >
        {googleLoading ? "Conectando..." : "Entrar com Google"}
      </Button>
      <p className="text-xs text-zinc-500 text-center mt-6">
        Ao continuar, você concorda com nossos termos de uso e política de
        privacidade
      </p>
    </AuthLayout>
  );
}
export default Login;