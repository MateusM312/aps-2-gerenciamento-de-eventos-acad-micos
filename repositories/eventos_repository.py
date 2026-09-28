# segundo a fazer

# class FilmeRepository:
#     def __init__(self):
#         self.filmes = []
#         self._proximo_filme = 1

#     def salvar(self, filme):
#         filme.id = self._proximo_filme
#         self._proximo_filme += 1
#         self.filmes.append(filme)
#         return filme

#     def listar(self):
#         return self.filmes

#     def buscar_por_id(self, id_filme:int):
#         for filme in self.filmes:
#             if filme.id == id_filme:
#                 return filme
#         return None

class EventoRepository:
    def __init__(self):
        self.eventos = []
        self._proximo_evento = 1

    def salvar(self, evento):
        evento.id = self._proximo_evento
        self._proximo_evento += 1
        self.eventos.append(evento)
        return evento

    def listar(self):
        return self.eventos

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