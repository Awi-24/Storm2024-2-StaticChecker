import os

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens gerados pelo léxico
        self.token_atual = None
        self.posicao = 0
        self.erros_sintaticos = []
        self.avancar()

    # Para garantir que espaços sejam ignorados durante a análise léxica
    def avancar(self):
        """Avança para o próximo token, ignorando espaços e quebras de linha."""
        while self.posicao < len(self.tokens) and 'TipoSimb' in self.tokens[self.posicao] and self.tokens[self.posicao]['TipoSimb'] == "ESPACO":
            self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]
            self.posicao += 1
        else:
            self.token_atual = None

    def esperar(self, tipo_esperado):
        """Verifica se o token atual corresponde ao tipo esperado."""
        if self.token_atual and self.token_atual['TipoSimb'] == tipo_esperado:
            self.avancar()
        else:
            erro_msg = f"Esperado: {tipo_esperado}, encontrado: {self.token_atual['Lexeme'] if self.token_atual else 'Nenhum token'}"
            self.erros_sintaticos.append(erro_msg)
            print(f"Erro sintático: {erro_msg}")

    def analisar_programa(self):
        """Inicia a análise sintática do programa."""
        self.esperar("PROGRAMA")  # Verifique o tipo do token atual
        self.esperar("IDENTIFICADOR")
        self.esperar("DECLARACOES")
        self.analisar_declaracoes()
        self.esperar("FIMDECLARACOES")
        self.esperar("FUNCOES")
        self.analisar_funcoes()
        self.esperar("FIMFUNCOES")
        self.esperar("FIMPROGRAMA")

    def analisar_declaracoes(self):
        """Analisa as declarações de variáveis."""
        while self.token_atual and self.token_atual["TipoSimb"] == "TIPOVAR":
            self.esperar("TIPOVAR")
            self.analisar_tipo()
            self.esperar(":")
            self.analisar_variaveis()
            self.esperar(";")

    def analisar_tipo(self):
        """Verifica o tipo de dado."""
        tipos_validos = ["REAL", "INTEIRO", "CADEIA", "LOGICO", "CARACTER", "VAZIO"]
        if self.token_atual and self.token_atual["Lexeme"] in tipos_validos:
            self.avancar()
        else:
            erro_msg = f"Tipo inválido: {self.token_atual['Lexeme'] if self.token_atual else 'Nenhum token'}"
            self.erros_sintaticos.append(erro_msg)
            print(f"Erro sintático: {erro_msg}")

    def analisar_variaveis(self):
        """Analisa a lista de variáveis."""
        self.esperar("IDENTIFICADOR")
        while self.token_atual and self.token_atual["Lexeme"] == ",":
            self.avancar()
            self.esperar("IDENTIFICADOR")

    def analisar_funcoes(self):
        """Analisa a definição de funções."""
        while self.token_atual and self.token_atual["TipoSimb"] == "TIPOFUNC":
            self.esperar("TIPOFUNC")
            self.analisar_tipo()
            self.esperar(":")
            self.esperar("IDENTIFICADOR")
            self.esperar("(")
            if self.token_atual and self.token_atual["TipoSimb"] != "DELIMITADOR":  # Parâmetros opcionais
                self.analisar_parametros()
            self.esperar(")")
            self.analisar_comando()
            self.esperar("FIMFUNC")

    def analisar_parametros(self):
        """Analisa os parâmetros de uma função."""
        self.analisar_tipo()
        self.esperar(":")
        self.esperar("IDENTIFICADOR")
        while self.token_atual and self.token_atual["Lexeme"] == ",":
            self.avancar()
            self.esperar("IDENTIFICADOR")

    def analisar_comando(self):
        """Analisa os comandos dentro de funções."""
        if self.token_atual["TipoSimb"] == "DELIMITADOR" and self.token_atual["Lexeme"] == "{":
            self.avancar()  # Abre bloco
            while self.token_atual and self.token_atual["Lexeme"] != "}":
                self.analisar_comando()
            self.esperar("DELIMITADOR")
        elif self.token_atual["Lexeme"] == "RETORNA":
            self.avancar()
            if self.token_atual and self.token_atual["TipoSimb"] in ["NUMERO", "IDENTIFICADOR"]:
                self.analisar_exp_aritmetica()
        elif self.token_atual["Lexeme"] == "SE":
            self.avancar()
            self.analisar_exp_logica()  # Expressão condicional
            self.analisar_comando()  # Comando dentro do "SE"
            if self.token_atual and self.token_atual["Lexeme"] == "SENAO":
                self.avancar()
                self.analisar_comando()  # Comando dentro do "SENAO"
        elif self.token_atual["Lexeme"] == "ENQUANTO":
            self.avancar()
            self.analisar_exp_logica()  # Expressão condicional
            self.analisar_comando()  # Comando dentro do "ENQUANTO"

    def analisar_exp_aritmetica(self):
        """Analisa expressões aritméticas."""
        self.analisar_termo()
        while self.token_atual and self.token_atual["Lexeme"] in ["+", "-"]:
            self.avancar()
            self.analisar_termo()

    def analisar_exp_logica(self):
        """Analisa expressões lógicas.""" 
        self.analisar_fator_logico()
        while self.token_atual and self.token_atual["Lexeme"] in ["E", "OU"]:
            self.avancar()
            self.analisar_fator_logico()

    def analisar_termo(self):
        """Analisa termos em expressões."""
        self.analisar_fator()
        while self.token_atual and self.token_atual["Lexeme"] in ["*", "/"]:
            self.avancar()
            self.analisar_fator()

    def analisar_fator(self):
        """Analisa fatores de expressões."""
        if self.token_atual["TipoSimb"] in ["NUMERO", "IDENTIFICADOR"]:
            self.avancar()
        elif self.token_atual["Lexeme"] == "(":
            self.avancar()
            self.analisar_exp_aritmetica()
            self.esperar(")")

    def analisar_fator_logico(self):
        """Analisa fatores lógicos.""" 
        if self.token_atual["Lexeme"] == "TRUE" or self.token_atual["Lexeme"] == "FALSE":
            self.avancar()
        elif self.token_atual["TipoSimb"] == "IDENTIFICADOR":
            self.avancar()
        else:
            erro_msg = f"Fator lógico inválido na expressão: {self.token_atual['Lexeme'] if self.token_atual else 'Nenhum token'}"
            self.erros_sintaticos.append(erro_msg)
            print(f"Erro sintático: {erro_msg}")

    def gerar_relatorio_lex(self, nome_arquivo, equipe, integrantes):
        """Gera o relatório .LEX com o índice da tabela de símbolos."""
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Código da Equipe: {equipe}\n")
            arquivo.write("Componentes:\n")
            for integrante in integrantes:
                arquivo.write(f"  {integrante}\n")
            arquivo.write("\nRELATÓRIO DA ANÁLISE LEXICA:\n")
            
            # Processa os tokens e escreve o relatório
            for token in self.tokens:
                arquivo.write(f"Lexeme: {token['Lexeme']}, Código: {token['Código']}, "
                            f"Índice da Tabela de Símbolos: {token['Entrada'] if token['Entrada'] is not None else 'N/A'}, "
                            f"Linha: {token['Linhas']}\n")
                arquivo.write("---------------------------------------------------------------------------------------\n")
                    
        print(f"Relatório .LEX gerado em {nome_arquivo}")
        
    def gerar_relatorio_tab(self, tokens, nome_arquivo, integrantes):
        """Gera o relatório .TAB com a tabela de símbolos, apenas se a análise sintática for válida."""   
        # Verificar se há erros sintáticos
        if self.erros_sintaticos:
            print("Relatório .TAB não gerado devido a erros na análise sintática.")
            print("Erros encontrados:") 
            for erro in self.erros_sintaticos:
                print(f"- {erro}")
            return

        # Se não há erros, gera o relatório
        caminho_arquivo_tab = os.path.splitext(nome_arquivo)[0] + ".TAB"

        with open(caminho_arquivo_tab, "w", encoding="utf-8") as arquivo:
            arquivo.write("Código da Equipe: 99\n")
            arquivo.write("Componentes:\n")
            for integrante in integrantes:
                arquivo.write(f"  {integrante}\n")
            arquivo.write(f"\nRELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {os.path.basename(nome_arquivo)}\n")

            tabela_simbolos = {}
            for token in tokens:
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
                arquivo.write(f"Entrada: {simbolo['Entrada']}, Código: {simbolo['Código']}, Lexeme: {simbolo['Lexeme']}, "
                              f"QtdCharAntesTrunc: {simbolo['QtdCharAntesTrunc']}, QtdCharDepoisTrunc: {simbolo['QtdCharDepoisTrunc']}, "
                              f"TipoSimb: {simbolo['TipoSimb']}, Linhas: ({linhas}).\n")
                arquivo.write("-------------------------------------------------------------------\n")

        print(f"Relatório .TAB gerado em {caminho_arquivo_tab}") 
