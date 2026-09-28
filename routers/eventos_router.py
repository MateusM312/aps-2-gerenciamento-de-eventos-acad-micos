from fastapi import APIRouter, HTTPException, Depends
from model.eventos_model import Evento
from services.eventos_services import EventoService
from repositories.eventos_repository import EventoRepository
from repositories.participantes_repository import ParticipantesRepositorio

router = APIRouter(prefix="/eventos", tags=["Eventos"])

repository = EventoRepository()
repository_participantes = ParticipantesRepositorio()
service = EventoService(repository, repository_participantes)

def get_evento_service():
    return service


# Cadastrar evento
# POST /eventos
# Deverá receber os dados do evento em formato JSON e retornar o evento cadastrado.

@router.post("/")
def cadastrar_evento(evento: Evento, service: EventoService = Depends(get_evento_service)):
    return service.repository.salvar(evento)


# Listar eventos
# GET /eventos
# Deverá retornar a lista de eventos cadastrados.

@router.get("/")
def listar_eventos(service: EventoService = Depends(get_evento_service)):
    return service.repository.listar()


# Consultar evento
# GET /eventos/{id}
# Deverá retornar os dados de um evento específico.
# Caso o evento não exista, a API deverá retornar um código HTTP adequado e uma
# mensagem informando o problema.

@router.get("/{id}")
def consultar_evento(id: int, service: EventoService = Depends(get_evento_service)):
    evento = service.repository.buscar_por_id(id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return evento


# Atualizar evento
# PUT /eventos/{id}
# Deverá permitir a atualização dos dados de um evento existente.

@router.put("/{id}")
def atualizar_evento(id: int, evento: Evento, service: EventoService = Depends(get_evento_service)):
    return service.editar_evento(id, evento)


# Excluir evento
# DELETE /eventos/{id}
# Deverá remover um evento existente.

@router.delete("/{id}")
def excluir_evento(id: int, service: EventoService = Depends(get_evento_service)):
    evento = service.repository.remover(id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return {"mensagem": "Evento removido"}


# Inscrever participante:
# POST /eventos/{evento_id}/inscricoes/{participante_id}

@router.post("/{evento_id}/inscricoes/{participante_id}")
def inscrever_participante(evento_id: int, participante_id: int, service: EventoService = Depends(get_evento_service)):
    return service.inscrever(evento_id, participante_id)


# Listar participantes inscritos em um evento
# GET /eventos/{evento_id}/inscricoes

@router.get("/{evento_id}/inscricoes")
def listar_inscritos(evento_id: int, service: EventoService = Depends(get_evento_service)):
    return service.listar_inscritos(evento_id)