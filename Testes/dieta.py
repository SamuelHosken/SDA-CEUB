import json
from config import openai

def carregar_dieta(arquivo_dieta):
    """
    Carrega a dieta do usuário a partir de um arquivo JSON.
    """
    with open(arquivo_dieta, "r") as file:
        dieta = json.load(file)
    return dieta

def salvar_dieta(arquivo_dieta, dieta):
    """
    Salva a dieta atualizada em um arquivo JSON.
    """
    with open(arquivo_dieta, "w") as file:
        json.dump(dieta, file, indent=4)

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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente nutricional especializado em ajuste de dietas."},
            {"role": "user", "content": prompt}
        ]
    )
    
    dieta_atualizada = json.loads(response["choices"][0]["message"]["content"])
    return dieta_atualizada
