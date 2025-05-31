from fastapi import FastAPI
from rotas_tarefas import roteador_tarefas
from rotas_auth import router as roteador_auth


app = FastAPI()

# As rotas GET /tasks, POST /tasks, PUT /tasks/{id}
app.include_router(roteador_tarefas)

# Rotas de Autenticaco POST /auth/signup, POST /auth/login, GET /auth/me
app.include_router(roteador_auth)
