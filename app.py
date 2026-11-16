from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="Cinema",
        user="postgres",
        password="senai",
        port="5432"
    )
    return banco

@app.route('/')
def inicio():
    return render_template("index.html")


# Tabela 1 - Filmes (Mateus Tripudi do Nascimento (23))
@app.route('/filmes')
def filmes():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""SELECT id, titulo, genero, duracao_min,
                      data_lancamento FROM filme ORDER BY id""")
    lista = cursor.fetchall()
    banco.close()
    return render_template("filmes.html", filmes=lista)

@app.route("/filmes/enviar", methods=["POST"])
def enviar_filme():
    titulo = request.form.get("titulo")
    genero = request.form.get("genero")
    duracao_min = request.form.get("duracao_min")
    data_lancamento = request.form.get("data_lancamento")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO filme
                   (titulo, genero, duracao_min, data_lancamento)
                   VALUES (%s, %s, %s, %s)""",
                   (titulo, genero, duracao_min, data_lancamento))
    banco.commit()
    banco.close()
    return redirect("/filmes")

@app.route("/filmes/editar/<int:id>")
def editar_filme(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""SELECT id, titulo, genero, duracao_min,
                   data_lancamento FROM filme WHERE id = %s""", (id,))
    filme = cursor.fetchone()
    banco.close()

    if filme is None:
        return redirect("/filmes")

    return render_template("editar_filme.html", filme=filme)

@app.route("/filmes/atualizar/<int:id>", methods=["POST"])
def atualizar_filme(id):
    titulo = request.form.get("titulo")
    genero = request.form.get("genero")
    duracao_min = request.form.get("duracao_min")
    data_lancamento = request.form.get("data_lancamento")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE filme SET titulo = %s, genero = %s,
                   duracao_min = %s, data_lancamento = %s
                   WHERE id = %s""",
                   (titulo, genero, duracao_min, data_lancamento, id))
    banco.commit()
    banco.close()
    return redirect("/filmes")

@app.route("/filmes/excluir/<int:id>", methods=["POST"])
def excluir_filme(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM filme WHERE id = %s", (id,))
    banco.commit()
    banco.close()
    return redirect("/filmes")

# Tabela 2 - Salas (Pedro Henrique Pontin da Silva Belduscho (26))
@app.route('/salas')
def salas():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""SELECT id, nome, tipo, capacidade,
                      preco_ingresso FROM sala ORDER BY id""")
    lista = cursor.fetchall()
    banco.close()
    return render_template("salas.html", salas=lista)

@app.route("/salas/enviar", methods=["POST"])
def enviar_sala():
    nome = request.form.get("nome")
    tipo = request.form.get("tipo")
    capacidade = request.form.get("capacidade")
    preco_ingresso = request.form.get("preco_ingresso")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO sala
                   (nome, tipo, capacidade, preco_ingresso)
                   VALUES (%s, %s, %s, %s)""",
                   (nome, tipo, capacidade, preco_ingresso))
    banco.commit()
    banco.close()
    return redirect("/salas")

@app.route("/salas/editar/<int:id>")
def editar_sala(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""SELECT id, nome, tipo, capacidade,
                   preco_ingresso FROM sala WHERE id = %s""", (id,))
    sala = cursor.fetchone()
    banco.close()

    if sala is None:
        return redirect("/salas")

    return render_template("editar_sala.html", sala=sala)

@app.route("/salas/atualizar/<int:id>", methods=["POST"])
def atualizar_sala(id):
    nome = request.form.get("nome")
    tipo = request.form.get("tipo")
    capacidade = request.form.get("capacidade")
    preco_ingresso = request.form.get("preco_ingresso")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE sala SET nome = %s, tipo = %s,
                   capacidade = %s, preco_ingresso = %s
                   WHERE id = %s""",
                   (nome, tipo, capacidade, preco_ingresso, id))
    banco.commit()
    banco.close()
    return redirect("/salas")

@app.route("/salas/excluir/<int:id>", methods=["POST"])
def excluir_sala(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM sala WHERE id = %s", (id,))
    banco.commit()
    banco.close()
    return redirect("/salas")

if __name__ == '__main__':
    app.run()
