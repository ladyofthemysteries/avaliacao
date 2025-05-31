from fastapi import FastAPI
from rotas_auth import router as roteador_auth
from rotas_tarefas import roteador_tarefas

app = FastAPI()

app.include_router(roteador_auth)
app.include_router(roteador_tarefas)

if __name__ == '__main__':
    main()