from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.services.agente_sda import AgenteSDAInteligente
from app.routes.auth import get_current_user
from app.routes.chat import get_agente, salvar_estado_no_firebase
import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid
router = APIRouter()
@router.post("/audio")
async def processar_audio(
    audio: UploadFile = File(...),
    session_id: str | None = None,
    current_user: dict = Depends(get_current_user)
):
    temp_original = None
    temp_wav = None
    try:
        user_uid = current_user["uid"]
        print(f"[AUDIO] Recebido áudio do usuário: {user_uid}")
        print(f"[AUDIO] Nome do arquivo: {audio.filename}")
        print(f"[AUDIO] Content-Type: {audio.content_type}")
        if not audio:
            raise HTTPException(status_code=400, detail="Nenhum arquivo de áudio foi enviado.")
        content = await audio.read()
        if not content or len(content) == 0:
            raise HTTPException(status_code=400, detail="Arquivo de áudio vazio. Tente gravar novamente.")
        file_size = len(content)
        print(f"[AUDIO] Tamanho do arquivo: {file_size} bytes")
        if file_size < 100:
            raise HTTPException(
                status_code=400, 
                detail=f"Áudio muito curto ({file_size} bytes). Grave por pelo menos 1-2 segundos."
            )
        temp_original = f"temp_audio_original_{uuid.uuid4()}"
        with open(temp_original, "wb") as f:
            f.write(content)
        file_size_saved = os.path.getsize(temp_original)
        print(f"[AUDIO] Arquivo salvo: {temp_original}, tamanho: {file_size_saved} bytes")
        if file_size_saved < 100:
            raise HTTPException(
                status_code=400, 
                detail=f"Áudio muito curto ({file_size_saved} bytes). Grave por pelo menos 1-2 segundos."
            )
        temp_wav = f"temp_audio_wav_{uuid.uuid4()}.wav"
        try:
            audio_segment = None
            content_type = audio.content_type or ""
            formato_detectado = None
            if 'webm' in content_type.lower():
                formato_detectado = 'webm'
            elif 'mp4' in content_type.lower() or 'm4a' in content_type.lower():
                formato_detectado = 'mp4'
            elif 'ogg' in content_type.lower():
                formato_detectado = 'ogg'
            elif 'wav' in content_type.lower():
                formato_detectado = 'wav'
            formatos = []
            if formato_detectado:
                formatos = [formato_detectado] + ['webm', 'mp4', 'm4a', 'ogg', 'wav']
                formatos = list(dict.fromkeys(formatos))
                print(f"[AUDIO] Formato detectado do Content-Type: {formato_detectado}")
            else:
                formatos = ['webm', 'mp4', 'm4a', 'ogg', 'wav']
                print(f"[AUDIO] Tentando detectar formato do áudio...")
            for formato in formatos:
                try:
                    print(f"[AUDIO] Tentando formato: {formato}")
                    audio_segment = AudioSegment.from_file(temp_original, format=formato)
                    print(f"[AUDIO] Sucesso com formato: {formato}")
                    break
                except Exception as e:
                    print(f"[AUDIO] Falhou formato {formato}: {str(e)}")
                    continue
            if audio_segment is None:
                try:
                    print(f"[AUDIO] Tentando carregar sem especificar formato...")
                    audio_segment = AudioSegment.from_file(temp_original)
                    print(f"[AUDIO] Áudio carregado sem especificar formato")
                except Exception as e:
                    print(f"[AUDIO] Erro ao carregar áudio: {e}")
                    import traceback
                    traceback.print_exc()
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Formato de áudio não suportado. Detalhe: {str(e)}"
                    )
            duracao_ms = len(audio_segment)
            print(f"[AUDIO] Duração do áudio: {duracao_ms}ms")
            if duracao_ms < 300:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Áudio muito curto ({duracao_ms}ms). Fale por pelo menos 1 segundo."
                )
            print(f"[AUDIO] Convertendo áudio para formato WAV...")
            try:
                audio_segment = audio_segment.set_channels(1)
                audio_segment = audio_segment.set_frame_rate(16000)
                print(f"[AUDIO] Canais e sample rate ajustados")
                max_dBFS = audio_segment.max_dBFS
                rms = audio_segment.rms
                print(f"[AUDIO] Volume máximo: {max_dBFS:.1f} dBFS")
                print(f"[AUDIO] Volume médio (RMS): {rms:.1f}")
                if max_dBFS < -20:
                    gain_to_apply = -15 - max_dBFS
                    gain_to_apply = min(gain_to_apply, 20)
                    audio_segment = audio_segment.apply_gain(gain_to_apply)
                    print(f"[AUDIO] Ganho aplicado: +{gain_to_apply:.1f} dB")
                elif max_dBFS < -15:
                    gain_to_apply = -15 - max_dBFS
                    audio_segment = audio_segment.apply_gain(gain_to_apply)
                    print(f"[AUDIO] Ganho leve aplicado: +{gain_to_apply:.1f} dB")
                try:
                    audio_segment = audio_segment.normalize()
                    print(f"[AUDIO] Áudio normalizado")
                    max_dBFS_final = audio_segment.max_dBFS
                    if max_dBFS_final < -3:
                        gain_extra = min(3, -3 - max_dBFS_final)
                        if gain_extra > 0:
                            audio_segment = audio_segment.apply_gain(gain_extra)
                            print(f"[AUDIO] Ganho extra aplicado: +{gain_extra:.1f} dB")
                except Exception as e:
                    print(f"[AUDIO] Aviso ao normalizar: {e}, continuando...")
                print(f"[AUDIO] Exportando para WAV: {temp_wav}")
                audio_segment.export(temp_wav, format="wav", parameters=["-ac", "1", "-ar", "16000"])
                print(f"[AUDIO] WAV exportado com sucesso")
            except Exception as e:
                print(f"[AUDIO] Erro ao converter áudio: {e}")
                import traceback
                traceback.print_exc()
                raise HTTPException(
                    status_code=400,
                    detail=f"Erro ao converter áudio: {str(e)}"
                )
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 200
            recognizer.dynamic_energy_threshold = True
            recognizer.dynamic_energy_adjustment_damping = 0.15
            recognizer.dynamic_energy_ratio = 1.5
            recognizer.pause_threshold = 1.0
            recognizer.phrase_threshold = 0.2
            recognizer.non_speaking_duration = 0.5
            print(f"[AUDIO] Iniciando reconhecimento de voz com configurações otimizadas...")
            texto = None
            with sr.AudioFile(temp_wav) as source:
                duracao_ajuste = min(1.0, len(audio_segment) / 1000)
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=duracao_ajuste)
                    print(f"[AUDIO] Ruído ambiente ajustado por {duracao_ajuste:.2f}s")
                    print(f"[AUDIO] Energy threshold após ajuste: {recognizer.energy_threshold}")
                except Exception as e:
                    print(f"[AUDIO] Aviso ao ajustar ruído: {e}, continuando...")
                try:
                    audio_data = recognizer.record(source, duration=None)
                    tamanho_bytes = len(audio_data.get_raw_data()) if hasattr(audio_data, 'get_raw_data') else 0
                    print(f"[AUDIO] Áudio gravado ({tamanho_bytes} bytes), tentando reconhecer...")
                except Exception as e:
                    print(f"[AUDIO] Erro ao gravar áudio: {e}")
                    source.rewind()
                    audio_data = recognizer.record(source)
                tentativas = [
                    ("pt-BR", "Brasileiro"),
                    ("pt-PT", "Português"),
                    ("pt", "Português genérico"),
                ]
                for idioma, nome in tentativas:
                    try:
                        print(f"[AUDIO] Tentando reconhecimento: {nome} ({idioma})")
                        texto = recognizer.recognize_google(audio_data, language=idioma)
                        if texto and texto.strip():
                            print(f"[AUDIO] ✅ Texto reconhecido ({nome}): {texto}")
                            break
                    except sr.UnknownValueError:
                        print(f"[AUDIO] ❌ Não reconhecido em {nome}")
                        continue
                    except sr.RequestError as e:
                        print(f"[AUDIO] ⚠️ Erro de conexão com Google: {e}")
                        raise
                    except Exception as e:
                        print(f"[AUDIO] ⚠️ Erro ao reconhecer em {nome}: {e}")
                        continue
                if not texto or not texto.strip():
                    print(f"[AUDIO] Não reconhecido na primeira tentativa, tentando configurações alternativas...")
                    configs_alternativas = [
                        {
                            "nome": "Super Sensível",
                            "energy_threshold": 100,
                            "dynamic_energy_threshold": False,
                            "pause_threshold": 1.5,
                            "phrase_threshold": 0.1,
                        },
                        {
                            "nome": "Sem Ajuste de Ruído",
                            "energy_threshold": 200,
                            "dynamic_energy_threshold": False,
                            "pause_threshold": 1.0,
                            "phrase_threshold": 0.2,
                        },
                        {
                            "nome": "Ultra Sensível",
                            "energy_threshold": 50,
                            "dynamic_energy_threshold": False,
                            "pause_threshold": 2.0,
                            "phrase_threshold": 0.05,
                        },
                    ]
                    for config in configs_alternativas:
                        if texto and texto.strip():
                            break
                        print(f"[AUDIO] Tentando configuração: {config['nome']}")
                        recognizer_alt = sr.Recognizer()
                        recognizer_alt.energy_threshold = config["energy_threshold"]
                        recognizer_alt.dynamic_energy_threshold = config["dynamic_energy_threshold"]
                        recognizer_alt.pause_threshold = config["pause_threshold"]
                        recognizer_alt.phrase_threshold = config["phrase_threshold"]
                        recognizer_alt.non_speaking_duration = 0.4
                        try:
                            with sr.AudioFile(temp_wav) as source_alt:
                                audio_data_alt = recognizer_alt.record(source_alt, duration=None)
                                for idioma, nome in tentativas:
                                    try:
                                        print(f"[AUDIO] Tentativa ({config['nome']}, {nome}): {idioma}")
                                        texto = recognizer_alt.recognize_google(audio_data_alt, language=idioma)
                                        if texto and texto.strip():
                                            print(f"[AUDIO] ✅ Texto reconhecido ({config['nome']}, {nome}): {texto}")
                                            break
                                    except sr.UnknownValueError:
                                        continue
                                    except Exception as e:
                                        print(f"[AUDIO] Erro na tentativa: {e}")
                                        continue
                        except Exception as e:
                            print(f"[AUDIO] Erro ao processar com {config['nome']}: {e}")
                            continue
            if not texto or not texto.strip():
                return {
                    "texto_reconhecido": None,
                    "resposta": "Desculpe, não consegui entender o que você disse. 😅\n\nPode tentar:\n• Falar mais alto e claro\n• Reduzir ruído de fundo\n• Tentar novamente\n• Ou digitar sua mensagem",
                    "status": None,
                    "erro_reconhecimento": True
                }
            print(f"[AUDIO] Processando resposta do agente...")
            agente = get_agente(user_uid)
            resposta = agente.conversar(texto)
            salvar_estado_no_firebase(user_uid, agente)
            status = agente.get_status_nutricional()
            print(f"[AUDIO] Resposta gerada com sucesso")
            return {
                "texto_reconhecido": texto,
                "resposta": resposta,
                "status": status
            }
        except sr.RequestError as e:
            print(f"[AUDIO] Erro no serviço de reconhecimento: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro no serviço de reconhecimento de voz: {str(e)}"
            )
        except HTTPException:
            raise
        except Exception as audio_error:
            print(f"[AUDIO] Erro ao processar áudio: {audio_error}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar áudio: {str(audio_error)}"
            )
    except HTTPException as he:
        print(f"[AUDIO] HTTPException capturada: {he.detail}")
        raise
    except Exception as e:
        print(f"[AUDIO] Erro geral não capturado: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro geral: {str(e)}")
    finally:
        for temp_file in [temp_original, temp_wav]:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass