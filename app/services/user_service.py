from firebase_admin import db
from passlib.context import CryptContext
import bcrypt
from fastapi import HTTPException, Depends
from api.auth.jwt_bearer import JWTBearer
from fastapi import FastAPI, Body, Depends, HTTPException, APIRouter
from models.user_model import User, UserLogin
from api.auth.jwt_bearer import JWTBearer
from api.auth.jwt_handler import signJWT
from core.database import add_user_to_firebase

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password, hashed_password):
    if plain_password is None or hashed_password is None:
        return False
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def add_user_to_firebase(user):
    if check_duplicate_email(user.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    hashed_password = hash_password(user.password)
    new_user_ref = db.reference("/users").push(
        {
            "email": user.email,
            "username": user.username,
            "id_discord": user.id_discord,
            "password": hashed_password,
        }
    )
    return new_user_ref.key

def check_duplicate_email(email):
    users_ref = db.reference("/users")
    users_snapshot = users_ref.get()
    if users_snapshot:
        for _, user_data in users_snapshot.items():
            if user_data.get("email") == email:
                return True
    return False

def check_user_in_firebase(data):
    users_ref = db.reference("/users")
    users_snapshot = users_ref.get()
    if users_snapshot:
        for user_id, user_data in users_snapshot.items():
            stored_password = user_data.get("password")
            if user_data.get("email") == data.email and verify_password(data.password, stored_password):
                return True, user_data.get("username"), user_data.get("id_discord")
    return False, None, None

def get_user_by_email(email):
    users_ref = db.reference("/users")
    users_snapshot = users_ref.get()
    if users_snapshot:
        for user_id, user_data in users_snapshot.items():
            if user_data.get("email") == email:
                return user_data
    return None

def get_current_user(token: str = Depends(JWTBearer())):
    return token

def user_signup(user: User = Body(default=None)):
    if check_duplicate_email(user.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    try:
        user_id = add_user_to_firebase(user)
        return {"user_id": user_id, "message": "Usuário cadastrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao cadastrar usuário")
    
def user_login(user_login: UserLogin = Body(default=None)):
    found, username, id_discord = check_user_in_firebase(user_login)
    if found:
        return {"message": "Login bem-sucedido", "token": signJWT(user_login.email)}
    else:
        raise HTTPException(status_code=401, detail="Credenciais de login inválidas")
    
def profile_web(user_login: UserLogin = Body(default=None)):
    found, username, id_discord = check_user_in_firebase(user_login)
    if found:
        return {"id_discord": id_discord, "username": username}
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")