# 🚀 SDA Backend API

API Backend do Sistema Digital de Alimentação usando FastAPI.

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **OpenAI** - Integração com GPT
- **SpeechRecognition** - Reconhecimento de voz
- **Pydub** - Processamento de áudio

## 📦 Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Copie `.env.example` para `.env`
2. Configure suas variáveis de ambiente:
   - `OPENAI_API_KEY` - Sua chave da OpenAI
   - `OPENAI_MODEL` - Modelo a usar (padrão: gpt-4o-mini)
   - `DEBUG` - Modo debug (true/false)

## 🚀 Executar

```bash
# Desenvolvimento com reload automático
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 Documentação

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Principais

- `POST /api/conversar` - Enviar mensagem
- `GET /api/status` - Obter status nutricional
- `POST /api/audio` - Processar áudio
- `POST /api/resetar` - Resetar sessão
