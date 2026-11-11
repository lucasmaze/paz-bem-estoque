# Importa as ferramentas necessárias para criar o sistema web.
from flask import Flask, render_template, request
import sqlite3

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

        return "Medicamento cadastrado com sucesso!"

    # Exibe a tela quando o usuário acessa a página.
    return render_template("cadastro.html")


# Inicia o sistema para testes durante o desenvolvimento.
if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
