from fastapi import FastAPI, Body, Depends, APIRouter
from app.models.user_model import User, UserLogin
from app.services.user_service import get_current_user, user_signup, user_login, profile_web

user_router = APIRouter()

@user_router.post('/adiciona', summary='Adiciona usuário')
async def usersignup(user: User = Body(default=None)):
    return user_signup(user)

@user_router.post('/login', summary='Login do usuário')
async def userlogin(user: UserLogin = Body(default=None)):
    return user_login(user)

@user_router.get('/profile', summary='Detalhes do usuário logado')
async def getprofile(current_user: str = Depends(get_current_user)):
    return  {"message": "Perfil acessado com sucesso!", "user": current_user}

@user_router.post("/profile_web", summary="Detalhes do usuário")
async def profileweb(user: UserLogin = Body(default=None), current_user: str = Depends(get_current_user)):
    return profile_web(user)