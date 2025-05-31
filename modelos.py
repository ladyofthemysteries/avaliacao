from pydantic import BaseModel
from typing import Optional


# USUÁRIOS
class UsuarioBase(BaseModel):
  username: str
  email: str
  senha: str

class Usuario(UsuarioBase):
  id: int 

# TOKEN
class SignUp(UsuarioBase):
  pass

class SignIn(BaseModel):
  email: str
  senha: str

# TAREFA
class TarefaBase(BaseModel):
  titulo: str
  descricao: Optional[str] = None
  concluida: Optional[bool] = False

class Tarefa(TarefaBase):
  id: int
  usuario_id: int 


class TarefaCreate(TarefaBase):
  pass