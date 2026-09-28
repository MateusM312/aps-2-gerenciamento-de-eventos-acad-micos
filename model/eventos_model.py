from pydantic import BaseModel

# Exemplos:
# class Filme(BaseModel):
#     id: int | None = None
#     titulo: str
#     diretor: str
#     estoque: int

class Evento(BaseModel):
    id: int | None = None
    titulo: str
    descricao: str
    data: str
    horario: str
    local: str
    capacidade: int
    categoria: str


# ●  id 
# ●  titulo 
# ●  descricao 
# ●  data 
# ●  horario 
# ●  local 
# ●  capacidade 
# ●  categoria

# Exemplos de categorias: 
# ●  Palestra 
# ●  Workshop 
# ●  Minicurso 
# ●  Seminário 
# ●  Competição