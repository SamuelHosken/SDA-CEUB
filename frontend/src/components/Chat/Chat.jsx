import { useState, useEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { chatAPI } from "../../services/api";
import AudioRecorder from "../AudioRecorder/AudioRecorder";
import { TypingIndicator } from "../common/LoadingSpinner";
import { Button } from "../../components/ui/button";
import { Textarea } from "../../components/ui/textarea";
const messageSchema = z.object({
  mensagem: z
    .string()
    .min(1, "Mensagem não pode estar vazia")
    .max(1000, "Mensagem muito longa (máximo 1000 caracteres)"),
});
function Chat({ sessionId }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
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
  const messagesRef = useRef(null);
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
    <div className="h-screen bg-black text-white flex flex-col">
      <div className="border-b border-zinc-800 bg-zinc-950 p-6 flex items-center gap-4">
        <div className="h-10 w-10 rounded-md bg-zinc-800 grid place-items-center">
          🤖
        </div>
        <div className="flex-1">
          <p className="font-semibold">Agente IA Nutricional</p>
          <p className="text-sm text-zinc-400 mt-0.5">
            Seu assistente pessoal para uma alimentação saudável
          </p>
        </div>
      </div>
      {messages.length === 0 ? (
        <div className="flex-1 overflow-auto p-6">
          <div className="space-y-6">
            <div>
              <p className="font-medium">Como posso ajudar hoje?</p>
              <p className="text-sm text-zinc-400">
                Escolha uma opção abaixo ou comece a conversar
              </p>
            </div>
            <div
              className="grid gap-4"
              style={{
                gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
              }}
            >
              {suggestions.map((s, idx) => (
                <div
                  key={idx}
                  className="bg-zinc-950 border border-zinc-800 rounded-md p-4 cursor-pointer hover:border-zinc-600"
                  onClick={() => sendMessage(s.prompt)}
                >
                  <div className="flex items-start gap-3">
                    <div className="text-2xl">{s.icon}</div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">{s.title}</p>
                      <p className="text-xs text-zinc-400">{s.text}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div ref={messagesRef} className="flex-1 overflow-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-3 ${
                msg.role === "user" ? "flex-row-reverse" : ""
              }`}
            >
              <div
                className={`h-8 w-8 rounded-md grid place-items-center ${
                  msg.role === "user"
                    ? "bg-white text-black"
                    : "bg-zinc-800 text-white"
                }`}
              >
                {msg.role === "user" ? "👤" : "🤖"}
              </div>
              <div
                className={`max-w-[75%] border border-zinc-800 rounded-md p-3 ${
                  msg.role === "user"
                    ? "bg-white text-black"
                    : "bg-zinc-950 text-white"
                }`}
              >
                <p className="text-sm whitespace-pre-wrap leading-relaxed">
                  {msg.content}
                </p>
              </div>
            </div>
          ))}
          {loading && <TypingIndicator />}
        </div>
      )}
      <div className="border-t border-zinc-800 bg-zinc-950 p-4">
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex items-end gap-2"
        >
          <div className="flex-1">
            <Textarea
              {...register("mensagem")}
              rows={1}
              placeholder="Digite sua mensagem ou use o microfone..."
              disabled={loading}
            />
            {errors.mensagem?.message && (
              <p className="text-xs text-red-400 mt-1">
                {errors.mensagem.message}
              </p>
            )}
          </div>
          <Button
            type="submit"
            disabled={loading || !inputValue?.trim()}
            className="h-10 px-3"
          >
            Enviar
          </Button>
          <AudioRecorder
            onResult={handleAudioResult}
            disabled={loading}
            sessionId={sessionId}
          />
        </form>
      </div>
    </div>
  );
}
export default Chat;