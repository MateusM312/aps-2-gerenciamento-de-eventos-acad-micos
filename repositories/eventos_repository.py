#  EVENTOS REPOSITORY

class EventoRepository:
    def __init__(self):
        self.eventos = []
        self._proximo_evento = 1
        self.inscricoes = {}

    def salvar(self, evento):
        evento.id = self._proximo_evento
        self._proximo_evento += 1
        self.eventos.append(evento)
        return evento

    def listar(self):
        return self.eventos

    def buscar_por_id(self, id:int):
        for i in self.eventos:
            if i.id == id:
                return i
        return None

    def remover(self, id: int):
        evento = self.buscar_por_id(id)
        if evento is None:
            return None
        self.eventos.remove(evento)
        return evento

    def atualizar(self, dados):
        evento = self.buscar_por_id(id)
        if evento is None:
            return None
        evento.titulo = dados.titulo
        evento.descricao = dados.descricao
        evento.data = dados.data
        evento.horario = dados.horario
        evento.local = dados.local
        evento.capacidade = dados.capacidade
        evento.categoria = dados.categoria
        return evento

    def inscrever(self, evento_id:int, participante_id:int):
        self.inscricoes.setdefault(evento_id, []).append(participante_id)

    def listar_inscritos(self, evento_id: int):
        return self.inscricoes.get(evento_id, [])

# Cadastrar evento (CHECK)
# POST /eventos 
# Deverá receber os dados do evento em formato JSON e retornar o evento cadastrado. 

# Listar eventos (CHECK)
# GET /eventos 
# Deverá retornar a lista de eventos cadastrados. 

# Consultar evento 
# GET /eventos/{id} 
# Deverá retornar os dados de um evento específico. 
# Caso o evento não exista, a API deverá retornar um código HTTP adequado e uma 
# mensagem informando o problema. 

# Atualizar evento 
# PUT /eventos/{id} 
# Deverá permitir a atualização dos dados de um evento existente. 

# Excluir evento 
# DELETE /eventos/{id} 
# Deverá remover um evento existente.