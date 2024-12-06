from config import openai
from utils import obter_informacoes_tempo

def interpretar_refeicao(descricao, dieta):
    """
    Envia a descrição da refeição para a OpenAI e compara com a dieta do usuário.
    """
    horario, dia_semana, data_completa = obter_informacoes_tempo()

    dieta_texto = "\n".join([f"{refeicao}: {detalhes}" for refeicao, detalhes in dieta.items()])
    
    prompt = (
        "Você é um nutricionista virtual especializado em emagrecimento. Analise detalhadamente a refeição descrita abaixo "
        "e compare-a com a dieta do usuário.\n\n"
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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um nutricionista."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]

def gerar_resposta_simplificada(analise_detalhada):
    """
    Simplifica a análise detalhada da refeição para uma resposta objetiva e prática.
    """
    prompt = (
        "Você é um assistente nutricional inteligente. Sua tarefa é pegar a análise detalhada de um nutricionista e criar uma resposta simples, "
        "clara e prática para o usuário. O foco deve ser:\n"
        "- Quantas calorias foram ingeridas.\n"
        "- Se a refeição está alinhada com a dieta ou não.\n"
        "- O que o usuário deve ajustar para melhorar.\n"
        "Analise detalhada do nutricionista:\n"
        f"{analise_detalhada}\n\n"
        "Sua resposta deve ser breve e fácil de entender."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente nutricional prático e claro."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response["choices"][0]["message"]["content"]
