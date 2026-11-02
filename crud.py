from database import conexao, cursor

# FETCHALL - PRECISA DO FOR PQ É UMA LISTA
# FETCHONE - NÃO PRECISA DO FOR PQ É TUPLA

# CRUD DE AUTENTICAÇÃO
def registrar_usuario(usuario, senha):
    cursor.execute("""INSERT INTO usuarios (usuario, senha) VALUES (?, ?)""", (usuario, senha))
    conexao.commit()

def verificar_usuario(usuario, senha):
    cursor.execute("""SELECT * FROM usuarios WHERE usuario = ? AND senha = ?""", (usuario, senha))
    resultado = cursor.fetchone()

    return resultado


# CRUD DE TRANSAÇÕES
def cadastrar_transacao(tipo, descricao, valor, data, usuario_id):
    cursor.execute("""
        INSERT INTO transacoes (tipo, descricao, valor, data, usuario_id) 
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, descricao, valor, data, usuario_id))
    conexao.commit()


# LISTA TRANSAÇÕES
def gerar_lista_transacoes():
    cursor.execute("""SELECT tipo, descricao, valor, data, usuario_id FROM transacoes""")
    membros = cursor.fetchall() # Buscar todos os registros (como preencher a tabela com a lista completa de membros)
    return membros

# CALCULAR TOTAL
def calcular_total(tipo, usuario_id):
    cursor.execute("""
        SELECT SUM(valor) FROM transacoes 
        WHERE tipo = ? AND usuario_id = ?
    """, (tipo, usuario_id))
    
    resultado = cursor.fetchone()[0]
    
    # Se o resultado for None (porque ainda não tem transações cadastradas), retornamos 0.0
    if resultado is None:
        return 0.0
    
    return resultado