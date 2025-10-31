import { useNavigate, useLocation } from "react-router-dom";
import { Home, MessageCircle, User, Settings } from "lucide-react";
function BottomNavigation() {
  const navigate = useNavigate();
  const location = useLocation();
  const isActive = (path) => location.pathname === path;
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-zinc-950 border-t border-zinc-800 md:hidden z-50">
      <div className="flex items-center justify-around px-2 py-2">
        <button
          onClick={() => navigate("/")}
          className={`flex flex-col items-center gap-1 px-3 py-2 rounded-md transition-colors ${
            isActive("/") ? "text-white" : "text-zinc-400 hover:text-white"
          }`}
          aria-label="Home"
        >
          <Home className="w-6 h-6" strokeWidth={1.5} />
          <span className="text-xs">Home</span>
        </button>
        <button
          onClick={() => navigate("/chat")}
          className={`flex flex-col items-center gap-1 px-3 py-2 rounded-md transition-colors ${
            isActive("/chat") ? "text-white" : "text-zinc-400 hover:text-white"
          }`}
          aria-label="Chat"
        >
          <MessageCircle className="w-6 h-6" strokeWidth={1.5} />
          <span className="text-xs">Chat</span>
        </button>
        <button
          onClick={() => navigate("/perfil")}
          className={`flex flex-col items-center gap-1 px-3 py-2 rounded-md transition-colors ${
            isActive("/perfil")
              ? "text-white"
              : "text-zinc-400 hover:text-white"
          }`}
          aria-label="Perfil"
        >
          <User className="w-6 h-6" strokeWidth={1.5} />
          <span className="text-xs">Perfil</span>
        </button>
        <button
          onClick={() => navigate("/configuracoes")}
          className={`flex flex-col items-center gap-1 px-3 py-2 rounded-md transition-colors ${
            isActive("/configuracoes")
              ? "text-white"
              : "text-zinc-400 hover:text-white"
          }`}
          aria-label="Configurações"
        >
          <Settings className="w-6 h-6" strokeWidth={1.5} />
          <span className="text-xs">Config</span>
        </button>
      </div>
    </nav>
  );
}
export default BottomNavigation;