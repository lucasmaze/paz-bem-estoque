# Importa as ferramentas necessárias para criar o sistema web.
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date, timedelta

# Importa a função que prepara o banco de dados.
from banco import criar_banco

# Cria a aplicação principal.
app = Flask(__name__)


# Define a página inicial do sistema.
@app.route("/")
def inicio():
    return "Sistema de Estoque - PAZ & BEM MEDICAMENTOS"


# Exibe o formulário e recebe os dados do medicamento.
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    # Quando o formulário é enviado, recebe os dados preenchidos.
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        quantidade_texto = request.form.get("quantidade", "")
        validade = request.form.get("validade", "")

        # Verifica se os campos possuem valores válidos.
        try:
            quantidade = int(quantidade_texto)
        except ValueError:
            return "Quantidade inválida.", 400

        if not nome or len(nome) > 150 or quantidade < 0 or not validade:
            return "Dados inválidos. Confira o formulário.", 400

        # Verifica se a data de validade é válida.
        from datetime import date

        try:
            date.fromisoformat(validade)
        except ValueError:
            return "Data de validade inválida.", 400

        # Abre uma conexão com o banco de dados.
        conexao = sqlite3.connect("estoque.db")
        conexao.execute("PRAGMA foreign_keys = ON")

        try:
            cursor = conexao.cursor()

            # Cadastra o nome do medicamento.
            cursor.execute(
                "INSERT INTO Medicamento (nome) VALUES (?)",
                (nome,)
            )

            # Obtém o identificador do medicamento cadastrado.
            id_medicamento = cursor.lastrowid

            # Registra a quantidade e a validade no estoque.
            cursor.execute(
                """
                INSERT INTO Estoque
                (id_medicamento, quantidade, data_validade)
                VALUES (?, ?, ?)
                """,
                (id_medicamento, quantidade, validade)
            )

            # Salva os dois registros no banco de dados.
            conexao.commit()

        except sqlite3.Error:
            conexao.rollback()
            return "Não foi possível salvar o medicamento.", 500

        finally:
            conexao.close()

        # Após cadastrar, retorna automaticamente à consulta de estoque.
        return redirect(url_for("consultar_estoque"))


    # Exibe a tela quando o usuário acessa a página.
    return render_template("cadastro.html")

# Exibe os medicamentos cadastrados no estoque.
@app.route("/estoque")
def consultar_estoque():
    # Abre a conexão com o banco de dados.
    conexao = sqlite3.connect("estoque.db")
    conexao.row_factory = sqlite3.Row

    # Consulta os medicamentos e suas informações de estoque.
    medicamentos = conexao.execute("""
    SELECT Estoque.id_estoque,
           Medicamento.nome,
           Estoque.quantidade,
           Estoque.data_validade
        FROM Medicamento
        JOIN Estoque
          ON Medicamento.id_medicamento = Estoque.id_medicamento
        ORDER BY Medicamento.nome
    """).fetchall()

    # Encerra a conexão.
    conexao.close()

     # Define a data atual e o limite de 30 dias.
    hoje = date.today()
    limite_validade = hoje + timedelta(days=30)

     # Verifica a validade de cada medicamento.
    avisos = []

    for medicamento in medicamentos:
        validade = date.fromisoformat(medicamento["data_validade"])

        if validade < hoje:
            avisos.append("Vencido")
        elif validade <= limite_validade:
            avisos.append("Próximo do vencimento")
        else:
            avisos.append("Dentro da validade")

    # Exibe os resultados na página HTML.
    return render_template(
        "estoque.html",
        medicamentos=medicamentos,
        avisos=avisos)

# Permite consultar e atualizar a quantidade de um medicamento.
@app.route("/atualizar/<int:id_estoque>", methods=["GET", "POST"])
def atualizar_estoque(id_estoque):
    conexao = sqlite3.connect("estoque.db")
    conexao.row_factory = sqlite3.Row

    medicamento = conexao.execute("""
        SELECT Estoque.id_estoque, Medicamento.nome, Estoque.quantidade
        FROM Estoque
        JOIN Medicamento
        ON Medicamento.id_medicamento = Estoque.id_medicamento
        WHERE Estoque.id_estoque = ?
    """, (id_estoque,)).fetchone()

    if medicamento is None:
        conexao.close()
        return "Medicamento não encontrado.", 404

    if request.method == "POST":
        try:
            quantidade = int(request.form.get("quantidade", ""))
        except ValueError:
            conexao.close()
            return "Quantidade inválida.", 400

        if quantidade < 0:
            conexao.close()
            return "A quantidade não pode ser negativa.", 400

        conexao.execute(
            "UPDATE Estoque SET quantidade = ? WHERE id_estoque = ?",
            (quantidade, id_estoque)
        )
        conexao.commit()
        conexao.close()

        return redirect(url_for("consultar_estoque"))

    conexao.close()
    return render_template("atualizar.html", medicamento=medicamento)


# Inicia o sistema para testes durante o desenvolvimento.
if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
