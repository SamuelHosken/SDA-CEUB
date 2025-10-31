import { useState } from "react";
import { useNavigate } from "react-router-dom";
import BottomNavigation from "../components/common/BottomNavigation";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { logout } from "../services/firebase";
function Configuracoes() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const handleLogout = async (e) => {
    e?.preventDefault();
    e?.stopPropagation();
    if (!confirm("Tem certeza que deseja sair?")) return;
    setLoading(true);
    try {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
      localStorage.removeItem("sda_session_id");
      await logout();
    } catch (error) {
      console.error("Erro ao fazer logout:", error);
    } finally {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
      localStorage.removeItem("sda_session_id");
      navigate("/login", { replace: true });
      setLoading(false);
    }
  };
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
          <h1 className="text-lg font-semibold flex-1">Configurações</h1>
        </div>
      </header>
      {}
      <main className="max-w-md mx-auto px-4 py-6 space-y-6">
        <Card className="border-zinc-800">
          <CardContent className="p-4 space-y-4">
            <h2 className="text-base font-semibold">Preferências</h2>
            <div className="space-y-3">
              <button className="w-full text-left p-3 rounded-md hover:bg-zinc-900 transition-colors">
                <p className="text-sm font-medium">Notificações</p>
                <p className="text-xs text-zinc-400 mt-1">
                  Gerencie suas notificações
                </p>
              </button>
              <button className="w-full text-left p-3 rounded-md hover:bg-zinc-900 transition-colors">
                <p className="text-sm font-medium">Metas</p>
                <p className="text-xs text-zinc-400 mt-1">
                  Configure suas metas diárias
                </p>
              </button>
            </div>
          </CardContent>
        </Card>
        <Card className="border-zinc-800">
          <CardContent className="p-4 space-y-4">
            <h2 className="text-base font-semibold">Sobre</h2>
            <div className="space-y-3">
              <button className="w-full text-left p-3 rounded-md hover:bg-zinc-900 transition-colors">
                <p className="text-sm font-medium">Termos de Uso</p>
              </button>
              <button className="w-full text-left p-3 rounded-md hover:bg-zinc-900 transition-colors">
                <p className="text-sm font-medium">Política de Privacidade</p>
              </button>
              <button className="w-full text-left p-3 rounded-md hover:bg-zinc-900 transition-colors">
                <p className="text-sm font-medium">Versão</p>
                <p className="text-xs text-zinc-400 mt-1">1.0.0</p>
              </button>
            </div>
          </CardContent>
        </Card>
        <Button
          variant="outline"
          onClick={handleLogout}
          disabled={loading}
          className="w-full h-12 border-red-500/50 text-red-400 hover:bg-red-500/10 relative z-10"
          type="button"
        >
          {loading ? "Saindo..." : "Sair da Conta"}
        </Button>
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
export default Configuracoes;