from fastapi import APIRouter, HTTPException, Depends
from app.routes.auth import get_current_user
from app.services.agente_sda import EstadoNutricional
from firebase_admin import firestore
from app.utils.firebase import get_firestore
from dataclasses import asdict
router = APIRouter()
@router.post("/resetar")
async def resetar(
    session_id: str | None = None,
    current_user: dict = Depends(get_current_user)
):
    try:
        user_uid = current_user["uid"]
        from app.routes.chat import agentes_sessao
        if user_uid in agentes_sessao:
            del agentes_sessao[user_uid]
        db = get_firestore()
        user_ref = db.collection("users").document(user_uid)
        estado_vazio = EstadoNutricional()
        estado_dict = asdict(estado_vazio)
        user_ref.update({
            "estado_nutricional": estado_dict,
            "updated_at": firestore.SERVER_TIMESTAMP
        })
        return {"sucesso": "Sessão resetada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao resetar: {str(e)}")