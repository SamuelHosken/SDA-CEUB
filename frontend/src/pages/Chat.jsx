import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { chatAPI } from "../services/api";
import { useSession } from "../hooks/useSession";
import AudioRecorder from "../components/AudioRecorder/AudioRecorder";
import StatusBar from "../components/StatusBar/StatusBar";
import { TypingIndicator } from "../components/common/LoadingSpinner";
import BottomNavigation from "../components/common/BottomNavigation";
import { Button } from "../components/ui/button";
import { Textarea } from "../components/ui/textarea";
const messageSchema = z.object({
  mensagem: z
    .string()
    .min(1, "Mensagem não pode estar vazia")
    .max(1000, "Mensagem muito longa (máximo 1000 caracteres)"),
});
function Chat() {
  const navigate = useNavigate();
  const { sessionId } = useSession();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showStatusBar, setShowStatusBar] = useState(false);
  const messagesRef = useRef(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm({
    resolver: zodResolver(messageSchema),
    defaultValues: {
      mensagem: "",
    },
  });
  const inputValue = watch("mensagem");
  const [suggestions] = useState([
    {
      icon: "🍗",
      title: "Registrar Refeição",
      text: "Acabei de comer algo",
      prompt:
        "Hoje eu comi 200g de frango grelhado com 150g de arroz integral e salada",
    },
    {
      icon: "⏰",
      title: "Próxima Refeição",
      text: "O que devo comer agora?",
      prompt: "Qual é a próxima refeição que devo fazer?",
    },
    {
      icon: "📊",
      title: "Progresso",
      text: "Como está minha dieta?",
      prompt: "Como estão minhas calorias e macros hoje?",
    },
    {
      icon: "🥗",
      title: "Sugestões",
      text: "Preciso de ideias saudáveis",
      prompt: "Preciso de uma sugestão de lanche saudável",
    },
  ]);
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  const scrollToBottom = () => {
    setTimeout(() => {
      if (messagesRef.current) {
        messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
      }
    }, 100);
  };
  const sendMessage = async (text) => {
    if (!text.trim() || loading) return;
    const userMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    try {
      const response = await chatAPI.conversar(text, sessionId);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.resposta },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `❌ Erro: ${error.response?.data?.detail || error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };
  const onSubmit = (data) => {
    sendMessage(data.mensagem);
    reset();
  };
  const handleAudioResult = async (text, response) => {
    if (response?.texto_reconhecido) {
      setMessages((prev) => [
        ...prev,
        { role: "user", content: response.texto_reconhecido },
      ]);
    }
    if (response?.resposta) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.resposta },
      ]);
    } else {
      await sendMessage(text);
    }
  };
  return (
    <div className="min-h-screen bg-black text-white flex flex-col md:flex-row pb-16 md:pb-0">
      {}
      <div className="flex-1 flex flex-col min-w-0">
        {}
        <header className="sticky top-0 z-10 bg-black/95 backdrop-blur-sm border-b border-zinc-800 px-4 py-3">
          <div className="flex items-center gap-3 max-w-4xl mx-auto">
            <button
              onClick={() => navigate("/")}
              className="p-2 rounded-md hover:bg-zinc-900 transition-colors md:hidden"
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
            <div className="flex items-center gap-3 flex-1 min-w-0">
              <div className="h-10 w-10 rounded-lg bg-zinc-900 border border-zinc-800 grid place-items-center flex-shrink-0">
                <span className="text-xl">🤖</span>
              </div>
              <div className="flex-1 min-w-0">
                <h1 className="text-base font-semibold truncate">
                  Agente IA Nutricional
                </h1>
                <p className="text-xs text-zinc-400 truncate">
                  Seu assistente pessoal para alimentação saudável
                </p>
              </div>
            </div>
            <button
              onClick={() => setShowStatusBar(!showStatusBar)}
              className="p-2 rounded-md hover:bg-zinc-900 transition-colors md:hidden"
              aria-label="Status"
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
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </button>
          </div>
        </header>
        {}
        {messages.length === 0 ? (
          <div className="flex-1 overflow-y-auto px-4 py-6 max-w-4xl mx-auto w-full">
            <div className="space-y-6">
              <div className="space-y-2">
                <h2 className="text-lg font-semibold">
                  Como posso ajudar hoje?
                </h2>
                <p className="text-sm text-zinc-400">
                  Escolha uma opção abaixo ou comece a conversar
                </p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {suggestions.map((s, idx) => (
                  <button
                    key={idx}
                    onClick={() => sendMessage(s.prompt)}
                    className="text-left bg-zinc-950 border border-zinc-800 rounded-lg p-4 hover:border-zinc-700 hover:bg-zinc-900 transition-all group"
                  >
                    <div className="flex items-start gap-3">
                      <div className="text-2xl group-hover:scale-110 transition-transform">
                        {s.icon}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-white mb-1">
                          {s.title}
                        </p>
                        <p className="text-xs text-zinc-400">{s.text}</p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div
            ref={messagesRef}
            className="flex-1 overflow-y-auto px-4 py-6 space-y-4 max-w-4xl mx-auto w-full"
          >
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex items-start gap-3 ${
                  msg.role === "user" ? "flex-row-reverse" : ""
                }`}
              >
                <div
                  className={`h-9 w-9 rounded-lg grid place-items-center flex-shrink-0 ${
                    msg.role === "user"
                      ? "bg-white text-black"
                      : "bg-zinc-900 border border-zinc-800 text-white"
                  }`}
                >
                  <span className="text-lg">
                    {msg.role === "user" ? "👤" : "🤖"}
                  </span>
                </div>
                <div
                  className={`max-w-[85%] sm:max-w-[75%] rounded-lg p-3 ${
                    msg.role === "user"
                      ? "bg-white text-black border border-zinc-200"
                      : "bg-zinc-950 text-white border border-zinc-800"
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap leading-relaxed">
                    {msg.content}
                  </p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex items-start gap-3">
                <div className="h-9 w-9 rounded-lg bg-zinc-900 border border-zinc-800 grid place-items-center flex-shrink-0">
                  <span className="text-lg">🤖</span>
                </div>
                <div className="bg-zinc-950 border border-zinc-800 rounded-lg p-3">
                  <TypingIndicator />
                </div>
              </div>
            )}
          </div>
        )}
        {}
        <div className="sticky bottom-0 bg-black/95 backdrop-blur-sm border-t border-zinc-800 p-4">
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex items-end gap-2 max-w-4xl mx-auto w-full"
          >
            <div className="flex-1 min-w-0">
              <Textarea
                {...register("mensagem")}
                rows={1}
                placeholder="Digite sua mensagem ou use o microfone..."
                disabled={loading}
                className="resize-none min-h-[44px] max-h-32"
              />
              {errors.mensagem?.message && (
                <p className="text-xs text-red-400 mt-1">
                  {errors.mensagem.message}
                </p>
              )}
            </div>
            <div className="flex items-center gap-2">
              <AudioRecorder
                onResult={handleAudioResult}
                disabled={loading}
                sessionId={sessionId}
              />
              <Button
                type="submit"
                disabled={loading || !inputValue?.trim()}
                className="h-11 px-4 min-w-[80px]"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                    Enviando
                  </span>
                ) : (
                  "Enviar"
                )}
              </Button>
            </div>
          </form>
        </div>
      </div>
      {}
      {showStatusBar && (
        <div
          className="fixed inset-0 z-50 md:hidden bg-black/50 backdrop-blur-sm"
          onClick={() => setShowStatusBar(false)}
        >
          <div
            className="absolute right-0 top-0 bottom-0 w-[85%] max-w-sm bg-black border-l border-zinc-800 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="sticky top-0 bg-black border-b border-zinc-800 p-4 flex items-center justify-between z-10">
              <h2 className="text-base font-semibold">Status Nutricional</h2>
              <button
                onClick={() => setShowStatusBar(false)}
                className="p-2 rounded-md hover:bg-zinc-900 transition-colors"
                aria-label="Fechar"
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
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            <div className="h-[calc(100vh-64px)] overflow-y-auto">
              <StatusBar sessionId={sessionId} />
            </div>
          </div>
        </div>
      )}
      <div
        className="hidden md:block md:w-80 border-l border-zinc-800 bg-black overflow-y-auto"
        style={{ maxHeight: "100vh" }}
      >
        <StatusBar sessionId={sessionId} />
      </div>
      {}
      <BottomNavigation />
    </div>
  );
}
export default Chat;