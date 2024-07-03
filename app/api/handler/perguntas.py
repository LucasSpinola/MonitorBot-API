from fastapi import Depends, APIRouter
from services.user_service import get_current_user
from models.pergunta_models import Pergunta
from services.pergunta_service import criapergunta, editapergunta, deletapergunta, listaperguntas, lepergunta

perguntas_router = APIRouter()

@perguntas_router.post("/cria_pergunta/", summary="Cria uma pergunta no banco de dados")
async def cria_pergunta(pergunta: Pergunta, current_user: str = Depends(get_current_user)):
    return await criapergunta(pergunta)

@perguntas_router.put("/edita_pergunta/{id}/", summary="Edita uma pergunta no banco de dados")
async def edita_pergunta(id: str, pergunta: Pergunta, current_user: str = Depends(get_current_user)):
    return await editapergunta(id, pergunta)
    
@perguntas_router.delete("/deleta_pergunta/{id}/", summary="Deleta uma pergunta no banco de dados")
async def deleta_pergunta(id: str, current_user: str = Depends(get_current_user)):
    return await deletapergunta(id)

@perguntas_router.get("/lista_perguntas/", summary="Lista todas as perguntas do banco de dados")
async def lista_perguntas(current_user: str = Depends(get_current_user)):
    return await listaperguntas()
    
@perguntas_router.get("/le_pergunta/{id}/", summary="Lê uma pergunta do banco de dados")
async def le_pergunta(id: str, current_user: str = Depends(get_current_user)):
    return await lepergunta(id)