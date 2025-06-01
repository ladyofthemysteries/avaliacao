from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from modelos import Usuario, TarefaCreate, Tarefa
from repositorio_tarefas import TarefaDAO
from utils_auth import get_current_user

roteador_tarefas = APIRouter()
tarefas_dao = TarefaDAO()

@roteador_tarefas.post('/criartarefas', status_code=status.HTTP_201_CREATED)
def criar_tarefas(nova_tarefa: TarefaCreate, user: Annotated[Usuario, Depends(get_current_user)]):
    tarefa = tarefas_dao.criar_tarefa(user, nova_tarefa)
    return tarefa

@roteador_tarefas.get('/listartarefas')
def listar_tarefas(user: Annotated[Usuario, Depends(get_current_user)]):
    tarefas = tarefas_dao.listar_tarefas(user)
    return tarefas


@roteador_tarefas.get('/tarefas/{id}')
def tarefas_detail(id: int, user: Annotated[Usuario, Depends(get_current_user)]):
   tarefa = tarefas_dao.obter_por_id(user, id)
   if tarefa:
    return tarefa
   else:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Não existe uma tarefa com id = {id}'
    )

@roteador_tarefas.put('/atualizartarefa/{id}',status_code=status.HTTP_200_OK)
def atualizar_tarefa(user:Annotated[Usuario,Depends(get_current_user)],id:int,tarefa: TarefaCreate):
    if tarefas_dao.listar_tarefa_por_id(id, user):
        return tarefas_dao.atualizar_tarefa(id, tarefa, user)

@roteador_tarefas.delete('/deletartarefas/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_tarefa(id:int, user: Annotated[Usuario, Depends(get_current_user)]):
  tarefa = tarefas_dao.obter_por_id(id)
  if tarefa:
    tarefas_dao.remover_por_id(id, user)
  else:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Não existe uma tarefa com id = {id}'
    )
  

@roteador_tarefas.get('/me',status_code=status.HTTP_200_OK)
def exibir(user:Annotated[Usuario,Depends(get_current_user)]):
    return {
        'Username':user.username,
        'Email': user.email,
        'Id': user.id  } 