import sqlite3

from modelos import Usuario, Tarefa, TarefaCreate

class TarefaDAO:

    def __init__(self):
        pass

    def criar_tarefa(self, user:Usuario, tarefa: TarefaCreate):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            sql = 'INSERT INTO Tarefa(titulo,descricao,concluida,usuario_id) VALUES (?,?,?,?)'
            cursor.execute(sql,(tarefa.titulo, tarefa.descricao, int(tarefa.concluida), user.id))
            id = cursor.lastrowid
            return Tarefa(id=id, usuario_id= user.id,**tarefa.dict())


    def listar_tarefas(self, user: Usuario):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            query = 'SELECT * FROM Tarefa WHERE usuario_id =?;'
            cursor.execute(query, (user.id,))
            tarefas_list = cursor.fetchall()
            tarefas: list[Tarefa] = []
            for t in tarefas_list:
                tarefa = Tarefa(
                        id=t[0],
                        titulo=t[1],
                        descricao=t[2],
                        concluida=bool(t[3]),
                        usuario_id=t[4]
                    )
                tarefas.append(tarefa)
            return tarefas


    def listar_tarefas_por_id(self, user: Usuario, id: int):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM Tarefa WHERE id = ? and usuario_id = ?'
            cursor.execute(sql, (id, user.id))
            resultado = cursor.fetchone()
            if not resultado:
                return None
            tarefa = Tarefa(
                id=resultado[0],
                titulo=resultado[1],
                descricao=resultado[2],
                concluida=bool(resultado[3]),
                usuario_id=resultado[4]
            )
            return tarefa


    def remover_por_id(self, id: int, user: Usuario):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            sql = 'DELETE FROM Tarefa WHERE id = ? and usuario_id = ?'
            cursor.execute(sql, (id, user.id))
            resultado = cursor.fetchone()
            if not resultado:
                return None 


    def atualizar_tarefa(self, id: int, tarefa: Tarefa, user: Usuario):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            sql = '''
                UPDATE Tarefa
                SET titulo = ?, descricao = ?, concluida = ?
                WHERE id = ? AND usuario_id = ?
            '''
            cursor.execute(sql, (
                tarefa.titulo,
                tarefa.descricao,
                int(tarefa.concluida),
                id,
                user.id
            ))
            return Tarefa(id=id, usuario_id=user.id, **tarefa.dict())