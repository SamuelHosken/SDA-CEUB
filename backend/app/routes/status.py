from fastapi import APIRouter, HTTPException, Depends
from app.routes.auth import get_current_user
from app.routes.chat import get_agente
router = APIRouter()
@router.get("/status")
async def get_status(
    session_id: str | None = None,
    current_user: dict = Depends(get_current_user)
):
    try:
        user_uid = current_user["uid"]
        agente = get_agente(user_uid)
        status = agente.get_status_nutricional()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter status: {str(e)}")