import json
from config import openai
from utils import obter_informacoes_tempo
from geopy.geocoders import Nominatim
import requests

class AssistenteNutricional:
    def __init__(self, arquivo_dieta):
        self.arquivo_dieta = arquivo_dieta
        self.dieta = self.carregar_dieta()
        self.historico_respostas = []  # Para manter o contexto das interações

    def carregar_dieta(self):
        with open(self.arquivo_dieta, "r") as file:
            return json.load(file)

    def salvar_dieta(self):
        with open(self.arquivo_dieta, "w") as file:
            json.dump(self.dieta, file, indent=4)

    def modificar_dieta(self, alteracao):
        prompt = (
            "Você é um assistente nutricional. Abaixo está a dieta atual do usuário. Ele quer fazer uma modificação, e você "
            "precisa atualizar a dieta considerando as necessidades nutricionais. Após entender o pedido, modifique a dieta "
            "e retorne o texto atualizado.\n\n"
            f"Dieta atual:\n{json.dumps(self.dieta, indent=4)}\n\n"
            f"Solicitação de alteração:\n{alteracao}\n\n"
            "Retorne apenas a dieta atualizada em formato JSON."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente nutricional especializado em ajuste de dietas."},
                {"role": "user", "content": prompt}
            ]
        )
        
        self.dieta = json.loads(response["choices"][0]["message"]["content"])
        self.salvar_dieta()

    def interpretar_refeicao(self, descricao):
            # Obter informações contextuais adicionais
            dia_semana, data_completa = obter_informacoes_tempo()[1:]  # Somente dia e data

            # Formatar a dieta como texto para o prompt
            dieta_texto = "\n".join([f"{refeicao}: {detalhes}" for refeicao, detalhes in self.dieta.items()])

            # Prompt atualizado para focar no contexto dos alimentos
            prompt = (
                f"Seu objetivo é analisar a refeição relatada e identificar qual refeição planejada na dieta do usuário ela representa, com base no tipo de alimentos, porções e descrição geral.\n\n"
                f"Dieta planejada do usuário:\n{dieta_texto}\n\n"
                f"Refeição relatada pelo usuário:\n{descricao}\n\n"
                "Com base no contexto, responda as seguintes perguntas:\n"
                "1. Qual refeição planejada na dieta (ex: café da manhã, almoço, lanche, jantar) mais se aproxima da refeição relatada?\n"
                "2. Quais as diferenças entre a refeição relatada e a refeição planejada (calorias, alimentos, porções, e macronutrientes)?\n"
                "3. Sugestões de ajustes ou compensações para equilibrar a dieta com base na refeição relatada.\n"
                "4. Quantas calorias foram ingeridas e o saldo de calorias permitido para o restante do dia.\n"
            )

            try:
                # Chamada à API GPT para gerar a análise
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é um nutricionista virtual chamado SDA (Smart Diet Assistant). "},
                        {"role": "user", "content": prompt}
                    ]
                )

                # Processar a resposta gerada pelo GPT
                resultado = response["choices"][0]["message"]["content"]
                self.historico_respostas.append(resultado)
                return resultado
            except Exception as e:
                # Lidando com erros na API
                erro_msg = f"Erro ao processar a refeição: {str(e)}"
                self.historico_respostas.append(erro_msg)
                return erro_msg


    def gerar_resposta_simplificada(self, analise_detalhada):
        dieta_texto = "\n".join([f"{refeicao}: {detalhes}" for refeicao, detalhes in self.dieta.items()])

        prompt = (
            f"Simplifique ao maximo a análise abaixo para uma resposta breve, prática e clara para o usuário. "
            f"Leve em conta a dieta atual para orientar melhor o usuário:\n\n"
            f"Dieta do usuário:\n{dieta_texto}\n\n"
            f"Análise detalhada da refeição:\n{analise_detalhada}\n\n"
            "Responda de forma objetiva, incluindo:\n"
            "1. Qual refeição do dia foi analisada.\n"
            "2. Quantas calorias foram ingeridas e o saldo restante.\n"
            "3. Pontos positivos da refeição.\n"
            "4. Orientações práticas ou ajustes necessários.\n"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente nutricional prático que fornece respostas claras e objetivas."},
                {"role": "user", "content": prompt}
            ]
        )

        resultado = response["choices"][0]["message"]["content"]
        self.historico_respostas.append(resultado)
        return resultado
    
    def obter_localizacao(self):
        """
        Obtém a localização do usuário (cidade e país) usando uma API de geolocalização baseada em IP.
        """
        try:
            # Faz uma requisição para uma API de geolocalização gratuita
            response = requests.get("http://ip-api.com/json/")
            if response.status_code == 200:
                dados = response.json()
                cidade = dados.get("city", "Desconhecida")
                pais = dados.get("country", "Desconhecido")
                return f"{cidade}, {pais}"
            return "Localização desconhecida"
        except Exception as e:
            return f"Erro ao obter localização: {str(e)}"

    def ia_geral(self, comando):
        """
        IA Geral que responde a comandos relacionados à dieta, compras e outros contextos.
        """
        horario, dia_semana, data_completa = obter_informacoes_tempo()
        localizacao = self.obter_localizacao()

        dieta_texto = "\n".join([f"{refeicao}: {detalhes}" for refeicao, detalhes in self.dieta.items()])
        historico = "\n\n".join(self.historico_respostas[-3:])  # Usa até 3 interações anteriores como contexto
        
        prompt = (
            "Você é um assistente nutricional geral. Responda a perguntas do usuário sobre sua dieta, horários de refeição, "
            "e análise de refeições anteriores. Use o contexto fornecido para criar uma resposta prática e direta.\n\n"
            "Sempre formate o texto com um titulo e um texto, mas continue sendo breve e diretamente aplicável ao comando do usuário.\n\n"
            f"Contexto atual:\n"
            f"- Horário: {horario}\n"
            f"- Dia da semana: {dia_semana}\n"
            f"- Data: {data_completa}\n"
            f"- Localização: {localizacao}\n\n"
            f"Dieta atual:\n{dieta_texto}\n\n"
            f"Histórico de interações recentes:\n{historico}\n\n"
            f"Comando do usuário:\n{comando}\n\n"
            "Responda da forma mais breve e resumida possível."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente nutricional prático e claro."},
                {"role": "user", "content": prompt}
            ]
        )

        resultado = response["choices"][0]["message"]["content"]
        self.historico_respostas.append(resultado)
        return resultado