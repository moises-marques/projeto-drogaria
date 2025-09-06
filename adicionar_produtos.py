import sqlite3

# Conectar ao banco
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Lista de produtos de teste
produtos = [
    ("Paracetamol", 5.50, 20, "2026-12-31"),
    ("Dipirona", 3.75, 15, "2025-12-31"),
    ("Vitamina C", 10.00, 30, "2027-06-30"),
    ("Água Oxigenada", 7.50, 10, "2026-03-31")
]

# Inserir produtos
for p in produtos:
    cursor.execute(
        "INSERT INTO produtos (nome, preco, quantidade, validade) VALUES (?, ?, ?, ?)",
        p
    )

conn.commit()
conn.close()

print("Produtos de teste adicionados com sucesso!")
