# Importa o Flask, utilizado para criar a aplicação web.
from flask import Flask

# Cria a aplicação principal do sistema.
app = Flask(__name__)


# Define a página inicial do sistema.
@app.route("/")
def inicio():
    # Exibe uma mensagem de identificação do projeto.
    return "Sistema de Estoque - PAZ & BEM MEDICAMENTOS"


# Inicia o servidor para testes durante o desenvolvimento.
if __name__ == "__main__":
    app.run(debug=True)
