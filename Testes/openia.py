import openai
import json
from datetime import datetime

# Configuração da API OpenAI
openai.api_key = "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"

# Função para carregar a dieta do usuário
def carregar_dieta(arquivo_dieta):
    """
    Carrega a dieta do usuário a partir de um arquivo JSON.
    """
    with open(arquivo_dieta, "r") as file:
        dieta = json.load(file)
    return dieta

# Função para salvar a dieta atualizada
def salvar_dieta(arquivo_dieta, dieta):
    """
    Salva a dieta atualizada em um arquivo JSON.
    """
    with open(arquivo_dieta, "w") as file:
        json.dump(dieta, file, indent=4)

# Função para obter o horário e a data atuais
def obter_informacoes_tempo():
    """
    Retorna informações sobre o horário e a data atual.
    """
    agora = datetime.now()
    horario = agora.strftime("%H:%M")
    dia_semana = agora.strftime("%A")  # Ex: Monday
    data_completa = agora.strftime("%d de %B de %Y")  # Ex: 18 de November de 2024
    return horario, dia_semana, data_completa

# Função para interpretar a refeição e comparar com a dieta
def interpretar_refeicao(descricao, dieta):
    """
    Envia a descrição da refeição para a OpenAI e compara com a dieta do usuário.
    """
    horario, dia_semana, data_completa = obter_informacoes_tempo()

    # Formata a dieta para ser incluída na mensagem
    dieta_texto = "\n".join([f"{refeicao}: {detalhes}" for refeicao, detalhes in dieta.items()])
    
    # Monta o prompt para a OpenAI
    prompt = (
        "Você é um nutricionista virtual especializado em emagrecimento. Analise detalhadamente a refeição descrita abaixo "
        "e compare-a com a dieta do usuário, considerando todos os aspectos mencionados pelo usuário. Forneça uma análise "
        "completa e categorizada, destacando erros e acertos, e sugira ações práticas para o dia seguinte, alinhadas com o "
        "objetivo de emagrecimento.\n\n"
        f"Informações atuais:\n"
        f"- Horário: {horario}\n"
        f"- Dia da semana: {dia_semana}\n"
        f"- Data: {data_completa}\n\n"
        f"Dieta do usuário:\n{dieta_texto}\n\n"
        f"Refeição consumida:\n{descricao}\n\n"
        "Sua resposta deve incluir:\n"
        "1. Calorias estimadas.\n"
        "2. Comparação com a dieta.\n"
        "3. Erros cometidos.\n"
        "4. Acertos na refeição.\n"
        "5. Direção para o próximo dia.\n"
        "6. Observações nutricionais."
    )

    # Chama a API OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um nutricionista."},
            {"role": "user", "content": prompt}
        ]
    )

    # Retorna a resposta do modelo
    return response["choices"][0]["message"]["content"]

# Função para modificar a dieta
def modificar_dieta(dieta, alteracao):
    """
    Modifica a dieta com base na solicitação do usuário.
    """
    prompt = (
        "Você é um assistente nutricional. Abaixo está a dieta atual do usuário. Ele quer fazer uma modificação, e você "
        "precisa atualizar a dieta considerando as necessidades nutricionais. Após entender o pedido, modifique a dieta "
        "e retorne o texto atualizado.\n\n"
        f"Dieta atual:\n{json.dumps(dieta, indent=4)}\n\n"
        f"Solicitação de alteração:\n{alteracao}\n\n"
        "Retorne apenas a dieta atualizada em formato JSON."
    )

    # Chama a API OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente nutricional especializado em ajuste de dietas."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Atualiza a dieta com a resposta da IA
    dieta_atualizada = json.loads(response["choices"][0]["message"]["content"])
    return dieta_atualizada

# Função principal com interação contínua
def main():
    # Caminho do arquivo com a dieta do usuário
    arquivo_dieta = "dieta_usuario.json"
    
    # Carrega a dieta do usuário
    dieta = carregar_dieta(arquivo_dieta)

    print("\nOlá! Sou seu assistente nutricional. Você pode descrever uma refeição, perguntar sobre sua dieta ou pedir ajustes.")
    print("Por exemplo:\n- \"Comi um Big Mac no almoço.\"\n- \"Quero mudar minha refeição da noite.\"\n- \"Qual é a minha dieta para o café da manhã?\"")
    
    while True:
        entrada_usuario = input("\nDigite sua pergunta ou refeição (ou 'sair' para encerrar): ")
        if entrada_usuario.lower() == "sair":
            print("\nAté mais! Lembre-se de seguir sua dieta. :)")
            break
        
        try:
            # Verificar se o usuário está pedindo para alterar a dieta
            if "mudar" in entrada_usuario.lower() or "alterar" in entrada_usuario.lower():
                dieta = modificar_dieta(dieta, entrada_usuario)
                salvar_dieta(arquivo_dieta, dieta)
                print("\nDieta atualizada com sucesso!")
            # Verificar se o usuário está pedindo sobre a dieta
            elif "qual" in entrada_usuario.lower() and "dieta" in entrada_usuario.lower():
                print("\nSua dieta atual:\n")
                print(json.dumps(dieta, indent=4))
            # Caso contrário, interpretar como uma descrição de refeição
            else:
                resultado_gpt = interpretar_refeicao(entrada_usuario, dieta)
                print("\nAnálise detalhada da sua refeição:\n")
                print(resultado_gpt)
        except Exception as e:
            print("\nErro ao processar sua solicitação:", e)

if __name__ == "__main__":
    main()
