# REPOSITORIO CLIENTES

class ParticipantesRepositorio:
    def __init__(self):
        self.participantes = []
        self._proximo_id = 1

    def salvar(self, participante):
        participante.id = self._proximo_id
        self._proximo_id += 1
        self.participantes.append(participante)
        return participante

    def listar_participantes(self):
        return self.participantes

    def buscar_por_id(self, id:int):
        for i in self.participantes:
            if i.id == id:
                return i

    def excluir(self, id:int):
        participante = self.buscar_por_id(id)
        if participante is None:
            return None
        self.participantes.remove(participante)

    def atualizar(self, dados, id:int):
        participante = self.buscar_por_id(id)
        if participante is None:
            return None
        participante.nome = dados.nome
        participante.email = dados.email
        return participante

# Cadastrar participante: (CHECK) 
# POST /participantes 

# Listar participantes: (CHECK)
# GET /participantes 

# Consultar participante: (CHECK)
# GET /participantes/{id} 

# Atualizar participante: 
# PUT /participantes/{id} 

# Excluir participante: 
# DELETE /participantes/{id} 

# MODEL PARTICIPANTE


# class Participante(BaseModel):
#     id: int | None = None
#     nome: str
#     email: str
#     curso: str