import speech_recognition as sr
from sda import AssistenteNutricional


def obter_texto_do_audio():
    """
    Converte entrada de áudio em texto usando SpeechRecognition.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Configurações para reduzir sensibilidade
        recognizer.energy_threshold = 300  # Nível de ruído necessário para considerar como fala
        recognizer.dynamic_energy_threshold = True  # Ajusta automaticamente  sensibilidade
        recognizer.pause_threshold = 2  # Tempo de pausa permitido antes de parar a gravação (em segundos)

        print("\nEstou ouvindo... Fale agora.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=20)
            texto = recognizer.recognize_google(audio, language="pt-BR")
            print(f"\nVocê disse: {texto}")
            return texto
        except sr.WaitTimeoutError:
            print("\nTempo limite excedido. Tente novamente.")
        except sr.UnknownValueError:
            print("\nNão consegui entender o áudio. Tente novamente.")
        except sr.RequestError as e:
            print(f"\nErro na API de reconhecimento de fala: {str(e)}")
    return None


def obter_entrada(modo):
    """
    Obtém a entrada do usuário com base no modo escolhido (falar ou digitar).
    """
    if modo == "falar":
        texto = obter_texto_do_audio()
        if texto:
            return texto
    elif modo == "digitar":
        return input("\nDigite sua resposta: ")
    return None


def main():
    # Define o caminho para o arquivo JSON com a dieta do usuário
    arquivo_dieta = "dieta_usuario.json"
    
    # Cria uma instância do assistente nutricional
    assistente = AssistenteNutricional(arquivo_dieta)

    print("\nOlá! Sou seu assistente nutricional. Vamos começar analisando a sua refeição.")

    while True:
        # Pergunta o modo de entrada preferido do usuário
        modo_entrada = input("\nVocê deseja usar áudio ou texto? (falar/digitar ou 'sair' para encerrar): ").lower()
        
        if modo_entrada == "sair":
            print("\nAté mais! Lembre-se de seguir sua dieta. :)")
            break

        if modo_entrada not in ["falar", "digitar"]:
            print("\nOpção inválida. Escolha 'falar' ou 'digitar'.")
            continue

        try:
            while True:
                # Obtém a refeição inicial
                refeicao = obter_entrada(modo_entrada)
                
                if not refeicao:
                    continue  # Retorna ao início se não capturar entrada válida

                if refeicao.lower() == "sair":
                    print("\nAté mais! Lembre-se de seguir sua dieta. :)")
                    return

                if refeicao.lower() == "new":
                    print("\nReiniciando. Vamos começar novamente.")
                    break

                print("\nInterpretando a refeição...\n")
                # Analisa a refeição
                analise_detalhada = assistente.interpretar_refeicao(refeicao)
                print("\nAnálise detalhada da refeição:\n")
                print(analise_detalhada)

                # Gera uma resposta simplificada para o usuário
                resposta_simplificada = assistente.gerar_resposta_simplificada(analise_detalhada)
                print("\nResposta simplificada para você:\n")
                print(resposta_simplificada)

                while True:
                    # Pergunta ao usuário o modo de entrada para interagir novamente
                    modo_entrada = input("\nDeseja usar áudio ou texto para a próxima interação? (falar/digitar ou 'new' para recomeçar, 'sair' para encerrar): ").lower()
                    
                    if modo_entrada == "sair":
                        print("\nAté mais! Lembre-se de seguir sua dieta. :)")
                        return

                    if modo_entrada == "new":
                        print("\nReiniciando. Vamos começar novamente.")
                        break

                    if modo_entrada not in ["falar", "digitar"]:
                        print("\nOpção inválida. Escolha 'falar', 'digitar', 'new' ou 'sair'.")
                        continue

                    # Obtém a entrada no modo escolhido
                    comando = obter_entrada(modo_entrada)
                    
                    if not comando:
                        continue  # Retorna ao início se não capturar entrada válida

                    if comando.lower() == "sair":
                        print("\nAté mais! Lembre-se de seguir sua dieta. :)")
                        return

                    if comando.lower() == "new":
                        print("\nReiniciando. Vamos começar novamente.")
                        break

                    # Responde usando a IA Geral
                    resposta = assistente.ia_geral(comando)
                    print("\nResposta da IA Geral:\n")
                    print(resposta)

        except Exception as e:
            print(f"\nErro ao processar sua solicitação: {str(e)}")

if __name__ == "__main__":
    main()
