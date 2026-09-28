from fastapi import APIRouter, HTTPException, Depends
from model.eventos_model import Evento
from services.eventos_services import EventoService
from repositories.eventos_repository import EventoRepository

router = APIRouter(prefix="/eventos", tags=["Eventos"])

repository = EventoRepository
service = EventoService(repository)

def get_evento_service():
    return service

# Cadastrar evento ()
# POST /eventos 
# Deverá receber os dados do evento em formato JSON e retornar o evento cadastrado. 

@router.post("/")
def cadastrar_evento(evento: Evento, service: EventoService = Depends(get_evento_service)):
    try:
        repository.salvar(evento)
    except ValueError as e:
        raise HTTPException(400, str(e))

# Listar eventos ()
# GET /eventos 
# Deverá retornar a lista de eventos cadastrados. 

@router.get("/")
def listar_eventos():
    try:
        repository.listar()
    except ValueError as e:
        raise HTTPException(404, str(e))

# Consultar evento ()
# GET /eventos/{id} 
# Deverá retornar os dados de um evento específico. 
# Caso o evento não exista, a API deverá retornar um código HTTP adequado e uma 
# mensagem informando o problema. 

@router.get("/{id}")
def consultar_evento(id: int):
    try:
        repository.buscar_por_id(id)
    except ValueError as e:
        HTTPException(404, str(e))

# Atualizar evento ()
# PUT /eventos/{id} 
# Deverá permitir a atualização dos dados de um evento existente. 

@router.put("/{id}")
def atualizar_evento(id:int, evento:Evento, service: EventoService = Depends(get_evento_service)):
    try:
        service.editar_evento(id, evento)
    except ValueError as e:
        HTTPException(404, str(e))

# Excluir evento ()
# DELETE /eventos/{id} 
# Deverá remover um evento existente.

@router.delete("/{id}")
def excluir_evento(id:int):
    try:
        repository.remover(id)
    except ValueError as e:
        HTTPException(404, str(e))


#Inscrever participante:
@router.post("/{evento_id}/inscricoes/{participante_id}")
def inscrever_participante(evento_id:int, participante_id:int, service: EventoService = Depends(get_evento_service)):
    try:
        service.inscrever(evento_id, participante_id)
    except ValueError as e:
        HTTPException(404, str(e))

# Listar participantes de certo evento

@router.get("/participantes/{evento_id}")
def listar_participantes(evento_id:int, services: EventoService = Depends(get_evento_service)):
    try:
        service.listar_inscritos(evento_id)
    except ValueError as e:
        HTTPException(404, str(e))