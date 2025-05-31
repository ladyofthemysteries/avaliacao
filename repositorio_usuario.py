import sqlite3
from modelos import SignUp, Usuario


class AuthDAO():

  def __init__(self):
    pass


  def buscar_usuario_por_email(self, email: str):
    with sqlite3.connect('usuario_tarefa.db') as conn:
      cursor = conn.cursor()
      sql = 'SELECT * FROM Usuario where email = ?'
      cursor.execute(sql, (email,))
      resultado = cursor.fetchone()

      if not resultado:
        return None

      usuario = Usuario(
        id=resultado[0],  username=resultado[1], 
        email=resultado[2],  senha=resultado[3], 
      )
      return usuario
  
  def buscar_usuario_por_username(self, username: str):
    with sqlite3.connect('usuario_tarefa.db') as conn:
      cursor = conn.cursor()
      sql = 'SELECT * FROM Usuario where username = ?'
      cursor.execute(sql, (username),)
      resultado = cursor.fetchone()

      if not resultado:
        return None

      usuario = Usuario(
        id=resultado[0],  username=resultado[1], 
        email=resultado[2],  senha=resultado[3], 
      )
      return usuario


  def criar_usuario(self, usuario: SignUp):
    with sqlite3.connect('usuario_tarefa.db') as conn:
      cursor = conn.cursor()

      sql = '''INSERT INTO Usuario(username, email, senha)
              VALUES (?, ?, ? )'''
      cursor.execute(sql, (usuario.username,usuario.email,
                usuario.senha))
      id = cursor.lastrowid
      return Usuario(id=id, **usuario.dict())