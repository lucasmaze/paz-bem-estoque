# paz-bem-estoque
Sistema web de controle de estoque de medicamentos — Projeto de Software.


## Funcionalidades implementadas

- Cadastro de medicamentos com nome, quantidade e validade.
- Consulta dos medicamentos cadastrados no estoque.
- Atualização da quantidade de medicamentos.

## Testes realizados

Os testes foram realizados no navegador durante o desenvolvimento.

- Cadastro com quantidade negativa: aprovado.
- Cadastro sem nome: aprovado.
- Cadastro sem data de validade: aprovado.
- Atualização com quantidade negativa: aprovado.
- Atualização com quantidade vazia: aprovado.
- Atualização com quantidade zero: aprovado.

Os testes confirmaram o funcionamento das validações dos formulários no navegador e a atualização da quantidade no estoque.

## Avisos de validade dos medicamentos

Foi implementada a funcionalidade de aviso de validade (RF04), que identifica automaticamente a situação dos medicamentos cadastrados.

O sistema apresenta três situações:
- Vencido: quando a data de validade já passou.
- Próximo do vencimento: quando faltam até 30 dias para a validade.
- Dentro da validade: quando faltam mais de 30 dias para a validade.

## Testes realizados

Os testes foram realizados no navegador, utilizando medicamentos fictícios.

- Medicamento com validade em 01/11/2026: aprovado. O sistema apresentou "Vencido".
- Medicamento com validade em 25/11/2026: aprovado. O sistema apresentou "Próximo do vencimento".
- Medicamento com validade em 31/12/2027: aprovado. O sistema apresentou "Dentro da validade".

Os três testes apresentaram os resultados esperados.