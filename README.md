# Static Checker - styorm2024.2

## Visão Geral

Este projeto é um **Static Checker** para a linguagem de programação **storm2024.2**, que é baseada em C. O objetivo do projeto é realizar a verificação estática de código-fonte, onde o código é analisado sem ser executado para identificar possíveis erros e inconsistências. Este é um projeto final da matéria de **Compiladores** do curso de **Engenharia da Computação** do CIMATEC.

O **Static Checker** consiste em três partes principais:

1. **Analisador Léxico:** Responsável por analisar o código-fonte e dividir o texto em tokens, que são os menores elementos significativos da linguagem (como palavras-chave, identificadores, operadores, etc.).
2. **Analisador Semântico:** Realiza a verificação semântica do código, garantindo que ele siga as regras de tipo, escopo e outras validações lógicas. 
3. **Geração de Relatórios:** Gera relatórios indicando erros encontrados no código-fonte, como declarações inválidas, tipos de dados incompatíveis, e outras inconsistências lógicas.

## Funcionalidades

- **Análise Léxica:** Identificação e categorização de tokens, como:
  - **PALAVRAS-CHAVE** (ex: `programa`, `fimPrograma`, `inteiro`, `real`, etc.)
  - **IDENTIFICADORES** (ex: variáveis e funções)
  - **OPERADORES** (aritméticos, lógicos, etc.)
  - **DELIMITADORES** (parênteses, ponto e vírgula, etc.)
- **Análise Semântica:** Verificação de erros como:
  - Variáveis não declaradas
  - Tipos incompatíveis (ex: soma de variáveis com tipos diferentes)
  - Escopo de variáveis e funções
- **Relatório de Erros:** Geração de mensagens de erro e avisos sobre problemas encontrados no código, como variáveis não definidas, tipos de dados incompatíveis e problemas de escopo.

## Como Funciona

1. **Analisador Léxico:**
   - O código-fonte é dividido em tokens com base em expressões regulares.
   - Cada token é classificado em um dos seguintes tipos:
     - **PALAVRA_CHAVE:** Palavras reservadas da linguagem, como `programa`, `se`, `fimFunc`, etc.
     - **IDENTIFICADOR:** Variáveis, funções e outros identificadores definidos pelo usuário.
     - **OPERADOR_ARITMETICO:** Operadores aritméticos como `+`, `-`, `*`, etc.
     - **DELIMITADOR:** Símbolos de pontuação como `;`, `:`, `,`, etc.
     - **NUMERO:** Literais numéricos.
     - **DESCONHECIDO:** Caracteres ou sequências que não pertencem à linguagem.

2. **Analisador Semântico:**
   - Após a análise léxica, o código é analisado para garantir que as variáveis estão corretamente declaradas e que os tipos de dados são usados corretamente.
   - Verifica a existência de variáveis antes de usá-las, a correspondência de tipos em expressões, e o escopo correto das variáveis e funções.

3. **Relatório .LEX e .TAB:**
   - [mexer nisso aqui depois]


## Requisitos

- Python 3.x
- Bibliotecas:
  - `re` (para expressões regulares)
  - `os` (para manipulação de arquivos)


## Licença

Este projeto não tem licença.
