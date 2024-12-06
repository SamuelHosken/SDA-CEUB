import openai
from PIL import Image
import pytesseract

# 1. Configure a chave da API OpenAI
openai.api_key = "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"

# 2. Função para extrair texto de uma imagem usando OCR
def extract_text_from_image(image_path):
    try:
        # Abrir a imagem
        image = Image.open(image_path)
        # Usar pytesseract para extrair texto
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Erro ao processar a imagem: {e}"

# 3. Função para enviar o texto extraído para a API OpenAI
def analyze_text_with_openai(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Você pode usar 'gpt-3.5-turbo' para reduzir custos
            messages=[
                {"role": "system", "content": "Você é um assistente que analisa de imagens, descreva a imagem detalhadamente."},
                {"role": "user", "content": f"Analise: {text}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro ao conectar à API OpenAI: {e}"

# 4. Código principal
if __name__ == "__main__":
    # Caminho da imagem
    image_path = "teste.jpg"  # Substitua pelo caminho da sua imagem

    # Extração de texto
    print("Extraindo texto da imagem...")
    extracted_text = extract_text_from_image(image_path)
    print(f"Texto extraído:\n{extracted_text}")

    # Análise com OpenAI
    print("\nEnviando texto para análise...")
    openai_analysis = analyze_text_with_openai(extracted_text)
    print(f"Resposta da OpenAI:\n{openai_analysis}")
