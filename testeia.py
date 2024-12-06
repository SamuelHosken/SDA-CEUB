import openai

openai.api_key = "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"

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": "Olá, tudo bem?"}
        ]
    )
    print(response["choices"][0]["message"]["content"])
except Exception as e:
    print(f"Erro: {e}")