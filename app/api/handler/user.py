from fastapi import FastAPI, Body, Depends, HTTPException, APIRouter
from app.models.user_model import User, UserLogin
from app.api.auth.jwt_handler import signJWT
from app.core.database import add_user_to_firebase
from app.services.user_service import check_user_in_firebase, add_user_to_firebase, check_duplicate_email
from app.api.auth.jwt_bearer import JWTBearer
from app.services.user_service import get_current_user

user_router = APIRouter()

@user_router.post('/adiciona', summary='Adiciona usuário')
def user_signup(user: User = Body(default=None)):
    if check_duplicate_email(user.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    try:
        user_id = add_user_to_firebase(user)
        return {"user_id": user_id, "message": "Usuário cadastrado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao cadastrar usuário")

@user_router.post('/login', summary='Login')
def user_login(user_login: UserLogin = Body(default=None)):
    if check_user_in_firebase(user_login):
        return {"message": "Login bem-sucedido", "token": signJWT(user_login.email)}
    else:
        return {"error": "Credenciais de login inválidas"}

@user_router.get('/profile', summary='Detalhes do usuário logado')
def get_profile(current_user: str = Depends(get_current_user)):
    return {"message": "Perfil acessado com sucesso!", "user": current_user}

@user_router.get("/testar_token")
async def testar_token(current_user: str = Depends(JWTBearer())):
    return {"mensagem": "Token válido"}