import os

class AnalisadorSintaticoParcial:
    def __init__(self, tokens):
        self.tokens = tokens  #* tokens gerados pelo analisador lexico

    def gerar_relatorio_lex(self, nome_arquivo, equipe, integrantes):
        # Gera o relatório .LEX com o índice da tabela de símbolos
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
        caminho_arquivo = os.path.join(diretorio_atual, nome_arquivo)  # Garante que o arquivo será salvo no diretório correto

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Código da Equipe: {equipe}\n")
            arquivo.write("Componentes:\n")
            for integrante in integrantes:
                arquivo.write(f"  {integrante}\n")
            arquivo.write("\nRELATÓRIO DA ANÁLISE LEXICA:\n")
            
            for token in self.tokens:
                arquivo.write(f"Lexeme: {token['Lexeme']}, Código: {token['Código']}, "
                            f"Índice da Tabela de Símbolos: {token['Entrada'] if token['Entrada'] is not None else 'N/A'}, "
                            f"Linha: {token['Linhas']}\n")
                arquivo.write("---------------------------------------------------------------------------------------\n")
                    
        print(f"Relatório .LEX gerado em {caminho_arquivo}")

    def gerar_relatorio_tab(self, nome_arquivo, equipe, integrantes):
        # Gera o relatório .TAB com a tabela de símbolos ignorando espaços e quebras de linha
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
        caminho_arquivo_tab = os.path.join(diretorio_atual, os.path.splitext(nome_arquivo)[0] + ".TAB")  # Garante que o arquivo será salvo no diretório correto

        with open(caminho_arquivo_tab, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Código da Equipe: {equipe}\n")
            arquivo.write("Componentes:\n")
            for integrante in integrantes:
                arquivo.write(f"  {integrante}\n")
            arquivo.write(f"\nRELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {os.path.basename(nome_arquivo)}\n")

            tabela_simbolos = {}
            for token in self.tokens:
                if token["TipoSimb"] in ["ESPACO", "QUEBRA_DE_LINHA"]:
                    continue

                lexeme = token["Lexeme"]
                if lexeme not in tabela_simbolos:
                    tabela_simbolos[lexeme] = {
                        "Entrada": token["Entrada"],
                        "Código": token["Código"],
                        "Lexeme": lexeme,
                        "QtdCharAntesTrunc": token["QtdCharAntesTrunc"],
                        "QtdCharDepoisTrunc": token["QtdCharDepoisTrunc"],
                        "TipoSimb": token["TipoSimb"],
                        "Linhas": set(),
                    }
                tabela_simbolos[lexeme]["Linhas"].update(token["Linhas"])

            for simbolo in tabela_simbolos.values():
                linhas = ", ".join(map(str, sorted(simbolo["Linhas"])))
                arquivo.write(f"Entrada: {simbolo['Entrada']}, Código: {simbolo['Código']}, Lexeme: {simbolo['Lexeme']}, \n"
                            f"QtdCharAntesTrunc: {simbolo['QtdCharAntesTrunc']}, QtdCharDepoisTrunc: {simbolo['QtdCharDepoisTrunc']}, \n"
                            f"TipoSimb: {simbolo['TipoSimb']}, Linhas: ({linhas}).\n")
                arquivo.write("-------------------------------------------------------------------\n")

        print(f"Relatório .TAB gerado em {caminho_arquivo_tab}")


#! ESSA CLASSE DEVE ANALISAR A SAIDA DE TOKENS, IGNORAR ESPAÇOS EM BRANCO E VERIFICAR ERROS SINTATICOS.
#todo ELA NAO TA ANALISANDO CORRETAMENTE.

class AnalisadorSintatico:
    def __init__(self, tokens, nome_arquivo="relatorio_erros.txt"):
        self.tokens = tokens
        self.posicao = 0
        self.nome_arquivo = nome_arquivo  
        self.erros = [] 

    def verificar_token(self, tipo_token):
        """Verifica se o próximo token é do tipo esperado, ignorando espaços e quebras de linha."""
        while self.posicao < len(self.tokens) and self.tokens[self.posicao]['TipoSimb'] == "ESPACO":
            self.posicao += 1  # Ignora espaços em branco
        if self.posicao < len(self.tokens) and self.tokens[self.posicao]['TipoSimb'] == tipo_token:
            print(f"Token esperado: {tipo_token}, Token encontrado: {self.tokens[self.posicao]}")  #! debug
            self.posicao += 1
            return True
        print(f"Token esperado: {tipo_token}, Token NÃO encontrado: {self.tokens[self.posicao]}")  #! debug
        return False

    def erro(self, mensagem):
        """Exibe erro quando a análise sintática falha e registra no relatório."""
        erro_msg = f"Erro na linha {self.tokens[self.posicao]['Linhas'][0] if self.posicao < len(self.tokens) else 'desconhecida'}: {mensagem}"
        print(erro_msg) 
        self.erros.append(erro_msg)  

        #! escreve no arquivo de log
        self.salvar_relatorio()

        exit(1)  

    def salvar_relatorio(self):
        """Salva o relatório de erros em um arquivo."""
        with open(self.nome_arquivo, "w", encoding="utf-8") as arquivo:
            for erro in self.erros:
                arquivo.write(erro + "\n")

    def programa(self):
        """Função principal para verificar a estrutura de um programa."""
        print("Iniciando análise do programa...")  # Debug
        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "PROGRAMA":
            self.erro("Esperado 'programa'")
        if not self.verificar_token("IDENTIFICADOR"):
            self.erro("Esperado nome do programa")
        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "DECLARACOES":
            self.erro("Esperado 'declarações'")

        self.declaracoes()

        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "FIMDECLARACOES":
            self.erro("Esperado 'fimDeclaracoes'")

        self.funcoes()

        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "FIMPROGRAMA":
            self.erro("Esperado 'fimPrograma'")

    def declaracoes(self):
        """Verifica as declarações de variáveis e tipos."""
        print("Iniciando análise das declarações...")  # Debug
        while True:
            print(f"Analisando token: {self.tokens[self.posicao]}")  # Debug

            # Verifica se encontramos um tipo de variável
            if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "TIPOVAR":
                print(f"Token tipo de variável encontrado: {self.tokens[self.posicao-1]}")  # Debug
                # Verifica o tipo da variável
                if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] not in ["INTEIRO", "REAL", "CADEIA", "LOGICO", "CARACTER", "VAZIO"]:
                    self.erro("Esperado tipo de variável válido")
                
                # Verifica o caractere ':' após o tipo de variável
                if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ":":
                    self.erro("Esperado ':' após tipo de variável")
                
                # Verifica os identificadores
                if not self.verificar_token("IDENTIFICADOR"):
                    self.erro("Esperado identificador para variável")
                
                # Agora vamos verificar se há múltiplos identificadores separados por vírgula
                while self.verificar_token("DELIMITADOR") and self.tokens[self.posicao-1]['Lexeme'] == ",":
                    if not self.verificar_token("IDENTIFICADOR"):
                        self.erro("Esperado identificador para variável")
                
                # A declaração de variáveis deve terminar com ponto e vírgula
                if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ";":
                    self.erro("Esperado ';' após declarações")
            
            # Se não for um tipo de variável, significa que chegamos ao fim das declarações
            elif self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "FIMDECLARACOES":
                print("Fim das declarações encontrado.")  # Debug
                break
            else:
                self.erro("Esperado 'TIPOVAR' ou 'fimDeclaracoes'")

    def funcoes(self):
        """Verifica a estrutura das funções."""
        print("Iniciando análise das funções...")  #!debug
        while self.posicao < len(self.tokens):
            if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "FUNCOES":
                while True:
                    if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "FIMFUNCOES":
                        return

                    if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "FUNCAO":
                        self.erro("Esperado 'função'")

                    self.tipo_funcao()
                    self.nome_funcao()
                    self.parametros()

    def tipo_funcao(self):
        """Verifica o tipo da função."""
        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] not in ["REAL", "INTEIRO", "CADEIA", "LOGICO", "CARACTER", "VAZIO"]:
            self.erro("Esperado tipo de função")

    def nome_funcao(self):
        """Verifica o nome da função."""
        if not self.verificar_token("IDENTIFICADOR"):
            self.erro("Esperado nome da função")

    def parametros(self):
        """Verifica os parâmetros da função."""
        if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != "(":
            self.erro("Esperado '(' para início dos parâmetros")
        
        while True:
            if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] in ["REAL", "INTEIRO", "CADEIA", "LOGICO", "CARACTER", "VAZIO"]:
                if not self.verificar_token("IDENTIFICADOR"):
                    self.erro("Esperado identificador para parâmetro")
            
            if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ",":
                break

        if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ")":
            self.erro("Esperado ')' para fechamento dos parâmetros")
