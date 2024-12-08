# Static Checker - storm2024.2

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


1. Pré-requisitos
Python 3.8 ou superior instalado.
Familiaridade com o padrão de texto fonte .242 especificado para Storm2024-2.
2. Estrutura de Entrada
O código aceita um arquivo fonte com extensão .242, contendo o programa em Storm2024-2. O texto deve seguir as regras da linguagem especificadas, incluindo uso de identificadores, palavras-chave, delimitadores, e operadores válidos.

3. Execução
Configurar o arquivo fonte:

Escreva o código em Storm2024-2 e salve-o com a extensão .242.
Criar uma instância do Analisador Léxico:

python
Copiar código
from analisador import AnalisadorLexico, AnalisadorSintatico

# Ler o código fonte
with open("exemplo.242", "r", encoding="utf-8") as arquivo:
    codigo = arquivo.read()

analisador_lexico = AnalisadorLexico(codigo)
tokens, tabela_simbolos = analisador_lexico.analisar()
Criar uma instância do Analisador Sintático:

Após a análise léxica, passe os tokens para o analisador sintático para gerar os relatórios:
python
Copiar código
analisador_sintatico = AnalisadorSintatico(tokens)

# Gerar os relatórios
equipe = "EQUIPE01"
integrantes = ["Aluno 1 - email1@exemplo.com", "Aluno 2 - email2@exemplo.com"]
analisador_sintatico.gerar_relatorio_lex("exemplo.242", equipe, integrantes)
analisador_sintatico.gerar_relatorio_tab("exemplo.242", equipe, integrantes)
Verificar os relatórios gerados:

Após a execução, serão criados dois arquivos na mesma pasta do programa:
exemplo.LEX: Contém os tokens identificados e informações relacionadas.
exemplo.TAB: Contém detalhes da tabela de símbolos.

Formato dos Relatórios
Relatório .LEX
Exemplo de saída:

yaml
Copiar código
Código da Equipe: EQUIPE01
Componentes:
  Aluno 1 - email1@exemplo.com
  Aluno 2 - email2@exemplo.com

RELATÓRIO DA ANÁLISE LEXICA:
Lexeme: PROGRAMA, Código: 101, Índice da Tabela de Símbolos: N/A, Linha: [1]
Lexeme: X, Código: 103, Índice da Tabela de Símbolos: 1, Linha: [2]
...
Relatório .TAB
Exemplo de saída:

yaml
Copiar código
Código da Equipe: EQUIPE01
Componentes:
  Aluno 1 - email1@exemplo.com
  Aluno 2 - email2@exemplo.com

RELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: exemplo.242
Entrada: 1, Código: 103, Lexeme: X,
QtdCharAntesTrunc: 1, QtdCharDepoisTrunc: 1,
TipoSimb: IDENTIFICADOR, Linhas: (2, 3, 5).
...
Pontos de Atenção
Certifique-se de que o arquivo fonte segue as especificações da linguagem Storm2024-2.
Palavras-chave e identificadores devem ser distinguíveis por suas regras léxicas.
Identificadores com mais de 30 caracteres serão truncados, mas seu funcionamento seguirá as especificações.


## Licença

Este projeto não tem licença.
