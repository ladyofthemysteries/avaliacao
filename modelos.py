from pydantic import BaseModel
from typing import Optional


# USUÁRIOS
class UsuarioBase(BaseModel):
  username: str
  email: str
  password_hash: str

class Usuario(UsuarioBase):
  id: int



# TOKEN
class SignUpUser(UsuarioBase):
  pass

class SignInUser(BaseModel):
  email: str
  password_hash: str

# TAREFA
class TarefaBase(BaseModel):
  titulo: str
  descricao: Optional[str] = None
  concluida: bool = False

class TarefaUpdate(BaseModel):
    titulo: Optional[str]
    descricao: Optional[str]
    concluida: Optional[bool]

class Tarefa(TarefaBase):
  id: int 
  usuario_id: int


class TarefaCreate(TarefaBase):
  pass