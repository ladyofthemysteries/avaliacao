from pydantic import BaseModel
from typing import Optional


# USUÁRIOS
class UsuarioBase(BaseModel):
  username: str
  email: str
  senha: str

class Usuario(UsuarioBase):
  id: int |  None = None

# TOKEN
class SignUp(UsuarioBase):
  pass

class SignIn(BaseModel):
  email: str
  senha: str

# TAREFA
class TarefaBase(BaseModel):
  titulo: str
  descricao: str | None = None
  concluida: bool = False

class Tarefa(TarefaBase):
  id: int | None = None
  usuario_id: int | None = None


class TarefaCreate(TarefaBase):
  pass