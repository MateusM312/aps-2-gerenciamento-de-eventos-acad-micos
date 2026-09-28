# REPOSITORIO PARTICIPANTES

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

    def buscar_por_id(self, id: int):
        for i in self.participantes:
            if i.id == id:
                return i

        return None

    def excluir(self, id: int):
        participante = self.buscar_por_id(id)
        if participante is None:
            return None
        self.participantes.remove(participante)
        return participante

    def atualizar(self, id: int, dados):
        participante = self.buscar_por_id(id)
        if participante is None:
            return None
        participante.nome = dados.nome
        participante.email = dados.email
        participante.curso = dados.curso
        return participante


# Cadastrar participante: (CHECK)
# POST /participantes

# Listar participantes: (CHECK)
# GET /participantes

# Consultar participante: (CHECK)
# GET /participantes/{id}

# Atualizar participante: (CHECK)
# PUT /participantes/{id}

# Excluir participante: (CHECK)
# DELETE /participantes/{id}