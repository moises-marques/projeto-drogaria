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

# ------------------- CAIXA / REGISTRO DE VENDAS -------------------
@app.route('/caixa')
def caixa():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Adicionamos a lógica de busca aqui
    busca = request.args.get('busca')
    if busca:
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + busca + '%',))
    else:
        cursor.execute("SELECT * FROM produtos")
        
    produtos = cursor.fetchall()
    
    # Calcular total vendido
    cursor.execute("SELECT SUM(total) FROM vendas")
    total_vendido = cursor.fetchone()[0]
    if total_vendido is None:
        total_vendido = 0
    
    conn.close()
    return render_template('caixa.html', produtos=produtos, total_vendido=total_vendido, busca=busca)

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

# ------------------- REGISTRAR VENDA -------------------
@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    produto_id = request.form['produto_id']
    quantidade_vendida = int(request.form['quantidade'])
    
    # Busca o produto no banco de dados
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        flash("Produto não encontrado!")
        return redirect(url_for('caixa'))

    preco_unitario = produto[2]
    estoque_atual = produto[3]
    
    # Verifica se a quantidade em estoque é suficiente
    if quantidade_vendida > estoque_atual:
        flash("Erro: Estoque insuficiente!")
        conn.close()
        return redirect(url_for('caixa'))
        
    # Calcula o total da venda e atualiza o estoque
    total_venda = preco_unitario * quantidade_vendida
    novo_estoque = estoque_atual - quantidade_vendida
    
    # Registra a venda na tabela de vendas
    cursor.execute("INSERT INTO vendas (produto_id, quantidade, total) VALUES (?, ?, ?)", 
               (produto_id, quantidade_vendida, total_venda))
    
    # Atualiza o estoque do produto
    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, produto_id))
    
    conn.commit()
    conn.close()

    flash(f'Venda registrada com sucesso! Total: R$ {total_venda:.2f}')
    return redirect(url_for('caixa'))

if __name__ == '__main__':
    app.run(debug=True)
