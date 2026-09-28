from fastapi import APIRouter, HTTPException, Depends
from model.participantes_model import Participante
from repositories.participantes_repository import ParticipantesRepositorio
from services.participantes_service import ParticipantesService

router = APIRouter(prefix="/participantes", tags=["Participante"])

repository = ParticipantesRepositorio()
service = ParticipantesService(repository)

def get_participante_service():
    return service


# Cadastrar participante:
# POST /participantes

@router.post("/")
def cadastrar_participante(dados: Participante, service: ParticipantesService = Depends(get_participante_service)):
    return service.participante_repository.salvar(dados)


# Listar participantes:
# GET /participantes

@router.get("/")
def listar_participantes(service: ParticipantesService = Depends(get_participante_service)):
    return service.participante_repository.listar_participantes()


# Consultar participante:
# GET /participantes/{id}

@router.get("/{id}")
def consultar_participante(id: int, service: ParticipantesService = Depends(get_participante_service)):
    participante = service.participante_repository.buscar_por_id(id)
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    return participante


# Atualizar participante:
# PUT /participantes/{id}

@router.put("/{id}")
def atualizar_participantes(id: int, dado: Participante, service: ParticipantesService = Depends(get_participante_service)):
    return service.editar_participante(id, dado)


# Excluir participante:
# DELETE /participantes/{id}

@router.delete("/{id}")
def excluir_participantes(id: int, service: ParticipantesService = Depends(get_participante_service)):
    participante = service.participante_repository.excluir(id)
    if participante is None:
        raise HTTPException(status_code=404, detail="Participante não encontrado")
    return {"mensagem": "Participante removido"}