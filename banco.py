import sqlite3

# Nome do arquivo que armazenará os dados do sistema.
NOME_BANCO = "estoque.db"


# Cria as tabelas necessárias para o controle de estoque.
def criar_banco():
    # Abre a conexão com o banco de dados.
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    # Cria a tabela de medicamentos.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Medicamento (
            id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    # Cria a tabela de estoque e relaciona cada
    # registro a um medicamento cadastrado.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Estoque (
            id_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
            id_medicamento INTEGER NOT NULL,
            quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
            data_validade DATE NOT NULL,
            FOREIGN KEY (id_medicamento)
                REFERENCES Medicamento(id_medicamento)
        )
    """)

    # Salva as alterações e encerra a conexão.
    conexao.commit()
    conexao.close()


# Executa a criação das tabelas quando este arquivo
# for iniciado diretamente pelo Python.
if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")