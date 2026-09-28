
class EventoService:
    def __init__(self, repository):
        self.repository = repository

    def editar_evento(self, id:int, dados):
        evento = self.repository.atualizar(id, dados)
        if evento is None:
            raise ValueError(status_code=404, detail="Evento não encontrado")
        return evento    




# Consultar evento 
# GET /eventos/{id} 
# Deverá retornar os dados de um evento específico.
# Caso o evento não exista, a API deverá retornar um código HTTP adequado e uma 
# mensagem informando o problema.


