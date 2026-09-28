# EVENTOS SERVICES
from fastapi import HTTPException

class ParticipantesService:
    def __init__(self, participante_repository):
        self.participante_repository = participante_repository

    def editar_participante(self, id:int, dados):
        participante = self.participante_repository.atualizar(id, dados)
        if participante is None:
            raise HTTPException(status_code=404, detail="participante não encontrado")
        return participante    