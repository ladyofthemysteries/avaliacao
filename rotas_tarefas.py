from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from modelos import Usuario, TarefaCreate, Tarefa
from repositorio_tarefas import TarefaDAO
from utils_auth import get_current_user

roteador_tarefas = APIRouter()
tarefas_dao = TarefaDAO()

@roteador_tarefas.post('/tarefas', status_code=status.HTTP_201_CREATED, response_model=Tarefa)
def tarefas_create(nova_tarefa: TarefaCreate, user: Annotated[Usuario, Depends(get_current_user)]):
    tarefa = tarefas_dao.inserir(nova_tarefa, user)
    return tarefa

@roteador_tarefas.get('/tarefas')
def veiculos_list(user: Annotated[Usuario, Depends(get_current_user)]):
    tarefas = tarefas_dao.todos_por_usuario(user)
    return tarefas


@roteador_tarefas.get('/tarefas/{id}')
def tarefas_detail(id: int, user: Annotated[Usuario, Depends(get_current_user)]):
   tarefa = tarefas_dao.obter_por_id(id)
   if tarefa:
    return tarefa
   else:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Não existe uma tarefa com id = {id}'
    )
  
@roteador_tarefas.delete('/tarefas/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_tarefa(id:int, user: Annotated[Usuario, Depends(get_current_user)]):
  if tarefas_detail(id):
    tarefas_dao.remover_por_id(id)
  else:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Não existe uma tarefa com id = {id}'
    )