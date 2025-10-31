import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  User,
  Settings,
  MessageCircle,
  Flame,
  Sparkles,
  Activity,
} from "lucide-react";
import BottomNavigation from "../components/common/BottomNavigation";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Progress } from "../components/ui/progress";
import api from "../services/api";
import { logout } from "../services/firebase";
function Home() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);
  const [stats, setStats] = useState({
    proteinasHoje: 0,
    caloriasHoje: 0,
    caloriasMeta: 2000,
    exercicioHoje: 0,
    exercicioMeta: 30,
  });
  useEffect(() => {
    loadUserData();
  }, []);
  const loadUserData = async () => {
    try {
      const token = localStorage.getItem("auth_token");
      if (!token) {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user");
        localStorage.removeItem("sda_session_id");
        navigate("/login", { replace: true });
        return;
      }
      const response = await api.get("/auth/user-data", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUserData(response.data);
      setStats({
        proteinasHoje: 85,
        caloriasHoje: 1450,
        caloriasMeta: 2000,
        exercicioHoje: 25,
        exercicioMeta: 30,
      });
    } catch (error) {
      console.error("Erro ao carregar dados:", error);
      if (error.response?.status === 401 || error.response?.status === 403) {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user");
        localStorage.removeItem("sda_session_id");
        navigate("/login", { replace: true });
      }
    } finally {
      setLoading(false);
    }
  };
  const handleLogout = async () => {
    try {
      await logout();
    } catch (e) {}
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user");
    navigate("/login");
  };
  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="spinner" />
      </div>
    );
  }
  const caloriasProgress = Math.min(
    (stats.caloriasHoje / stats.caloriasMeta) * 100,
    100
  );
  const exercicioProgress = Math.min(
    (stats.exercicioHoje / stats.exercicioMeta) * 100,
    100
  );
  const proteinasProgress = Math.min((stats.proteinasHoje / 150) * 100, 100);
  return (
    <div className="min-h-screen bg-black text-white pb-20">
      {}
      <header className="sticky top-0 z-10 bg-black/80 backdrop-blur-sm border-b border-zinc-800 px-4 py-3">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <h1 className="text-lg font-semibold">Dashboard</h1>
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate("/perfil")}
              className="p-2 rounded-md hover:bg-zinc-900 transition-colors"
              aria-label="Perfil"
            >
              <User className="w-5 h-5" strokeWidth={1.5} />
            </button>
            <button
              onClick={() => navigate("/configuracoes")}
              className="p-2 rounded-md hover:bg-zinc-900 transition-colors"
              aria-label="Configurações"
            >
              <Settings className="w-5 h-5" strokeWidth={1.5} />
            </button>
          </div>
        </div>
      </header>
      {}
      <main className="max-w-md mx-auto px-4 py-6 space-y-6">
        {}
        <div className="space-y-1">
          <h2 className="text-xl font-semibold">
            Olá, {userData?.apelido || userData?.display_name || "Usuário"}
          </h2>
          <p className="text-sm text-zinc-400">
            Acompanhe seu progresso de hoje
          </p>
        </div>
        {}
        <div className="space-y-4">
          {}
          <Card className="border-zinc-800">
            <CardContent className="p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm text-zinc-400">Calorias</p>
                  <p className="text-2xl font-semibold">
                    {stats.caloriasHoje}{" "}
                    <span className="text-sm font-normal text-zinc-500">
                      / {stats.caloriasMeta}
                    </span>
                  </p>
                </div>
                <div className="p-3 rounded-full bg-zinc-900">
                  <Flame className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
              </div>
              <Progress value={caloriasProgress} className="h-2" />
              <p className="text-xs text-zinc-500">
                {stats.caloriasMeta - stats.caloriasHoje > 0
                  ? `${
                      stats.caloriasMeta - stats.caloriasHoje
                    } calorias restantes`
                  : "Meta atingida!"}
              </p>
            </CardContent>
          </Card>
          {}
          <Card className="border-zinc-800">
            <CardContent className="p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm text-zinc-400">Proteínas</p>
                  <p className="text-2xl font-semibold">
                    {stats.proteinasHoje}g{" "}
                    <span className="text-sm font-normal text-zinc-500">
                      / 150g
                    </span>
                  </p>
                </div>
                <div className="p-3 rounded-full bg-zinc-900">
                  <Sparkles className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
              </div>
              <Progress value={proteinasProgress} className="h-2" />
              <p className="text-xs text-zinc-500">
                {150 - stats.proteinasHoje > 0
                  ? `${150 - stats.proteinasHoje}g restantes`
                  : "Meta atingida!"}
              </p>
            </CardContent>
          </Card>
          {}
          <Card className="border-zinc-800">
            <CardContent className="p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm text-zinc-400">Exercício Físico</p>
                  <p className="text-2xl font-semibold">
                    {stats.exercicioHoje}{" "}
                    <span className="text-sm font-normal text-zinc-500">
                      / {stats.exercicioMeta} min
                    </span>
                  </p>
                </div>
                <div className="p-3 rounded-full bg-zinc-900">
                  <Activity className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
              </div>
              <Progress value={exercicioProgress} className="h-2" />
              <p className="text-xs text-zinc-500">
                {stats.exercicioMeta - stats.exercicioHoje > 0
                  ? `${
                      stats.exercicioMeta - stats.exercicioHoje
                    } minutos restantes`
                  : "Meta atingida!"}
              </p>
            </CardContent>
          </Card>
        </div>
        {}
        <div className="space-y-3 pt-4">
          <Button
            onClick={() => navigate("/chat")}
            className="w-full h-12 text-base font-medium"
          >
            <MessageCircle className="w-5 h-5 mr-2" strokeWidth={1.5} />
            Iniciar Novo Chat
          </Button>
          <div className="grid grid-cols-2 gap-3">
            <Button
              variant="outline"
              onClick={() => navigate("/perfil")}
              className="h-12"
            >
              <User className="w-5 h-5 mr-2" strokeWidth={1.5} />
              Perfil
            </Button>
            <Button
              variant="outline"
              onClick={() => navigate("/configuracoes")}
              className="h-12"
            >
              <Settings className="w-5 h-5 mr-2" strokeWidth={1.5} />
              Configurações
            </Button>
          </div>
        </div>
      </main>
      {}
      <BottomNavigation />
    </div>
  );
}
export default Home;