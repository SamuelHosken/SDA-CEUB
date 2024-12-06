from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
from sda import AssistenteNutricional

app = Flask(__name__)

# Instância do assistente nutricional
arquivo_dieta = "dieta_usuario.json"
assistente = AssistenteNutricional(arquivo_dieta)

# Variável global para controle do estado
modo_analise = True  # Define o estado inicial como "análise"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global modo_analise
    try:
        recognized_text = ""  # Variável para armazenar o texto reconhecido
        if "audio" in request.files:
            # Processa o áudio enviado
            recognizer = sr.Recognizer()
            audio_file = request.files["audio"]

            # Log para verificar se o áudio foi recebido
            print(f"Áudio recebido: {audio_file.filename}")

            # Converte o áudio para WAV usando pydub
            audio = AudioSegment.from_file(audio_file)
            wav_audio = BytesIO()
            audio.export(wav_audio, format="wav")
            wav_audio.seek(0)  # Retorna ao início do arquivo para leitura

            with sr.AudioFile(wav_audio) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)

            recognized_text = recognizer.recognize_google(audio_data, language="pt-BR")
            print(f"Texto reconhecido do áudio: {recognized_text}")

        else:
            # Processa texto enviado
            data = request.json
            recognized_text = data.get("message", "")

        if recognized_text.lower() == "sair":
            return jsonify({"response": "Encerrando o sistema. Até mais!", "recognized": recognized_text})

        if recognized_text.lower() == "new":
            modo_analise = True  # Reinicia o fluxo para análise
            return jsonify({"response": "Modo reiniciado. Por favor, informe sua última refeição.", "recognized": recognized_text})

        if modo_analise:
            # Etapa 1: Analisar a refeição
            analise_detalhada = assistente.interpretar_refeicao(recognized_text)
            print(f"Análise detalhada: {analise_detalhada}")

            # Etapa 2: Simplificar a análise
            resposta_simplificada = assistente.gerar_resposta_simplificada(analise_detalhada)
            print(f"Resposta simplificada: {resposta_simplificada}")

            # Atualiza o modo para sair do estado de análise
            modo_analise = False

            return jsonify({
                "response": resposta_simplificada,
                "recognized": recognized_text
            })
        else:
            # Estado contínuo: utiliza apenas a IA Geral
            resposta_final = assistente.ia_geral(recognized_text)
            print(f"Resposta final: {resposta_final}")
            return jsonify({"response": resposta_final, "recognized": recognized_text})

    except sr.UnknownValueError:
        print("Erro: Não consegui entender o áudio.")
        return jsonify({"response": "Não consegui entender o áudio. Tente novamente.", "recognized": "Áudio não reconhecido"})
    except sr.RequestError as e:
        print(f"Erro na API de reconhecimento de fala: {str(e)}")
        return jsonify({"response": f"Erro ao processar o áudio: {str(e)}", "recognized": "Erro na API"})
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        return jsonify({"response": f"Erro ao processar sua solicitação: {str(e)}", "recognized": "Erro geral"})


if __name__ == "__main__":
    app.run(debug=True)