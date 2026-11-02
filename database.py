import sqlite3

conexao = sqlite3.connect("gestor.db")
cursor = conexao.cursor()

# TABELA DE USUÁRIOS/LOGIN
cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL
                )""")

# TABELA DE TRANSAÇÕES
cursor.execute("""CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )""")