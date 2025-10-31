#!/usr/bin/env python3
import json
import datetime
import re
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from openai import OpenAI
from app.config import settings
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import os
@dataclass
class EstadoNutricional:
    calorias_consumidas_dia: float = 0
    calorias_consumidas_semana: float = 0
    calorias_consumidas_mes: float = 0
    hidratacao_dia: float = 0
    hidratacao_semana: float = 0
    hidratacao_mes: float = 0
    macros_dia: Dict[str, float] = None
    refeicoes_registradas: List[Dict] = None
    ultima_refeicao: Optional[Dict] = None
    historico_conversas: List[str] = None
    def __post_init__(self):
        if self.macros_dia is None:
            self.macros_dia = {'proteinas': 0, 'carboidratos': 0, 'gorduras': 0, 'fibras': 0}
        if self.refeicoes_registradas is None:
            self.refeicoes_registradas = []
        if self.historico_conversas is None:
            self.historico_conversas = []
class AgenteSDAInteligente:
    def __init__(self, arquivo_dieta: str = None, dieta_dict: Dict = None):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.openai_model = settings.openai_model
        self.geolocator = Nominatim(user_agent="SDA_NutricionalAgent")
        if dieta_dict:
            self.dieta = dieta_dict
        elif arquivo_dieta:
            self.dieta = self.carregar_dieta(arquivo_dieta)
        else:
            self.dieta = self.carregar_dieta("dieta_usuario.json")
        self.metas = self._calcular_metas_da_dieta()
        self.estado = EstadoNutricional()
    def _calcular_metas_da_dieta(self) -> Dict:
        calorias_diaria = self.dieta.get('calories', {}).get('daily', 2600)
        calorias_semanal = self.dieta.get('calories', {}).get('weekly', calorias_diaria * 7)
        calorias_mensal = self.dieta.get('calories', {}).get('monthly', calorias_diaria * 30)
        hidratacao_diaria = self.dieta.get('hydration', {}).get('daily', 3.5)
        macros = self.dieta.get('macronutrients', {})
        protein_pct = macros.get('protein', {}).get('percentage', 25)
        carb_pct = macros.get('carbohydrates', {}).get('percentage', 43)
        fat_pct = macros.get('fats', {}).get('percentage', 26)
        fiber_g = macros.get('fiber', 30)
        return {
            'calorias_diaria': calorias_diaria,
            'calorias_semanal': calorias_semanal,
            'calorias_mensal': calorias_mensal,
            'hidratacao_diaria': hidratacao_diaria,
            'macros_alvo': {
                'proteinas_pct': protein_pct,
                'carboidratos_pct': carb_pct,
                'gorduras_pct': fat_pct,
                'fibras_g': fiber_g
            }
        }
    def carregar_dieta(self, arquivo: str) -> Dict:
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        arquivo_path = os.path.join(base_dir, 'backend', arquivo)
        if not os.path.exists(arquivo_path):
            arquivo_path = os.path.join(os.path.dirname(__file__), '..', '..', arquivo)
        try:
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.criar_dieta_padrao()
    def criar_dieta_padrao(self) -> Dict:
        return {
            "calories": {"daily": 2600},
            "daily_meals": {
                "weekdays": {
                    "breakfast": {"time": "06:00", "calories": 520, "items": ["Aveia com frutas", "Café com leite"]},
                    "pre_workout": {"time": "11:00", "calories": 260, "items": ["Banana", "Whey protein"]},
                    "post_workout": {"time": "13:00", "calories": 520, "items": ["Frango grelhado", "Arroz integral"]},
                    "afternoon_snack": {"time": "16:00", "calories": 390, "items": ["Iogurte grego", "Castanhas"]},
                    "dinner": {"time": "20:00", "calories": 650, "items": ["Salmão", "Batata doce"]},
                    "evening_snack": {"time": "22:00", "calories": 260, "items": ["Caseína", "Amêndoas"]}
                }
            }
        }
    def detectar_localizacao_na_mensagem(self, mensagem: str) -> Optional[str]:
        padroes_localizacao = [
            r'estou (no|na|em|perto do|perto da|próximo ao|próximo da|ao lado do|ao lado da) (.+?)(?:\s+e\s+|\s+o\s+que|\s+qual|\s+onde|\.|$)',
            r'estou em (.+?)(?:\s+e\s+|\s+o\s+que|\s+qual|\s+onde|\.|$)',
            r'aqui (no|na|em) (.+?)(?:\s+e\s+|\s+o\s+que|\s+qual|\s+onde|\.|$)',
            r'me encontro (no|na|em) (.+?)(?:\s+e\s+|\s+o\s+que|\s+qual|\s+onde|\.|$)',
            r'localizado (no|na|em) (.+?)(?:\s+e\s+|\s+o\s+que|\s+qual|\s+onde|\.|$)'
        ]
        for padrao in padroes_localizacao:
            match = re.search(padrao, mensagem.lower())
            if match:
                localizacao = match.groups()[-1].strip()
                localizacao = re.sub(r'[.!?]+$', '', localizacao)
                return localizacao
        pontos_famosos = [
            'coliseu', 'torre eiffel', 'cristo redentor', 'times square', 'big ben',
            'sagrada familia', 'machu picchu', 'taj mahal', 'opera house'
        ]
        for ponto in pontos_famosos:
            if ponto in mensagem.lower():
                if 'coliseu' in mensagem.lower():
                    return 'Colosseum, Rome, Italy'
                elif 'torre eiffel' in mensagem.lower():
                    return 'Eiffel Tower, Paris, France'
                else:
                    return ponto
        return None
    def obter_coordenadas(self, localizacao: str) -> Optional[tuple]:
        try:
            location = self.geolocator.geocode(localizacao, timeout=10)
            if location:
                return (location.latitude, location.longitude)
        except (GeocoderTimedOut, Exception) as e:
            print(f"Erro ao geocodificar {localizacao}: {e}")
        return None
    def buscar_restaurantes_proximos(self, latitude: float, longitude: float, radius: int = 1000) -> List[Dict]:
        try:
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json][timeout:25];
            (
              node["amenity"="restaurant"](around:{radius},{latitude},{longitude});
              node["amenity"="fast_food"](around:{radius},{latitude},{longitude});
              node["amenity"="cafe"](around:{radius},{latitude},{longitude});
            );
            out body;
            """
            response = requests.get(overpass_url, params={'data': overpass_query}, timeout=30)
            data = response.json()
            restaurantes = []
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                if 'name' in tags:
                    restaurante = {
                        'nome': tags.get('name', 'Restaurante sem nome'),
                        'tipo': tags.get('amenity', 'restaurant'),
                        'cozinha': tags.get('cuisine', 'Não especificada'),
                        'latitude': element.get('lat'),
                        'longitude': element.get('lon'),
                        'endereco': tags.get('addr:street', '')
                    }
                    restaurantes.append(restaurante)
            return restaurantes[:10]
        except Exception as e:
            print(f"Erro ao buscar restaurantes: {e}")
            return []
    def processar_com_ia(self, mensagem_usuario: str) -> Dict:
        agora = datetime.datetime.now()
        contexto_temporal = f"Horário atual: {agora.strftime('%H:%M')} - {agora.strftime('%A, %d/%m/%Y')}"
        historico_recente = "\n".join(self.estado.historico_conversas[-3:]) if self.estado.historico_conversas else "Primeira interação"
        palavras_planejamento = ['planejamento', 'plano', 'cardápio', 'cardapio', 'me mostre', 'mostra', 'refeições', 'refeicoes', 'diário', 'diario']
        is_planejamento = any(palavra in mensagem_usuario.lower() for palavra in palavras_planejamento)
        prompt_completo = f"""
        {self.criar_prompt_agente_ia()}
        CONTEXTO TEMPORAL: {contexto_temporal}
        HISTÓRICO RECENTE:
        {historico_recente}
        MENSAGEM DO USUÁRIO: {mensagem_usuario}
        {'🚨 ATENÇÃO: Esta mensagem está pedindo PLANEJAMENTO DIÁRIO! Você DEVE mostrar todas as 6 refeições detalhadas!' if is_planejamento else ''}
        Como agente IA, interprete esta mensagem e responda adequadamente usando sua inteligência artificial.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "Você é um agente de IA superinteligente especializado em nutrição. SEMPRE retorne APENAS um JSON válido sem explicações extras."},
                    {"role": "user", "content": prompt_completo}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            resultado_texto = (response.choices[0].message.content or "").strip()
            try:
                if resultado_texto.startswith('```'):
                    resultado_texto = resultado_texto.split('\n', 1)[1].rsplit('\n', 1)[0]
                inicio_json = resultado_texto.find('{')
                fim_json = resultado_texto.rfind('}') + 1
                if inicio_json != -1 and fim_json != 0:
                    resultado_texto = resultado_texto[inicio_json:fim_json]
                resultado = json.loads(resultado_texto)
                if resultado.get('tipo') == 'registro_refeicao':
                    self.atualizar_estado_nutricional(resultado)
                return resultado
            except json.JSONDecodeError:
                return {
                    "tipo": "conversa_geral",
                    "resposta_usuario": resultado_texto
                }
        except Exception as e:
            return {
                "tipo": "erro",
                "resposta_usuario": f"Desculpe, houve um erro ao processar sua mensagem. Pode tentar novamente? Erro: {str(e)}"
            }
    def atualizar_estado_nutricional(self, resultado: Dict):
        if resultado.get('tipo') == 'registro_refeicao':
            calorias = resultado.get('calorias_estimadas', 0)
            self.estado.calorias_consumidas_dia += calorias
            macros = resultado.get('macros', {})
            self.estado.macros_dia['proteinas'] += macros.get('proteina_g', 0)
            self.estado.macros_dia['carboidratos'] += macros.get('carboidratos_g', 0)
            self.estado.macros_dia['gorduras'] += macros.get('gorduras_g', 0)
            self.estado.macros_dia['fibras'] += macros.get('fibras_g', 0)
            refeicao = {
                'descricao': resultado.get('alimento', ''),
                'horario': datetime.datetime.now().strftime("%H:%M"),
                'calorias': calorias,
                'macros': macros,
                'timestamp': datetime.datetime.now().isoformat()
            }
            self.estado.refeicoes_registradas.append(refeicao)
            self.estado.ultima_refeicao = refeicao
    def criar_prompt_agente_ia(self) -> str:
        return f"""
        Você é o SDA (Sistema Digital de Alimentação), um AGENTE DE IA SUPERINTELIGENTE especializado em nutrição.
        CARACTERÍSTICAS DO AGENTE:
        - Você interpreta QUALQUER entrada usando inteligência artificial
        - Não usa regras pré-definidas, você PENSA e DECIDE
        - Você é capaz de entender contexto, emoções, intenções e sutilezas
        - Você aprende com cada interação e se adapta
        SUAS CAPACIDADES COMO AGENTE IA:
        1. INTERPRETAÇÃO INTELIGENTE: Analise a entrada e decida se é:
           - Registro de refeição (qualquer alimento mencionado)
           - Pergunta sobre nutrição/planejamento
           - Pedido de orientação
           - Consulta sobre restaurantes/localizações
           - Expressão de sentimento/frustração
           - Pedido de ajuda ou motivação
        2. EXTRAÇÃO DE INFORMAÇÕES: Se for refeição, extraia:
           - Alimento(s) consumido(s)
           - Quantidade aproximada
           - Horário (se mencionado)
           - Contexto emocional
        3. DETECÇÃO DE LOCALIZAÇÃO: Se mencionada localização, extraia:
           - Local específico mencionado
           - Contexto da consulta (buscar restaurante, refeição, etc.)
           - Tipo de estabelecimento desejado
        4. CÁLCULO NUTRICIONAL: Estime macronutrientes usando sua base de conhecimento
        5. SUGESTÕES GEOLOCALIZADAS: Para consultas de localização:
           - Identifique a próxima refeição planejada
           - Considere as calorias necessárias para essa refeição
           - Sugira pratos específicos em restaurantes próximos
           - Mantenha o foco nutricional do plano alimentar
        6. AJUSTE AUTOMÁTICO DE DIETA: Se perguntado sobre planejamento:
           - Calcule calorias restantes para o dia
           - Ajuste as próximas refeições automaticamente
           - Redistribua as calorias nas refeições restantes
           - Mantenha proporções de macronutrientes
        7. RESPOSTA CONTEXTUAL: Gere resposta personalizada considerando:
           - Estado nutricional atual
           - Metas do usuário
           - Contexto emocional
           - Localização (se mencionada)
           - Histórico de conversas
        ESTADO NUTRICIONAL ATUAL:
        - Calorias consumidas hoje: {self.estado.calorias_consumidas_dia} kcal
        - Meta diária: {self.metas['calorias_diaria']} kcal
        - Calorias restantes: {self.metas['calorias_diaria'] - self.estado.calorias_consumidas_dia} kcal
        - Status: {'EXCEDEU A META' if self.estado.calorias_consumidas_dia > self.metas['calorias_diaria'] else 'DENTRO DA META'}
        - Proteínas: {self.estado.macros_dia['proteinas']:.1f}g
        - Carboidratos: {self.estado.macros_dia['carboidratos']:.1f}g
        - Gorduras: {self.estado.macros_dia['gorduras']:.1f}g
        - Hidratação: {self.estado.hidratacao_dia}L de {self.metas['hidratacao_diaria']}L
        - Refeições registradas hoje: {len(self.estado.refeicoes_registradas)}
        - Última refeição: {self.estado.ultima_refeicao['descricao'] if self.estado.ultima_refeicao else 'Nenhuma registrada'}
        PLANO ALIMENTAR BASE (ajuste conforme necessário):
        {json.dumps(self.dieta.get('daily_meals', {}), indent=2, ensure_ascii=False)}
        INSTRUÇÕES PARA PLANEJAMENTO:
        Se o usuário perguntar sobre "planejamento", "plano diário", "cardápio" ou similar:
        1. Use o plano base acima
        2. Calcule calorias restantes: {self.metas['calorias_diaria']} - {self.estado.calorias_consumidas_dia} = {self.metas['calorias_diaria'] - self.estado.calorias_consumidas_dia} kcal
        3. Ajuste as próximas refeições redistribuindo as calorias restantes
        4. Mostre TODAS as 6 refeições do dia com detalhes completos
        INSTRUÇÕES DE RESPOSTA:
        1. Se identificar registro de refeição, retorne JSON:
        {{
            "tipo": "registro_refeicao",
            "alimento": "descrição do alimento",
            "calorias_estimadas": 000,
            "macros": {{
                "proteina_g": 00.0,
                "carboidratos_g": 00.0,
                "gorduras_g": 00.0,
                "fibras_g": 0.0
            }},
            "resposta_usuario": "resposta amigável e contextual"
        }}
        2. Se perguntado sobre planejamento diário, SEMPRE retorne:
        {{
            "tipo": "planejamento_diario",
            "resposta_usuario": "Seu plano alimentar ajustado para hoje:\n\n1. Café da manhã (06:00) - 520 kcal\n- 4 ovos (3 claras e 1 inteiro)\n- 2 fatias de pão integral\n- 1/3 de abacate\n- 5g de creatina com água\n- Café preto sem açúcar\n\n2. Pré-treino (11:00) - 260 kcal\n- 1 banana\n- 1 dose de whey protein\n\n[CONTINUE COM TODAS AS 6 REFEIÇÕES]\n\n📊 RESUMO:\nCalorias já consumidas: XXX kcal\nCalorias restantes: XXX kcal\nStatus: [DENTRO/EXCEDEU] da meta de 2600 kcal"
        }}
        OBRIGATÓRIO: Mostre TODAS as 6 refeições completas com alimentos específicos, horários e calorias ajustadas!
        3. Se detectar consulta sobre localização/restaurantes, retorne JSON:
        {{
            "tipo": "consulta_localizacao",
            "localizacao_detectada": "local mencionado pelo usuário",
            "resposta_usuario": "resposta indicando que vou buscar restaurantes próximos"
        }}
        4. Para outras interações, retorne JSON:
        {{
            "tipo": "conversa_geral",
            "resposta_usuario": "resposta completa e contextual"
        }}
        PERSONALIDADE:
        - Amigável e motivacional
        - Técnico quando necessário
        - Empático com deslizes
        - Proativo em sugestões
        - Celebra conquistas
        - Usa linguagem natural brasileira
        LEMBRE-SE: Você é um AGENTE IA, não um sistema de regras. PENSE, INTERPRETE e RESPONDA!
        """
    def conversar(self, mensagem: str) -> str:
        self.estado.historico_conversas.append(f"Usuário: {mensagem}")
        localizacao = self.detectar_localizacao_na_mensagem(mensagem)
        palavras_comida = ['restaurante', 'comer', 'almoç', 'jant', 'lanche', 'refeição', 'prato', 'comida', 'onde posso']
        tem_contexto_comida = any(palavra in mensagem.lower() for palavra in palavras_comida)
        if localizacao and tem_contexto_comida:
            resposta = self.processar_consulta_localizacao(mensagem, localizacao)
        else:
            resultado = self.processar_com_ia(mensagem)
            resposta = resultado.get('resposta_usuario', 'Desculpe, não consegui processar sua mensagem.')
        self.estado.historico_conversas.append(f"SDA: {resposta}")
        return resposta
    def processar_consulta_localizacao(self, mensagem: str, localizacao: str) -> str:
        try:
            coordenadas = self.obter_coordenadas(localizacao)
            if not coordenadas:
                return f"Não consegui encontrar a localização '{localizacao}'. Pode tentar ser mais específico?"
            latitude, longitude = coordenadas
            restaurantes = self.buscar_restaurantes_proximos(latitude, longitude, radius=2000)
            if not restaurantes:
                return f"Não encontrei restaurantes próximos ao {localizacao}. Vou te dar sugestões gerais para sua próxima refeição."
            proxima_refeicao = self.obter_proxima_refeicao_planejada()
            return self.gerar_sugestoes_geolocalizadas(localizacao, restaurantes, proxima_refeicao, mensagem)
        except Exception as e:
            return f"Houve um erro ao buscar restaurantes. Vou te dar sugestões gerais para sua próxima refeição."
    def obter_proxima_refeicao_planejada(self) -> Dict:
        agora = datetime.datetime.now()
        hora_atual = agora.time()
        refeicoes = self.dieta.get('daily_meals', {}).get('weekdays', {})
        refeicoes_ordenadas = []
        for nome, dados in refeicoes.items():
            hora_refeicao = datetime.datetime.strptime(str(dados['time']).zfill(5), '%H:%M').time()
            refeicoes_ordenadas.append((nome, hora_refeicao, dados))
        refeicoes_ordenadas.sort(key=lambda x: x[1])
        for nome, hora, dados in refeicoes_ordenadas:
            if hora > hora_atual:
                return {
                    'nome': nome,
                    'hora': dados['time'],
                    'calorias': dados['calories'],
                    'items': dados.get('items', [])
                }
        if refeicoes_ordenadas:
            nome, hora, dados = refeicoes_ordenadas[0]
            return {
                'nome': nome,
                'hora': dados['time'],
                'calorias': dados['calories'],
                'items': dados.get('items', [])
            }
        return {'nome': 'almoço', 'hora': '12:00', 'calorias': 650, 'items': []}
    def gerar_sugestoes_geolocalizadas(self, localizacao: str, restaurantes: List[Dict], 
                                     proxima_refeicao: Dict, mensagem_original: str) -> str:
        lista_restaurantes = "\n".join([
            f"- {r['nome']} ({r['tipo']}, cozinha: {r['cozinha']})"
            for r in restaurantes[:8]
        ])
        prompt_geolocalizacao = f"""
        Você é um nutricionista especializado que está ajudando seu paciente a escolher uma refeição adequada.
        SITUAÇÃO:
        - Paciente está localizado próximo ao: {localizacao}
        - Próxima refeição planejada: {proxima_refeicao['nome']} às {proxima_refeicao['hora']}
        - Calorias necessárias para esta refeição: {proxima_refeicao['calorias']} kcal
        - Calorias já consumidas hoje: {self.estado.calorias_consumidas_dia} kcal
        - Meta diária: {self.metas['calorias_diaria']} kcal
        RESTAURANTES PRÓXIMOS ENCONTRADOS:
        {lista_restaurantes}
        MENSAGEM ORIGINAL DO PACIENTE:
        {mensagem_original}
        INSTRUÇÕES:
        1. Escolha 2-3 restaurantes mais adequados da lista
        2. Para cada restaurante, sugira 1-2 pratos específicos que:
           - Tenham aproximadamente {proxima_refeicao['calorias']} kcal
           - Sejam nutritivos e equilibrados
           - Sejam típicos do tipo de cozinha do restaurante
        3. Dê dicas de como ajustar as porções se necessário
        4. Mantenha o tom amigável e prático
        5. Use emojis para tornar a resposta mais visual
        Responda de forma direta e útil, como um nutricionista experiente ajudando seu paciente.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "Você é um nutricionista experiente que dá sugestões práticas e específicas. Use linguagem natural brasileira."},
                    {"role": "user", "content": prompt_geolocalizacao}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return (response.choices[0].message.content or "").strip()
        except Exception as e:
            nomes_restaurantes = [r['nome'] for r in restaurantes[:5]]
            return f"""Perfeito! Encontrei restaurantes próximos ao {localizacao}!

Restaurantes encontrados:
{chr(10).join([f"• {nome}" for nome in nomes_restaurantes])}

Para sua próxima refeição ({proxima_refeicao['nome']} - {proxima_refeicao['calorias']} kcal):

Sugestões nutricionais:
• Procure pratos com proteína magra (frango, peixe, carne vermelha magra)
• Inclua carboidratos complexos (arroz integral, batata, massas)
• Não esqueça dos vegetais (saladas, legumes grelhados)
• Evite frituras e molhos muito calóricos

Dica: Peça porções moderadas e, se necessário, complemente com uma entrada leve ou divida o prato!

Isso vai manter você dentro das {proxima_refeicao['calorias']} kcal planejadas para esta refeição!"""
    def get_status_nutricional(self) -> Dict:
        return {
            'calorias_consumidas': self.estado.calorias_consumidas_dia,
            'meta_calorias': self.metas['calorias_diaria'],
            'calorias_restantes': self.metas['calorias_diaria'] - self.estado.calorias_consumidas_dia,
            'percentual_meta': (self.estado.calorias_consumidas_dia / self.metas['calorias_diaria']) * 100 if self.metas['calorias_diaria'] else 0,
            'macros_consumidos': self.estado.macros_dia.copy(),
            'refeicoes_hoje': len(self.estado.refeicoes_registradas),
            'refeicoes': self.estado.refeicoes_registradas.copy(),
            'hidratacao': self.estado.hidratacao_dia
        }
    def salvar_estado(self, arquivo: str = None, estado_dict: Dict = None):
        if estado_dict:
            for key, value in estado_dict.items():
                if hasattr(self.estado, key):
                    setattr(self.estado, key, value)
        elif arquivo:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.estado), f, indent=2, ensure_ascii=False, default=str)
    def carregar_estado(self, arquivo: str = None, estado_dict: Dict = None):
        if estado_dict:
            for key, value in estado_dict.items():
                if hasattr(self.estado, key):
                    setattr(self.estado, key, value)
        elif arquivo:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    for key, value in dados.items():
                        if hasattr(self.estado, key):
                            setattr(self.estado, key, value)
            except FileNotFoundError:
                pass
    def estado_para_dict(self) -> Dict:
        return asdict(self.estado)
if __name__ == "__main__":
    agente = AgenteSDAInteligente()
    agente.carregar_estado()
    while True:
        try:
            entrada = input("Você: ").strip()
            if entrada.lower() in ['sair', 'quit', 'exit', 'tchau']:
                agente.salvar_estado()
                break
            if entrada.lower() == 'status':
                status = agente.get_status_nutricional()
                print(f"Calorias: {status['calorias_consumidas']:.0f}/{status['meta_calorias']} kcal ({status['percentual_meta']:.1f}%)")
                print(f"Proteínas: {status['macros_consumidos']['proteinas']:.1f}g")
                print(f"Carboidratos: {status['macros_consumidos']['carboidratos']:.1f}g")
                print(f"Gorduras: {status['macros_consumidos']['gorduras']:.1f}g")
                print(f"Refeições hoje: {status['refeicoes_hoje']}")
                continue
            if not entrada:
                continue
            resposta = agente.conversar(entrada)
            print(f"\n🤖 Agente SDA: {resposta}\n")
        except KeyboardInterrupt:
            agente.salvar_estado()
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            print("Tente novamente ou digite 'sair' para terminar.\n") 