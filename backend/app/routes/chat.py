from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.agente_sda import AgenteSDAInteligente
from app.routes.auth import get_current_user
from app.utils.firebase import get_firestore
from firebase_admin import firestore
router = APIRouter()
agentes_sessao = {}
class MensagemRequest(BaseModel):
    mensagem: str
    session_id: str | None = None
class MensagemResponse(BaseModel):
    resposta: str
    status: dict
def get_agente(user_uid: str) -> AgenteSDAInteligente:
    if user_uid not in agentes_sessao:
        db = get_firestore()
        user_ref = db.collection("users").document(user_uid)
        user_doc = user_ref.get()
        dieta = None
        estado_nutricional = None
        if user_doc.exists:
            user_data = user_doc.to_dict()
            dieta = user_data.get("dieta_ia")
            estado_nutricional = user_data.get("estado_nutricional")
        if dieta:
            agente = AgenteSDAInteligente(dieta_dict=dieta)
        else:
            agente = AgenteSDAInteligente()
        if estado_nutricional:
            agente.carregar_estado(estado_dict=estado_nutricional)
        agentes_sessao[user_uid] = agente
    return agentes_sessao[user_uid]
def salvar_estado_no_firebase(user_uid: str, agente: AgenteSDAInteligente):
    try:
        db = get_firestore()
        user_ref = db.collection("users").document(user_uid)
        estado_dict = agente.estado_para_dict()
        user_ref.update({
            "estado_nutricional": estado_dict,
            "updated_at": firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        print(f"Erro ao salvar estado no Firebase: {e}")
@router.post("/conversar", response_model=MensagemResponse)
async def conversar(
    request: MensagemRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not request.mensagem.strip():
            raise HTTPException(status_code=400, detail="Mensagem vazia")
        user_uid = current_user["uid"]
        agente = get_agente(user_uid)
        resposta = agente.conversar(request.mensagem)
        salvar_estado_no_firebase(user_uid, agente)
        status = agente.get_status_nutricional()
        return MensagemResponse(resposta=resposta, status=status)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")