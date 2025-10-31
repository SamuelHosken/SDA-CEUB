import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import BottomNavigation from "../components/common/BottomNavigation";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import api from "../services/api";
function Perfil() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);
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
  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="spinner" />
      </div>
    );
  }
  const perfil = userData?.perfil_nutricional || {};
  return (
    <div className="min-h-screen bg-black text-white pb-20">
      {}
      <header className="sticky top-0 z-10 bg-black/80 backdrop-blur-sm border-b border-zinc-800 px-4 py-3">
        <div className="flex items-center gap-3 max-w-md mx-auto">
          <button
            onClick={() => navigate("/")}
            className="p-2 rounded-md hover:bg-zinc-900 transition-colors"
            aria-label="Voltar"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>
          <h1 className="text-lg font-semibold flex-1">Perfil</h1>
        </div>
      </header>
      {}
      <main className="max-w-md mx-auto px-4 py-6 space-y-6">
        {}
        <Card className="border-zinc-800">
          <CardContent className="p-4 space-y-4">
            <h2 className="text-base font-semibold">Informações Pessoais</h2>
            <div className="space-y-3">
              <div>
                <p className="text-xs text-zinc-400 mb-1">Nome</p>
                <p className="text-sm">
                  {userData?.apelido ||
                    userData?.display_name ||
                    "Não informado"}
                </p>
              </div>
              <div>
                <p className="text-xs text-zinc-400 mb-1">Email</p>
                <p className="text-sm">{userData?.email || "Não informado"}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        {}
        <Card className="border-zinc-800">
          <CardContent className="p-4 space-y-4">
            <h2 className="text-base font-semibold">Perfil Nutricional</h2>
            <div className="grid grid-cols-2 gap-4">
              {perfil.sexo && (
                <div>
                  <p className="text-xs text-zinc-400 mb-1">Sexo</p>
                  <p className="text-sm">{perfil.sexo}</p>
                </div>
              )}
              {perfil.idade && (
                <div>
                  <p className="text-xs text-zinc-400 mb-1">Idade</p>
                  <p className="text-sm">{perfil.idade} anos</p>
                </div>
              )}
              {perfil.altura && (
                <div>
                  <p className="text-xs text-zinc-400 mb-1">Altura</p>
                  <p className="text-sm">{perfil.altura} cm</p>
                </div>
              )}
              {perfil.peso && (
                <div>
                  <p className="text-xs text-zinc-400 mb-1">Peso</p>
                  <p className="text-sm">{perfil.peso} kg</p>
                </div>
              )}
              {perfil.objetivo && (
                <div className="col-span-2">
                  <p className="text-xs text-zinc-400 mb-1">Objetivo</p>
                  <p className="text-sm capitalize">{perfil.objetivo}</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
        {}
        {(perfil.treino_freq || perfil.treino_tipo || perfil.rotina) && (
          <Card className="border-zinc-800">
            <CardContent className="p-4 space-y-4">
              <h2 className="text-base font-semibold">Atividades Físicas</h2>
              <div className="space-y-3">
                {perfil.treino_freq && (
                  <div>
                    <p className="text-xs text-zinc-400 mb-1">
                      Frequência de Treino
                    </p>
                    <p className="text-sm">{perfil.treino_freq}</p>
                  </div>
                )}
                {perfil.treino_tipo && (
                  <div>
                    <p className="text-xs text-zinc-400 mb-1">Tipo de Treino</p>
                    <p className="text-sm">{perfil.treino_tipo}</p>
                  </div>
                )}
                {perfil.rotina && (
                  <div>
                    <p className="text-xs text-zinc-400 mb-1">Rotina</p>
                    <p className="text-sm">{perfil.rotina}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}
        <Button
          variant="outline"
          onClick={() => navigate("/")}
          className="w-full h-12"
        >
          Voltar para Dashboard
        </Button>
      </main>
      {}
      <BottomNavigation />
    </div>
  );
}
export default Perfil;