from pydantic import BaseModel

# ●  id 
# ●  nome 
# ●  email 
# ●  curso 

class Participante(BaseModel):
    id: int | None = None
    nome: str
    email: str
    curso: str