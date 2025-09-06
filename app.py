import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "senha_super_secreta"

# Usuários de teste
usuarios = {
    "admin": "1234",
    "funcionario": "abcd"
}

# ------------------- LOGIN -------------------
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario in usuarios and usuarios[usuario] == senha:
        return redirect(url_for('cadastro_produto'))
    else:
        flash("Usuário ou senha inválidos!")
        return redirect(url_for('login'))

# ------------------- CADASTRO DE PRODUTOS -------------------
@app.route('/cadastro_produto')
def cadastro_produto():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return render_template('cadastro_produto.html', produtos=produtos)

@app.route('/salvar_produto', methods=['POST'])
def salvar_produto():
    nome = request.form['nome']
    preco = float(request.form['preco'])
    quantidade = int(request.form['quantidade'])
    validade = request.form['validade']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, preco, quantidade, validade) VALUES (?, ?, ?, ?)",
        (nome, preco, quantidade, validade)
    )
    conn.commit()
    conn.close()

    flash("Produto cadastrado com sucesso!")
    return redirect(url_for('cadastro_produto'))

# ------------------- EDITAR PRODUTO -------------------
@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        validade = request.form['validade']
        cursor.execute(
            "UPDATE produtos SET nome=?, preco=?, quantidade=?, validade=? WHERE id=?",
            (nome, preco, quantidade, validade, id)
        )
        conn.commit()
        conn.close()
        flash("Produto atualizado com sucesso!")
        return redirect(url_for('cadastro_produto'))
    
    cursor.execute("SELECT * FROM produtos WHERE id=?", (id,))
    produto = cursor.fetchone()
    conn.close()
    return render_template('editar_produto.html', produto=produto)

# ------------------- DELETAR PRODUTO -------------------
@app.route('/deletar_produto/<int:id>')
def deletar_produto(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Produto deletado com sucesso!")
    return redirect(url_for('cadastro_produto'))

# ------------------- CAIXA / REGISTRO DE VENDAS -------------------
@app.route('/caixa')
def caixa():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Buscar todos os produtos
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    
    # Calcular total vendido
    cursor.execute("SELECT SUM(total) FROM vendas")
    total_vendido = cursor.fetchone()[0]
    if total_vendido is None:
        total_vendido = 0
    
    conn.close()
    return render_template('caixa.html', produtos=produtos, total_vendido=total_vendido)

@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    produto_id = int(request.form['produto_id'])
    quantidade_vendida = int(request.form['quantidade'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT preco, quantidade FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()
    if not produto:
        flash("Produto não encontrado!")
        conn.close()
        return redirect(url_for('caixa'))

    preco, estoque_atual = produto

    if quantidade_vendida > estoque_atual:
        flash("Erro: Estoque insuficiente!")
        conn.close()
        return redirect(url_for('caixa'))

    total = preco * quantidade_vendida

    cursor.execute(
        "INSERT INTO vendas (produto_id, quantidade, total) VALUES (?, ?, ?)",
        (produto_id, quantidade_vendida, total)
    )

    novo_estoque = estoque_atual - quantidade_vendida
    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, produto_id))

    conn.commit()
    conn.close()

    flash(f"Venda registrada com sucesso! Total: R$ {total:.2f}")
    return redirect(url_for('caixa'))

# ------------------- INICIAR O SISTEMA -------------------
if __name__ == '__main__':
    app.run(debug=True)
