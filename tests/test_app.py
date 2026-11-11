
# Testes automatizados do sistema PAZ & BEM MEDICAMENTOS.

import sqlite3

from app import app


# Teste 1: verifica a página inicial.
def test_pagina_inicial():
    cliente = app.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"Sistema de Estoque" in resposta.data


# Teste 2: verifica a integração do Flask com o SQLite.
def test_consulta_estoque(tmp_path, monkeypatch):

    # Utiliza um banco temporário, sem alterar o estoque real.
    monkeypatch.chdir(tmp_path)

    conexao = sqlite3.connect("estoque.db")

    # Cria as tabelas necessárias para o teste.
    conexao.execute(
        "CREATE TABLE Medicamento "
        "(id_medicamento INTEGER PRIMARY KEY, nome TEXT)"
    )

    conexao.execute(
        "CREATE TABLE Estoque "
        "(id_estoque INTEGER PRIMARY KEY, "
        "id_medicamento INTEGER, quantidade INTEGER, "
        "data_validade TEXT)"
    )

    # Cadastra um medicamento fictício.
    conexao.execute(
        "INSERT INTO Medicamento VALUES (1, 'Dipirona')"
    )

    conexao.execute(
        """
        INSERT INTO Estoque
        (id_medicamento, quantidade, data_validade)
        VALUES (?, ?, ?)
        """,
        (1, 10, "2027-12-30")
    )

    conexao.commit()
    conexao.close()

    # Consulta o estoque por meio do Flask.
    cliente = app.test_client()
    resposta = cliente.get("/estoque")

    # Verifica se a consulta funcionou.
    assert resposta.status_code == 200
    assert b"Dipirona" in resposta.data
