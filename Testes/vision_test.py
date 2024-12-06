from google.cloud import vision

def describe_image(image_path):
    """
    Descreve o conteúdo de uma imagem usando a API Google Cloud Vision.
    """
    # Configurar o cliente da API
    client = vision.ImageAnnotatorClient()

    # Carregar a imagem
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Analisar o conteúdo
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Mostrar as descrições
    print("Descrição da imagem:")
    for label in labels:
        print(f"- {label.description} (confiança: {label.score:.2f})")

    # Verificar se há erros
    if response.error.message:
        raise Exception(f"Erro na API: {response.error.message}")

# Testar com uma imagem
image_path = "teste.jpg"  # Substitua pelo caminho da sua imagem
describe_image(image_path)
