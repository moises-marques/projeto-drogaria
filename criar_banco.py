import sqlite3

# Conectar (se não existir, cria o arquivo database.db)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Criar tabela de produtos
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    validade TEXT
)
""")

# Criar tabela de vendas
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    total REAL NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
)
""")

# Salvar alterações e fechar
conn.commit()
conn.close()

print("Banco de dados criado com sucesso! ✅")
