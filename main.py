from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import eventos_router, participantes_routers
# precisa importar o router

app = FastAPI(title="Gerenciamento de eventos acadêmicos - Santana & Mendes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # em produção, restrinja a origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eventos_router.router)
app.include_router(participantes_routers.router)