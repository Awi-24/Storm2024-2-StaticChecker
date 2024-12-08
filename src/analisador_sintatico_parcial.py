import os

class AnalisadorSintaticoParcial:
    def __init__(self, tokens):
        self.tokens = tokens  #* tokens gerados pelo analisador lexico

    def gerar_relatorio_lex(self, nome_arquivo, equipe, integrantes):
        # Gera o relatório .lex com o índice da tabela de símbolos
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
        # Gera o relatório .tab com a tabela de símbolos ignorando espaços e quebras de linha
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


#! essa classe deve analisar a saida de tokens, ignorar espacos em branco e verificar erros sintaticos
#todo ela nao ta analisando corretamente

class AnalisadorSintatico:
    def __init__(self, tokens, nome_arquivo="relatorio_erros.txt"):
        self.tokens = tokens
        self.posicao = 0
        self.nome_arquivo = nome_arquivo  
        self.erros = [] 

    def verificar_token(self, tipo_token):
        #! verifica se o proximo token e do tipo esperado, ignorando espacos e quebras de linha
        while self.posicao < len(self.tokens) and self.tokens[self.posicao]['TipoSimb'] == "ESPACO":
            self.posicao += 1  # ignora espacos em branco
        if self.posicao < len(self.tokens) and self.tokens[self.posicao]['TipoSimb'] == tipo_token:
            print(f"Token esperado: {tipo_token}, Token encontrado: {self.tokens[self.posicao]}")  #! debug
            self.posicao += 1
            return True
        print(f"Token esperado: {tipo_token}, Token NAO encontrado: {self.tokens[self.posicao]}")  #! debug
        return False

    def erro(self, mensagem):
        #! exibe erro quando a analise sintatica falha e registra no relatorio
        erro_msg = f"Erro na linha {self.tokens[self.posicao]['Linhas'][0] if self.posicao < len(self.tokens) else 'desconhecida'}: {mensagem}"
        print(erro_msg) 
        self.erros.append(erro_msg)  

        #! escreve no arquivo de log
        self.salvar_relatorio()

        exit(1)  

    def salvar_relatorio(self):
        #! salva o relatorio de erros em um arquivo
        with open(self.nome_arquivo, "w", encoding="utf-8") as arquivo:
            for erro in self.erros:
                arquivo.write(erro + "\n")

    def programa(self):
        #! funcao principal para verificar a estrutura de um programa
        print("Iniciando análise do programa...")  #! debug
        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "PROGRAMA":
            self.erro("Esperado 'programa'")
        if not self.verificar_token("IDENTIFICADOR"):
            self.erro("Esperado nome do programa")
        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "DECLARACOES":
            self.erro("Esperado 'declaracoes'")

        self.declaracoes()

        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "FIMDECLARACOES":
            self.erro("Esperado 'fimDeclaracoes'")

        self.funcoes()

        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "FIMPROGRAMA":
            self.erro("Esperado 'fimPrograma'")

    def declaracoes(self):
        #! verifica as declaracoes de variaveis e tipos
        print("Iniciando análise das declarações...")  #! debug
        while True:
            print(f"Analisando token: {self.tokens[self.posicao]}")  #! debug

            #! verifica se encontramos um tipo de variavel
            if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "TIPOVAR":
                print(f"Token tipo de variável encontrado: {self.tokens[self.posicao-1]}")  #! debug
                #! verifica o tipo da variavel
                if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] not in ["INTEIRO", "REAL", "CADEIA", "LOGICO", "CARACTER", "VAZIO"]:
                    self.erro("Esperado tipo de variável válido")
                
                #! verifica o caractere ':' apos o tipo de variavel
                if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ":":
                    self.erro("Esperado ':' apos tipo de variavel")
                
                #! verifica os identificadores
                if not self.verificar_token("IDENTIFICADOR"):
                    self.erro("Esperado identificador para variavel")
                
                #! verificar se ha multiplos identificadores separados por virgula
                while self.verificar_token("DELIMITADOR") and self.tokens[self.posicao-1]['Lexeme'] == ",":
                    if not self.verificar_token("IDENTIFICADOR"):
                        self.erro("Esperado identificador para variavel")
                
                #! a declaracao de variaveis deve terminar com ponto e virgula
                if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ";":
                    self.erro("Esperado ';' apos declaracoes")
            
            #! se nao for um tipo de variavel, significa que chegamos ao fim das declaracoes
            elif self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "FIMDECLARACOES":
                print("Fim das declarações encontrado.")  #! debug
                break
            else:
                self.erro("Esperado 'TIPOVAR' ou 'fimDeclaracoes'")

    def funcoes(self):
        #! verifica a estrutura das funcoes
        print("Iniciando análise das funções...")  #! debug
        while self.posicao < len(self.tokens):
            if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "FUNCOES":
                while True:
                    if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] == "FIMFUNCOES":
                        return

                    if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] != "FUNCAO":
                        self.erro("Esperado 'funcao'")

                    self.tipo_funcao()
                    self.nome_funcao()
                    self.parametros()

    def tipo_funcao(self):
        #! verifica o tipo da funcao
        if not self.verificar_token("PALAVRA_CHAVE") or self.tokens[self.posicao-1]['Lexeme'] not in ["REAL", "INTEIRO", "CADEIA", "LOGICO", "CARACTER", "VAZIO"]:
            self.erro("Esperado tipo de funcao")

    def nome_funcao(self):
        #! verifica o nome da funcao
        if not self.verificar_token("IDENTIFICADOR"):
            self.erro("Esperado nome da funcao")

    def parametros(self):
        #! verifica os parametros da funcao
        if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != "(":
            self.erro("Esperado '(' para inicio dos parametros")
        
        while True:
            if self.verificar_token("PALAVRA_CHAVE") and self.tokens[self.posicao-1]['Lexeme'] in ["REAL", "INTEIRO", "CADEIA", "LOGICO", "CARACTER", "VAZIO"]:
                if not self.verificar_token("IDENTIFICADOR"):
                    self.erro("Esperado identificador para parametro")
            
            if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ",":
                break

        if not self.verificar_token("DELIMITADOR") or self.tokens[self.posicao-1]['Lexeme'] != ")":
            self.erro("Esperado ')' para fechamento dos parametros")
