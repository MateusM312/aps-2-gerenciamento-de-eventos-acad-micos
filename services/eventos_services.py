# EVENTOS SERVICES
from fastapi import HTTPException

class EventoService:
    def __init__(self, repository, participante_repository):
        self.repository = repository
        self.participante_repository = participante_repository

    def editar_evento(self, id:int, dados):
        evento = self.repository.atualizar(id, dados)
        if evento is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        return evento    

    def inscrever(self, evento_id:int, participante_id:int):
        evento = self.repository.buscar_por_id(evento_id)
        inscritos = self.repository.listar_inscritos(evento_id)
        participante = self.participante_repository.buscar_por_id(participante_id)

        # REGRAS:
        if evento is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        if participante is None:
            raise HTTPException(status_code=404, detail="Participante não encontrado")
        if participante in inscritos:
            raise HTTPException(status_code=409, detail="Participante já inscrito neste evento")
        if len(inscritos) >= evento.capacidade:
            raise HTTPException(status_code=409, detail="Evento sem vagas disponíveis")

        self.repository.inscrever(evento_id, participante_id)
        return {"mensagem": "Inscrição realizada com sucesso"}

    def listar_inscritos(self, evento_id:int):
        evento = self.repository.buscar_por_id(evento_id)
        if evento is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        ids = self.repository.listar_inscritos(evento_id)
        return [self.participante_repository.buscar_por_id(i) for i in ids]


# Além dos recursos anteriores, a API deverá permitir que um participante se inscreva em um 
# evento. 
# Para isso, deverá existir uma rota semelhante a: 
# POST /eventos/{evento_id}/inscricoes/{participante_id} 
# A API deverá verificar, no mínimo: 
# 1.  Se o evento existe; 
# 2.  Se o participante existe; 
# 3.  Se o participante já está inscrito no evento; 
# 4.  Se o evento ainda possui vagas disponíveis. 
# Caso alguma dessas condições não seja atendida, a API deverá retornar um código HTTP 
# adequado e uma mensagem explicando o erro. 
# Também deverá existir uma forma de consultar os participantes inscritos em determinado 
# evento: 
# GET /eventos/{evento_id}/inscricoes 

# Consultar evento 
# GET /eventos/{id} 
# Deverá retornar os dados de um evento específico.
# Caso o evento não exista, a API deverá retornar um código HTTP adequado e uma 
# mensagem informando o problema.


