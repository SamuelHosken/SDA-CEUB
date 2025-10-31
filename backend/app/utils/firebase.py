import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.config import settings
import os
import json
firebase_app = None
db = None
def init_firebase():
    global firebase_app, db
    if firebase_app is not None:
        return firebase_app
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH") or settings.firebase_credentials_path
    if not os.path.isabs(cred_path):
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        cred_path_abs = os.path.join(backend_dir, cred_path.lstrip("./"))
    else:
        cred_path_abs = cred_path
    if cred_path_abs and os.path.exists(cred_path_abs):
        cred = credentials.Certificate(cred_path_abs)
        firebase_app = firebase_admin.initialize_app(cred)
    elif os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)
    elif os.getenv("FIREBASE_CREDENTIALS_JSON"):
        cred_dict = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))
        cred = credentials.Certificate(cred_dict)
        firebase_app = firebase_admin.initialize_app(cred)
    else:
        raise ValueError(
            f"Firebase não configurado. Arquivo não encontrado em: {cred_path_abs} ou {cred_path}. "
            "Defina FIREBASE_CREDENTIALS_PATH ou FIREBASE_CREDENTIALS_JSON"
        )
    db = firestore.client()
    return firebase_app
def get_firestore():
    if db is None:
        init_firebase()
    return db
def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Token inválido: {str(e)}")
def get_user_by_uid(uid: str):
    try:
        user_record = auth.get_user(uid)
        return user_record
    except Exception as e:
        raise ValueError(f"Usuário não encontrado: {str(e)}")