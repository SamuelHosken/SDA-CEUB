import { useState } from "react";
import { chatAPI } from "../../services/api";
function AudioRecorder({ onResult, disabled, sessionId }) {
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [processing, setProcessing] = useState(false);
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 16000,
          channelCount: 1,
          volume: 1.0,
        },
      });
      const options = {
        mimeType: "audio/webm;codecs=opus",
        audioBitsPerSecond: 128000,
      };
      let recorder;
      try {
        recorder = new MediaRecorder(stream, options);
      } catch (e) {
        console.warn("WebM não disponível, tentando outros formatos:", e);
        const alternativas = [
          { mimeType: "audio/mp4" },
          { mimeType: "audio/ogg;codecs=opus" },
          { mimeType: "audio/wav" },
        ];
        for (const alt of alternativas) {
          try {
            recorder = new MediaRecorder(stream, alt);
            console.log("Usando formato:", alt.mimeType);
            break;
          } catch (err) {
            continue;
          }
        }
        if (!recorder) {
          recorder = new MediaRecorder(stream);
        }
      }
      const audioChunks = [];
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };
      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, {
          type: recorder.mimeType || "audio/webm",
        });
        setProcessing(true);
        try {
          const response = await chatAPI.processarAudio(audioBlob, sessionId);
          if (response.texto_reconhecido) {
            onResult(response.texto_reconhecido, response);
          }
        } catch (error) {
          console.error("Erro ao processar áudio:", error);
          alert(
            `Erro ao processar áudio: ${
              error.response?.data?.detail || error.message
            }`
          );
        } finally {
          setProcessing(false);
        }
        stream.getTracks().forEach((track) => track.stop());
      };
      recorder.start(100);
      setMediaRecorder(recorder);
      setRecording(true);
    } catch (error) {
      console.error("Erro ao acessar microfone:", error);
      let errorMsg = "Erro ao acessar o microfone. ";
      if (error.name === "NotAllowedError") {
        errorMsg += "Permissão negada. Permita o acesso ao microfone.";
      } else if (error.name === "NotFoundError") {
        errorMsg += "Nenhum microfone encontrado.";
      } else {
        errorMsg += "Verifique as permissões e tente novamente.";
      }
      alert(errorMsg);
    }
  };
  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      setRecording(false);
      setMediaRecorder(null);
    }
  };
  const handleClick = () => {
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  };
  return (
    <button
      type="button"
      title={
        processing
          ? "Processando áudio..."
          : recording
          ? "Parar gravação"
          : "Gravar áudio"
      }
      onClick={handleClick}
      disabled={disabled || processing}
      className={
        "h-10 w-10 rounded-md border text-sm flex items-center justify-center " +
        (disabled || processing
          ? "bg-zinc-800 text-zinc-500 border-zinc-800"
          : "bg-white text-black border-zinc-300 hover:opacity-80")
      }
    >
      {processing ? "…" : recording ? "■" : "🎤"}
    </button>
  );
}
export default AudioRecorder;