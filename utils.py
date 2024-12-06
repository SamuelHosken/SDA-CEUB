from datetime import datetime

def obter_informacoes_tempo():
    """
    Retorna informações sobre o horário e a data atual.
    """
    agora = datetime.now()
    horario = agora.strftime("%H:%M")
    dia_semana = agora.strftime("%A")  # Ex: Monday
    data_completa = agora.strftime("%d de %B de %Y")  # Ex: 18 de November de 2024
    return horario, dia_semana, data_completa
