#!/usr/bin/env python3
import json
import re
from typing import Dict, Optional
from openai import OpenAI
from app.config import settings
class GeradorDietaPersonalizada:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.openai_model = settings.openai_model
    def calcular_meta_calorica(self, perfil: Dict) -> int:
        sexo = perfil.get("sexo", "").lower()
        idade = perfil.get("idade", 30)
        altura_cm = perfil.get("altura", 170)
        peso_kg = perfil.get("peso", 70)
        objetivo = perfil.get("objetivo", "").lower()
        rotina = perfil.get("rotina", "").lower()
        treino_freq = perfil.get("treino_freq", "3x semana")
        if sexo in ["masculino", "m"]:
            tmb = 88.362 + (13.397 * peso_kg) + (4.799 * altura_cm) - (5.677 * idade)
        else:
            tmb = 447.593 + (9.247 * peso_kg) + (3.098 * altura_cm) - (4.330 * idade)
        fatores_atividade = {
            "sedentario": 1.2,
            "ativo-moderado": 1.375,
            "fisicamente-ativo": 1.55,
            "agenda-variavel": 1.4,
        }
        freq_num = 0
        try:
            if "x" in treino_freq.lower() or "X" in treino_freq:
                partes = treino_freq.lower().split("x")
                if partes:
                    freq_num = int(partes[0].strip())
            else:
                numeros = re.findall(r'\d+', treino_freq)
                if numeros:
                    freq_num = int(numeros[0])
        except (ValueError, AttributeError):
            freq_num = 0
        fator_atividade = fatores_atividade.get(rotina, 1.375)
        ajuste_treino = min(0.3, freq_num * 0.05)
        fator_atividade += ajuste_treino
        gasto_calorico_dia = tmb * fator_atividade
        ajuste_objetivo = {
            "ganhar massa": 1.15,
            "perder gordura": 0.85,
            "manter": 1.0,
            "performance": 1.1,
        }
        fator_objetivo = ajuste_objetivo.get(objetivo, 1.0)
        meta_calorica = int(gasto_calorico_dia * fator_objetivo)
        return max(1500, min(4000, meta_calorica))
    def gerar_dieta_com_ia(self, perfil: Dict) -> Dict:
        meta_calorica = self.calcular_meta_calorica(perfil)
        prompt = self._criar_prompt_dieta(perfil, meta_calorica)
        try:
            response = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um nutricionista especializado em criar planos alimentares personalizados. "
                                 "Sempre retorne APENAS um JSON válido no formato especificado, sem explicações extras. "
                                 "O JSON deve estar completo e bem formatado."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            resultado_texto = (response.choices[0].message.content or "").strip()
            if resultado_texto.startswith('```'):
                resultado_texto = resultado_texto.split('\n', 1)[1].rsplit('\n', 1)[0]
            if resultado_texto.startswith('```json'):
                resultado_texto = resultado_texto.split('\n', 1)[1].rsplit('\n', 1)[0]
            inicio_json = resultado_texto.find('{')
            fim_json = resultado_texto.rfind('}') + 1
            if inicio_json != -1 and fim_json != 0:
                resultado_texto = resultado_texto[inicio_json:fim_json]
            dieta = json.loads(resultado_texto)
            return self._validar_e_ajustar_dieta(dieta, meta_calorica, perfil)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON da dieta: {e}")
            print(f"Resposta recebida: {resultado_texto[:500]}")
            return self._criar_dieta_padrao(meta_calorica, perfil)
        except Exception as e:
            print(f"Erro ao gerar dieta com IA: {e}")
            return self._criar_dieta_padrao(meta_calorica, perfil)
    def _criar_prompt_dieta(self, perfil: Dict, meta_calorica: int) -> str:
        objetivo = perfil.get("objetivo", "")
        treino_freq = perfil.get("treino_freq", "3x semana")
        treino_tipo = perfil.get("treino_tipo", "")
        rotina = perfil.get("rotina", "")
        restricoes = perfil.get("restricoes", "") or "Nenhuma"
        alimentos_evita = perfil.get("alimentos_evita", "") or "Nenhum"
        alimentos_preferidos = perfil.get("alimentos_preferidos", "") or "Sem preferências específicas"
        refeicoes_dia = perfil.get("refeicoes_dia", 3)
        onde_come = perfil.get("onde_come", "Misto")
        suplementos = perfil.get("suplementos", [])
        prompt = f"""
Crie um plano alimentar personalizado completo em formato JSON para o usuário.
DADOS DO USUÁRIO:
- Sexo: {perfil.get("sexo", "Não informado")}
- Idade: {perfil.get("idade", 0)} anos
- Altura: {perfil.get("altura", 0)} cm
- Peso: {perfil.get("peso", 0)} kg
- Objetivo: {objetivo}
- Frequência de treino: {treino_freq}
- Tipo de treino: {treino_tipo}
- Rotina diária: {rotina}
- Restrições/Alergias: {restricoes}
- Alimentos que evita: {alimentos_evita}
- Alimentos preferidos: {alimentos_preferidos}
- Refeições por dia desejadas: {refeicoes_dia}
- Onde costuma comer: {onde_come}
- Suplementos: {", ".join(suplementos) if suplementos else "Nenhum"}
META CALÓRICA DIÁRIA: {meta_calorica} kcal
FORMATO JSON OBRIGATÓRIO:
{{
  "calories": {{
    "daily": {meta_calorica},
    "weekly": {meta_calorica * 7},
    "monthly": {meta_calorica * 30}
  }},
  "macronutrients": {{
    "protein": {{
      "grams": <valor em gramas>,
      "percentage": <percentual>
    }},
    "carbohydrates": {{
      "grams": <valor em gramas>,
      "percentage": <percentual>
    }},
    "fats": {{
      "grams": <valor em gramas>,
      "percentage": <percentual>
    }},
    "fiber": <valor em gramas>
  }},
  "hydration": {{
    "daily": <litros por dia>,
    "weekly": <litros por semana>,
    "monthly": <litros por mês>,
    "unit": "litros"
  }},
  "daily_meals": {{
    "weekdays": {{
      "breakfast": {{
        "time": "HH:MM",
        "items": ["item 1", "item 2", ...],
        "calories": <valor>
      }},
      "pre_workout": {{
        "time": "HH:MM",
        "items": ["item 1", "item 2", ...],
        "calories": <valor>
      }},
      "post_workout": {{
        "time": "HH:MM",
        "items": ["item 1", "item 2", ...],
        "calories": <valor>
      }},
      "afternoon_snack": {{
        "time": "HH:MM",
        "items": ["item 1", "item 2", ...],
        "calories": <valor>
      }},
      "dinner": {{
        "time": "HH:MM",
        "items": ["item 1", "item 2", ...],
        "calories": <valor>
      }},
      "evening_snack": {{
        "time": "HH:MM",
        "items": ["item 1", "item 2", ...],
        "calories": <valor>
      }}
    }},
    "weekends": {{
      "adjustments": ["ajuste 1", "ajuste 2", ...],
      "calories": <valor diário>
    }}
  }},
  "weekly_plan": {{
    "training_days": <número>,
    "total_calories": {meta_calorica * 7},
    "hydration": "<valor> litros"
  }},
  "monthly_plan": {{
    "training_days": <número>,
    "rest_days": <número>,
    "total_calories": {meta_calorica * 30},
    "hydration": "<valor> litros"
  }},
  "additional_notes": [
    "nota 1",
    "nota 2",
    ...
  ],
  "food_alternatives": {{
    "proteins": {{
      "substitutes": ["alternativa 1", "alternativa 2", ...],
      "fast_food_options": ["opção 1", "opção 2", ...]
    }},
    "carbohydrates": {{
      "substitutes": ["alternativa 1", "alternativa 2", ...],
      "fast_food_options": ["opção 1", "opção 2", ...]
    }},
    "fats": {{
      "substitutes": ["alternativa 1", "alternativa 2", ...],
      "fast_food_options": ["opção 1", "opção 2", ...]
    }},
    "snacks": {{
      "substitutes": ["alternativa 1", "alternativa 2", ...],
      "fast_food_options": ["opção 1", "opção 2", ...]
    }},
    "drinks": {{
      "substitutes": ["alternativa 1", "alternativa 2", ...],
      "fast_food_options": ["opção 1", "opção 2", ...]
    }}
  }}
}}
INSTRUÇÕES IMPORTANTES:
1. Calcule os macronutrientes apropriados baseado no objetivo do usuário:
   - Ganhar massa: ~30% proteína, ~40% carboidratos, ~30% gorduras
   - Perder gordura: ~35% proteína, ~35% carboidratos, ~30% gorduras
   - Manter: ~25% proteína, ~45% carboidratos, ~30% gorduras
   - Performance: ~30% proteína, ~45% carboidratos, ~25% gorduras
2. DISTRIBUIR as {meta_calorica} kcal entre as refeições considerando:
   - Café da manhã: 20-25%
   - Pré-treino: 10-15%
   - Pós-treino: 25-30%
   - Lanche da tarde: 10-15%
   - Jantar: 20-25%
   - Lanche noturno: 5-10%
3. Considerar as preferências alimentares: {alimentos_preferidos}
4. RESPEITAR restrições e alimentos evitados: {restricoes}, {alimentos_evita}
5. Incluir suplementos mencionados quando apropriado: {", ".join(suplementos) if suplementos else "Nenhum"}
6. Criar horários realistas baseados na rotina do usuário
7. Incluir alternativas de fast food apropriadas se o usuário come fora
8. Calcular hidratação baseada no peso (35ml/kg) e atividade física
9. Garantir que a soma das calorias das refeições seja aproximadamente {meta_calorica} kcal
10. Se o usuário prefere {refeicoes_dia} refeições, ajuste a distribuição adequadamente
RETORNE APENAS O JSON, sem explicações ou comentários adicionais.
"""
        return prompt
    def _validar_e_ajustar_dieta(self, dieta: Dict, meta_calorica: int, perfil: Dict) -> Dict:
        if "calories" not in dieta:
            dieta["calories"] = {
                "daily": meta_calorica,
                "weekly": meta_calorica * 7,
                "monthly": meta_calorica * 30
            }
        if "macronutrients" not in dieta:
            dieta["macronutrients"] = self._calcular_macros_padrao(meta_calorica, perfil.get("objetivo", ""))
        if "hydration" not in dieta:
            peso = perfil.get("peso", 70)
            hidratacao_dia = round(peso * 0.035, 1)
            dieta["hydration"] = {
                "daily": hidratacao_dia,
                "weekly": round(hidratacao_dia * 7, 1),
                "monthly": round(hidratacao_dia * 30, 1),
                "unit": "litros"
            }
        if "daily_meals" not in dieta or "weekdays" not in dieta["daily_meals"]:
            dieta["daily_meals"] = {
                "weekdays": self._criar_refeicoes_padrao(meta_calorica, perfil),
                "weekends": {
                    "adjustments": ["Reduzir carboidratos em 10-15%", "Manter proteínas"],
                    "calories": int(meta_calorica * 0.92)
                }
            }
        if "weekly_plan" not in dieta:
            treino_freq = perfil.get("treino_freq", "3x semana")
            try:
                if "x" in treino_freq:
                    freq_num = int(treino_freq.split("x")[0].strip())
                else:
                    freq_num = 3
            except (ValueError, AttributeError):
                freq_num = 3
            freq_num = max(0, min(7, freq_num))
            dieta["weekly_plan"] = {
                "training_days": freq_num,
                "total_calories": meta_calorica * 7,
                "hydration": f"{dieta['hydration']['daily'] * 7:.1f} litros"
            }
        if "monthly_plan" not in dieta:
            freq_semanal = dieta["weekly_plan"].get("training_days", 3)
            dieta["monthly_plan"] = {
                "training_days": freq_semanal * 4,
                "rest_days": 30 - (freq_semanal * 4),
                "total_calories": meta_calorica * 30,
                "hydration": f"{dieta['hydration']['daily'] * 30:.1f} litros"
            }
        if "additional_notes" not in dieta:
            dieta["additional_notes"] = [
                "Siga o plano 90% do tempo para manter flexibilidade.",
                "Acompanhe o peso semanalmente e ajuste as porções se necessário.",
                "Beba água regularmente ao longo do dia."
            ]
        if "food_alternatives" not in dieta:
            dieta["food_alternatives"] = self._criar_alternativas_padrao()
        return dieta
    def _calcular_macros_padrao(self, calorias: int, objetivo: str) -> Dict:
        objetivo_lower = objetivo.lower()
        if "ganhar massa" in objetivo_lower:
            pct_proteina, pct_carb, pct_gordura = 0.30, 0.40, 0.30
        elif "perder gordura" in objetivo_lower or "emagrec" in objetivo_lower:
            pct_proteina, pct_carb, pct_gordura = 0.35, 0.35, 0.30
        elif "performance" in objetivo_lower:
            pct_proteina, pct_carb, pct_gordura = 0.30, 0.45, 0.25
        else:
            pct_proteina, pct_carb, pct_gordura = 0.25, 0.45, 0.30
        return {
            "protein": {
                "grams": int((calorias * pct_proteina) / 4),
                "percentage": int(pct_proteina * 100)
            },
            "carbohydrates": {
                "grams": int((calorias * pct_carb) / 4),
                "percentage": int(pct_carb * 100)
            },
            "fats": {
                "grams": int((calorias * pct_gordura) / 9),
                "percentage": int(pct_gordura * 100)
            },
            "fiber": 30
        }
    def _criar_refeicoes_padrao(self, calorias: int, perfil: Dict) -> Dict:
        objetivo = perfil.get("objetivo", "").lower()
        refeicoes_dia = perfil.get("refeicoes_dia", 6)
        if refeicoes_dia >= 6:
            cal_cafe = int(calorias * 0.20)
            cal_pre = int(calorias * 0.10)
            cal_pos = int(calorias * 0.30)
            cal_lanche = int(calorias * 0.15)
            cal_jantar = int(calorias * 0.20)
            cal_noturno = int(calorias * 0.05)
        else:
            cal_cafe = int(calorias * 0.25)
            cal_pre = int(calorias * 0.15)
            cal_pos = int(calorias * 0.35)
            cal_lanche = 0
            cal_jantar = int(calorias * 0.20)
            cal_noturno = int(calorias * 0.05)
        return {
            "breakfast": {
                "time": "07:00",
                "items": ["Aveia com frutas", "Café ou chá"],
                "calories": cal_cafe
            },
            "pre_workout": {
                "time": "11:00",
                "items": ["Banana", "Whey protein"] if "whey" in str(perfil.get("suplementos", [])).lower() else ["Banana"],
                "calories": cal_pre
            },
            "post_workout": {
                "time": "13:00",
                "items": ["Frango grelhado", "Arroz integral", "Legumes"],
                "calories": cal_pos
            },
            "afternoon_snack": {
                "time": "16:00",
                "items": ["Iogurte grego", "Castanhas"],
                "calories": cal_lanche
            },
            "dinner": {
                "time": "20:00",
                "items": ["Salmão ou frango", "Batata doce", "Salada"],
                "calories": cal_jantar
            },
            "evening_snack": {
                "time": "22:00",
                "items": ["Caseína ou iogurte", "Amêndoas"],
                "calories": cal_noturno
            }
        }
    def _criar_alternativas_padrao(self) -> Dict:
        return {
            "proteins": {
                "substitutes": [
                    "Peito de frango",
                    "Peito de peru",
                    "Ovos",
                    "Peixes magros",
                    "Cortes magros de carne"
                ],
                "fast_food_options": [
                    "Sanduíche de frango grelhado",
                    "Salada com proteína grelhada"
                ]
            },
            "carbohydrates": {
                "substitutes": [
                    "Batata-doce",
                    "Arroz integral",
                    "Quinoa",
                    "Aveia"
                ],
                "fast_food_options": [
                    "Bowl de vegetais",
                    "Aveia sem açúcar"
                ]
            },
            "fats": {
                "substitutes": [
                    "Abacate",
                    "Azeite de oliva",
                    "Castanhas",
                    "Sementes"
                ],
                "fast_food_options": [
                    "Salada com azeite",
                    "Torrada com abacate"
                ]
            },
            "snacks": {
                "substitutes": [
                    "Iogurte grego",
                    "Ovos cozidos",
                    "Frutos secos"
                ],
                "fast_food_options": [
                    "Barras de proteína",
                    "Iogurte natural"
                ]
            },
            "drinks": {
                "substitutes": [
                    "Água",
                    "Chá verde",
                    "Café preto"
                ],
                "fast_food_options": [
                    "Chá gelado sem açúcar",
                    "Café americano"
                ]
            }
        }
    def _criar_dieta_padrao(self, meta_calorica: int, perfil: Dict) -> Dict:
        peso = perfil.get("peso", 70)
        hidratacao_dia = round(peso * 0.035, 1)
        return {
            "calories": {
                "daily": meta_calorica,
                "weekly": meta_calorica * 7,
                "monthly": meta_calorica * 30
            },
            "macronutrients": self._calcular_macros_padrao(meta_calorica, perfil.get("objetivo", "")),
            "hydration": {
                "daily": hidratacao_dia,
                "weekly": round(hidratacao_dia * 7, 1),
                "monthly": round(hidratacao_dia * 30, 1),
                "unit": "litros"
            },
            "daily_meals": {
                "weekdays": self._criar_refeicoes_padrao(meta_calorica, perfil),
                "weekends": {
                    "adjustments": ["Reduzir carboidratos em 10-15%"],
                    "calories": int(meta_calorica * 0.92)
                }
            },
            "weekly_plan": {
                "training_days": 3,
                "total_calories": meta_calorica * 7,
                "hydration": f"{hidratacao_dia * 7:.1f} litros"
            },
            "monthly_plan": {
                "training_days": 12,
                "rest_days": 18,
                "total_calories": meta_calorica * 30,
                "hydration": f"{hidratacao_dia * 30:.1f} litros"
            },
            "additional_notes": [
                "Siga o plano 90% do tempo para manter flexibilidade.",
                "Acompanhe o peso semanalmente e ajuste as porções se necessário."
            ],
            "food_alternatives": self._criar_alternativas_padrao()
        }
def gerar_dieta_personalizada(perfil: Dict) -> Dict:
    gerador = GeradorDietaPersonalizada()
    return gerador.gerar_dieta_com_ia(perfil)