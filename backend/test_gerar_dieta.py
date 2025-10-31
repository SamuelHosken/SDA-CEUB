#!/usr/bin/env python3
import json
import sys
from app.services.gerar_dieta import gerar_dieta_personalizada
def testar_geracao_dieta():
    print("=" * 60)
    print("🧪 TESTE DE GERAÇÃO DE DIETA PERSONALIZADA")
    print("=" * 60)
    print()
    perfil_exemplo = {
        "sexo": "Masculino",
        "idade": 30,
        "altura": 175,
        "peso": 75,
        "objetivo": "ganhar massa",
        "treino_freq": "4x semana",
        "treino_tipo": "Musculação",
        "rotina": "fisicamente-ativo",
        "restricoes": "Nenhuma restrição alimentar",
        "alimentos_evita": "Não gosto de brócolis",
        "alimentos_preferidos": "Frango grelhado, arroz integral, batata doce, ovos",
        "refeicoes_dia": 6,
        "onde_come": "Misto",
        "suplementos": ["Whey", "Creatina"]
    }
    print("📋 Dados do perfil nutricional:")
    print(json.dumps(perfil_exemplo, indent=2, ensure_ascii=False))
    print()
    print("🔄 Gerando dieta personalizada com ChatGPT...")
    print("⏳ Isso pode levar alguns segundos...")
    print()
    try:
        dieta = gerar_dieta_personalizada(perfil_exemplo)
        print("✅ Dieta gerada com sucesso!")
        print()
        print("=" * 60)
        print("📊 DIETA GERADA")
        print("=" * 60)
        print()
        print(f"🔥 Calorias diárias: {dieta['calories']['daily']} kcal")
        print(f"📅 Calorias semanais: {dieta['calories']['weekly']} kcal")
        print(f"📆 Calorias mensais: {dieta['calories']['monthly']} kcal")
        print()
        print("🥗 Macronutrientes:")
        macros = dieta['macronutrients']
        print(f"  • Proteínas: {macros['protein']['grams']}g ({macros['protein']['percentage']}%)")
        print(f"  • Carboidratos: {macros['carbohydrates']['grams']}g ({macros['carbohydrates']['percentage']}%)")
        print(f"  • Gorduras: {macros['fats']['grams']}g ({macros['fats']['percentage']}%)")
        print(f"  • Fibras: {macros['fiber']}g")
        print()
        print("💧 Hidratação:")
        hidratacao = dieta['hydration']
        print(f"  • Diária: {hidratacao['daily']}L")
        print(f"  • Semanal: {hidratacao['weekly']}L")
        print(f"  • Mensal: {hidratacao['monthly']}L")
        print()
        print("🍽️ Refeições do dia (dias de semana):")
        refeicoes = dieta['daily_meals']['weekdays']
        for nome, dados in refeicoes.items():
            print(f"\n  {nome.replace('_', ' ').title()} ({dados['time']}) - {dados['calories']} kcal")
            for item in dados['items']:
                print(f"    • {item}")
        print()
        print("=" * 60)
        print("💾 Salvar dieta completa em arquivo JSON? (s/n)")
        print("=" * 60)
        resposta = input().strip().lower()
        if resposta == 's':
            nome_arquivo = "dieta_test_gerada.json"
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dieta, f, indent=2, ensure_ascii=False)
            print(f"✅ Dieta salva em: {nome_arquivo}")
        return True
    except Exception as e:
        print(f"❌ Erro ao gerar dieta: {e}")
        import traceback
        traceback.print_exc()
        return False
def testar_varios_perfis():
    perfis = [
        {
            "nome": "Homem - Ganhar Massa",
            "dados": {
                "sexo": "Masculino",
                "idade": 25,
                "altura": 180,
                "peso": 70,
                "objetivo": "ganhar massa",
                "treino_freq": "5x semana",
                "treino_tipo": "Musculação",
                "rotina": "ativo-moderado",
                "restricoes": "",
                "alimentos_evita": "",
                "alimentos_preferidos": "Frango, arroz, batata doce",
                "refeicoes_dia": 6,
                "onde_come": "Casa",
                "suplementos": ["Whey", "Creatina"]
            }
        },
        {
            "nome": "Mulher - Perder Gordura",
            "dados": {
                "sexo": "Feminino",
                "idade": 28,
                "altura": 165,
                "peso": 68,
                "objetivo": "perder gordura",
                "treino_freq": "3x semana",
                "treino_tipo": "Cross/Funcional",
                "rotina": "sedentario",
                "restricoes": "Intolerante a lactose",
                "alimentos_evita": "Alimentos processados",
                "alimentos_preferidos": "Vegetais, peixe, quinoa",
                "refeicoes_dia": 4,
                "onde_come": "Misto",
                "suplementos": ["Vitaminas"]
            }
        }
    ]
    print("🧪 Testando múltiplos perfis...")
    print()
    for perfil_info in perfis:
        print(f"📋 Testando: {perfil_info['nome']}")
        try:
            dieta = gerar_dieta_personalizada(perfil_info['dados'])
            print(f"✅ Sucesso! Calorias diárias: {dieta['calories']['daily']} kcal")
        except Exception as e:
            print(f"❌ Erro: {e}")
        print()
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--multi":
        testar_varios_perfis()
    else:
        sucesso = testar_geracao_dieta()
        sys.exit(0 if sucesso else 1)