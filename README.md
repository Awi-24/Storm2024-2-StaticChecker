## **README - Analisador Léxico e Sintático para Storm2024-2**

### **Introdução**
Este projeto implementa um *Static Checker* para a linguagem **Storm2024-2**. Ele realiza as etapas de análise léxica e emite relatórios com base nas especificações do documento de projeto fornecido. O código está dividido em duas partes principais: **Analisador Léxico** e **Analisador Sintático**, que trabalham em conjunto para processar um texto fonte escrito na linguagem Storm2024-2.

---

### **Descrição do Funcionamento**

#### **1. Analisador Léxico (`AnalisadorLexico`)**
Responsável por:
- **Remover comentários:** Suporta comentários de linha (`//`) e bloco (`/* */`).
- **Identificar tokens:** Reconhece palavras-chave, delimitadores, identificadores, números, operadores e cadeias, entre outros elementos da linguagem.
- **Armazenar tokens e símbolos:** Gera uma lista de tokens encontrados e mantém uma tabela de símbolos com identificadores únicos.
- **Gerar relatórios:** A lista de tokens pode ser utilizada para gerar o relatório `.LEX`.

**Métodos principais:**
- **`remover_comentarios()`**: Remove comentários de linha e bloco do código.
- **`analisar()`**: Processa o código fonte, identifica tokens usando expressões regulares e armazena os resultados em uma lista e na tabela de símbolos.

#### **2. Analisador Sintático (`AnalisadorSintatico`)**
Responsável por:
- **Gerar relatórios:** Com base nos tokens gerados pelo analisador léxico, cria dois arquivos de saída:
  - `.LEX`: Lista os tokens identificados, junto com seus códigos e índice na tabela de símbolos.
  - `.TAB`: Detalha os identificadores armazenados na tabela de símbolos.

**Métodos principais:**
- **`gerar_relatorio_lex(nome_arquivo, equipe, integrantes)`**: Gera o relatório `.LEX` com informações sobre os tokens.
- **`gerar_relatorio_tab(nome_arquivo, equipe, integrantes)`**: Gera o relatório `.TAB` com informações da tabela de símbolos, como lexeme, tipo, e as linhas em que aparecem.

---

### **Como Usar o Código**

#### **1. Pré-requisitos**
- Python 3.8 ou superior instalado.
- Familiaridade com o padrão de texto fonte `.242` especificado para Storm2024-2.

#### **2. Estrutura de Entrada**
O código aceita um arquivo fonte com extensão `.242`, contendo o programa em **Storm2024-2**. O texto deve seguir as regras da linguagem especificadas, incluindo uso de identificadores, palavras-chave, delimitadores, e operadores válidos.

#### **3. Execução**
1. **Configurar o arquivo fonte:**
   - Escreva o código em Storm2024-2 e salve-o com a extensão `.242`.

2. **Testando o compilador:**
    - Para testar o compilador, basta arrastar o arquivo com extensão `.242` para o executável `main`

3. **Criar uma instância do Analisador Léxico:**
   ```python
   from analisador import AnalisadorLexico, AnalisadorSintatico
   
   # Ler o código fonte
   with open("exemplo.242", "r", encoding="utf-8") as arquivo:
       codigo = arquivo.read()

   analisador_lexico = AnalisadorLexico(codigo)
   tokens, tabela_simbolos = analisador_lexico.analisar()
   ```

4. **Criar uma instância do Analisador Sintático:**
   - Após a análise léxica, passe os tokens para o analisador sintático para gerar os relatórios:
   ```python
   analisador_sintatico = AnalisadorSintatico(tokens)

   # Gerar os relatórios
   equipe = "EQUIPE01"
   integrantes = ["Aluno 1 - email1@exemplo.com", "Aluno 2 - email2@exemplo.com"]
   analisador_sintatico.gerar_relatorio_lex("exemplo.242", equipe, integrantes)
   analisador_sintatico.gerar_relatorio_tab("exemplo.242", equipe, integrantes)
   ```

4. **Verificar os relatórios gerados:**
   - Após a execução, serão criados dois arquivos na mesma pasta do programa:
     - **`exemplo.LEX`**: Contém os tokens identificados e informações relacionadas.
     - **`exemplo.TAB`**: Contém detalhes da tabela de símbolos.

---

### **Formato dos Relatórios**

#### **Relatório `.LEX`**
Exemplo de saída:
```
Código da Equipe: EQUIPE01
Componentes:
  Aluno 1 - email1@exemplo.com
  Aluno 2 - email2@exemplo.com

RELATÓRIO DA ANÁLISE LEXICA:
Lexeme: PROGRAMA, Código: 101, Índice da Tabela de Símbolos: N/A, Linha: [1]
Lexeme: X, Código: 103, Índice da Tabela de Símbolos: 1, Linha: [2]
...
```

#### **Relatório `.TAB`**
Exemplo de saída:
```
Código da Equipe: EQUIPE01
Componentes:
  Aluno 1 - email1@exemplo.com
  Aluno 2 - email2@exemplo.com

RELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: exemplo.242
Entrada: 1, Código: 103, Lexeme: X,
QtdCharAntesTrunc: 1, QtdCharDepoisTrunc: 1,
TipoSimb: IDENTIFICADOR, Linhas: (2, 3, 5).
...
```

---

### **Pontos de Atenção**
- Certifique-se de que o arquivo fonte segue as especificações da linguagem Storm2024-2.
- Palavras-chave e identificadores devem ser distinguíveis por suas regras léxicas.
- Identificadores com mais de 30 caracteres serão truncados, mas seu funcionamento seguirá as especificações.
