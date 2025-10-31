#!/usr/bin/env python3
import requests
import json
import sys
def testar_via_api(token=None):
    if not token:
        print("⚠️  Token não fornecido. Você precisa de um token válido do Firebase.")
        print("Para obter um token:")
        print("1. Faça login no frontend")
        print("2. Abra o console do navegador")
        print("3. Execute: localStorage.getItem('auth_token')")
        print()
        token = input("Cole o token aqui (ou pressione Enter para pular): ").strip()
        if not token:
            print("❌ Teste cancelado. Token necessário.")
            return False
    url = "http://localhost:8000/api/auth/save-user-data"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "apelido": "Teste Dieta",
        "perfil_nutricional": {
            "sexo": "Masculino",
            "idade": 30,
            "altura": 175,
            "peso": 75,
            "objetivo": "ganhar massa",
            "treino_freq": "4x semana",
            "treino_tipo": "Musculação",
            "rotina": "fisicamente-ativo",
            "restricoes": "",
            "alimentos_evita": "",
            "alimentos_preferidos": "Frango grelhado, arroz integral, batata doce, ovos",
            "refeicoes_dia": 6,
            "onde_come": "Misto",
            "suplementos": ["Whey", "Creatina"]
        }
    }
    print("=" * 60)
    print("🧪 TESTE VIA API - GERAÇÃO DE DIETA")
    print("=" * 60)
    print()
    print(f"📡 URL: {url}")
    print(f"🔑 Token: {token[:20]}..." if len(token) > 20 else f"🔑 Token: {token}")
    print()
    print("📤 Enviando dados...")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"📥 Status Code: {response.status_code}")
        print()
        if response.status_code == 200:
            resultado = response.json()
            print("✅ Sucesso!")
            print()
            print("📊 Resposta:")
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
            if resultado.get("dieta_gerada"):
                print()
                print("🎉 Dieta gerada com sucesso!")
                print("   Verifique o Firebase na collection 'users' para ver a dieta completa.")
            else:
                print()
                print("⚠️  Dieta não foi gerada.")
                if "erro_dieta" in resultado:
                    print(f"   Erro: {resultado['erro_dieta']}")
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que o servidor está rodando em http://localhost:8000")
        print()
        print("   Para iniciar o servidor:")
        print("   cd backend")
        print("   uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
def verificar_servidor():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False
if __name__ == "__main__":
    print("🔍 Verificando se o servidor está rodando...")
    if not verificar_servidor():
        print("❌ Servidor não está rodando!")
        print()
        print("Para iniciar o servidor:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        sys.exit(1)
    print("✅ Servidor está rodando!")
    print()
    token = sys.argv[1] if len(sys.argv) > 1 else None
    sucesso = testar_via_api(token)
    sys.exit(0 if sucesso else 1)