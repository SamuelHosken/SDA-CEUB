from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.utils.firebase import verify_firebase_token, get_firestore, init_firebase
from app.services.gerar_dieta import gerar_dieta_personalizada
from firebase_admin import firestore, auth
import asyncio
router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()
class FirebaseTokenRequest(BaseModel):
    id_token: str
class UserResponse(BaseModel):
    uid: str
    email: str
    display_name: str | None = None
    photo_url: str | None = None
    email_verified: bool
class TokenVerification(BaseModel):
    valid: bool
    user: UserResponse | None = None
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        decoded_token = verify_firebase_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
@router.post("/verify-token", response_model=TokenVerification)
async def verify_token(token_data: FirebaseTokenRequest):
    try:
        decoded_token = verify_firebase_token(token_data.id_token)
        user_response = UserResponse(
            uid=decoded_token["uid"],
            email=decoded_token.get("email", ""),
            display_name=decoded_token.get("name"),
            photo_url=decoded_token.get("picture"),
            email_verified=decoded_token.get("email_verified", False),
        )
        return TokenVerification(valid=True, user=user_response)
    except Exception as e:
        return TokenVerification(valid=False, user=None)
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        uid=current_user["uid"],
        email=current_user.get("email", ""),
        display_name=current_user.get("name"),
        photo_url=current_user.get("picture"),
        email_verified=current_user.get("email_verified", False),
    )
@router.get("/user-data")
async def get_user_data(current_user: dict = Depends(get_current_user)):
    db = get_firestore()
    user_doc = db.collection("users").document(current_user["uid"]).get()
    if user_doc.exists:
        return user_doc.to_dict()
    user_data = {
        "uid": current_user["uid"],
        "email": current_user.get("email"),
        "display_name": current_user.get("name"),
        "created_at": firestore.SERVER_TIMESTAMP,
    }
    db.collection("users").document(current_user["uid"]).set(user_data)
    return user_data
@router.post("/save-user-data")
async def save_user_data(
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    try:
        db = get_firestore()
        user_ref = db.collection("users").document(current_user["uid"])
        user_doc = user_ref.get()
        tem_dieta_ia = False
        if user_doc.exists:
            user_data_existente = user_doc.to_dict()
            tem_dieta_ia = "dieta_ia" in user_data_existente
        user_ref.set(data, merge=True)
        perfil_nutricional = data.get("perfil_nutricional", {})
        tem_dados_suficientes = (
            perfil_nutricional.get("idade") and 
            perfil_nutricional.get("altura") and 
            perfil_nutricional.get("peso") and 
            perfil_nutricional.get("objetivo") and
            not tem_dieta_ia
        )
        if tem_dados_suficientes:
            try:
                loop = asyncio.get_event_loop()
                dieta_ia = await loop.run_in_executor(
                    None, 
                    gerar_dieta_personalizada, 
                    perfil_nutricional
                )
                user_ref.update({
                    "dieta_ia": dieta_ia,
                    "dieta_ia_gerada_em": firestore.SERVER_TIMESTAMP
                })
                return {
                    "success": True, 
                    "message": "Dados salvos com sucesso. Dieta personalizada gerada!",
                    "dieta_gerada": True
                }
            except Exception as e:
                print(f"Erro ao gerar dieta personalizada: {e}")
                return {
                    "success": True,
                    "message": "Dados salvos com sucesso. A dieta será gerada em breve.",
                    "dieta_gerada": False,
                    "erro_dieta": str(e)
                }
        else:
            return {
                "success": True, 
                "message": "Dados salvos com sucesso",
                "dieta_gerada": False
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar dados: {e}")
@router.put("/update-account")
async def update_account(
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    try:
        db = get_firestore()
        user_uid = current_user["uid"]
        user_ref = db.collection("users").document(user_uid)
        update_data = {}
        if "apelido" in data:
            update_data["apelido"] = data["apelido"]
        if "perfil_nutricional" in data:
            update_data["perfil_nutricional"] = data["perfil_nutricional"]
        if "display_name" in data:
            update_data["display_name"] = data["display_name"]
            try:
                auth.update_user(user_uid, display_name=data["display_name"])
            except Exception as e:
                print(f"Erro ao atualizar display_name no Firebase Auth: {e}")
        if update_data:
            user_doc = user_ref.get()
            tem_dieta_ia = False
            if user_doc.exists:
                user_data_existente = user_doc.to_dict()
                tem_dieta_ia = "dieta_ia" in user_data_existente
            update_data["updated_at"] = firestore.SERVER_TIMESTAMP
            user_ref.update(update_data)
            if "perfil_nutricional" in update_data and not tem_dieta_ia:
                perfil_nutricional = update_data["perfil_nutricional"]
                tem_dados_suficientes = (
                    perfil_nutricional.get("idade") and 
                    perfil_nutricional.get("altura") and 
                    perfil_nutricional.get("peso") and 
                    perfil_nutricional.get("objetivo")
                )
                if tem_dados_suficientes:
                    try:
                        loop = asyncio.get_event_loop()
                        dieta_ia = await loop.run_in_executor(
                            None, 
                            gerar_dieta_personalizada, 
                            perfil_nutricional
                        )
                        user_ref.update({
                            "dieta_ia": dieta_ia,
                            "dieta_ia_gerada_em": firestore.SERVER_TIMESTAMP
                        })
                    except Exception as e:
                        print(f"Erro ao gerar dieta personalizada após atualização: {e}")
        return {
            "success": True,
            "message": "Conta atualizada com sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar conta: {e}")
@router.delete("/delete-account")
async def delete_account(
    current_user: dict = Depends(get_current_user)
):
    try:
        user_uid = current_user["uid"]
        db = get_firestore()
        from app.routes.chat import agentes_sessao
        if user_uid in agentes_sessao:
            del agentes_sessao[user_uid]
        user_ref = db.collection("users").document(user_uid)
        user_ref.delete()
        try:
            auth.delete_user(user_uid)
        except Exception as e:
            print(f"Erro ao deletar usuário do Firebase Auth: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao deletar conta do Firebase Auth: {str(e)}"
            )
        return {
            "success": True,
            "message": "Conta deletada com sucesso"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar conta: {e}")