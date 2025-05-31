import sqlite3

from modelos import Usuario, Tarefa, TarefaCreate

class TarefaDAO:

    def __init__(self):
        pass

    def todos(self):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            select_query = 'SELECT * FROM Tarefa;'
            cursor.execute(select_query)
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
        
    def todos_por_usuario(self, usuario: Usuario):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            select_query = 'SELECT * FROM Tarefa WHERE usuario_id = ?;'
            cursor.execute(select_query, (usuario.id,))
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

    def obter_por_id(self, id: int):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            sql = 'SELECT * FROM Tarefa WHERE id = ?'
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            if not result:
                return None
            tarefa = Tarefa(
                id=result[0],
                titulo=result[1],
                descricao=result[2],
                concluida=bool(result[3]),
                usuario_id=result[4]
            )
            return tarefa

    def remover_por_id(self, id: int):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            sql = 'DELETE FROM Tarefa WHERE id = ?'
            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()
            if not resultado:
                return 

    def inserir(self, tarefa: TarefaCreate, usuario: Usuario):
        with sqlite3.connect('usuario_tarefa.db') as connection:
            cursor = connection.cursor()
            sql = '''
                INSERT INTO Tarefa(titulo, descricao, concluida, usuario_id)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(sql, (
                tarefa.titulo,
                tarefa.descricao,
                int(tarefa.concluida),
                usuario.id
            ))
            id = cursor.lastrowid
            return Tarefa(id=id, **tarefa.dict())

    def atualizar(self, id: int, tarefa: TarefaCreate, usuario: Usuario):
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
                usuario.id
            ))