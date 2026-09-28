from fastapi import APIRouter, HTTPException, Depends
from model.participantes_model import Participante 
from repositories.participantes_repository import ParticipantesRepositorio
from services.participantes_service import ParticipantesService

router = APIRouter(prefix="/participantes", tags=["Participante"])

repository = ParticipantesRepositorio
service = ParticipantesService(repository)

def get_participante_service():
    return service


# Cadastrar participante: 
# POST /participantes 

@router.post("/")
def cadastrar_participante(dados: Participante):
    try:
        ParticipantesRepositorio.salvar(dados)
    except ValueError as e:
        HTTPException(404, str(e))

# Listar participantes: 
# GET /participantes 
@router.get("/")
def listar_participantes():
    try:
        ParticipantesRepositorio.listar_participantes()
    except ValueError as e:
        HTTPException(404, str(e))

# Consultar participante: 
# GET /participantes/{id} 
@router.get("/{id}")
def consultar_participante(id:int):
    try:
        ParticipantesRepositorio.buscar_por_id(id)
    except ValueError as e:
        HTTPException(404, str(e))

# Atualizar participante: 
# PUT /participantes/{id} 
@router.put("/{id}")
def atualizar_participantes(id:int, dado: Participante):
    try:
        ParticipantesService.editar_participante(id, dado)
    except ValueError as e:
        HTTPException(404, str(e))

# Excluir participante: 
# DELETE /participantes/{id} 
@router.delete("/{id}")
def excluir_participantes(id:int):
    try:
        ParticipantesRepositorio.excluir(id)
    except ValueError as e:
        HTTPException(404, str(e))