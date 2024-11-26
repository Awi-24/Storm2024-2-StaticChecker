class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  #! lista de tokens gerados pelo analisador léxico
        self.token_atual = None
        self.posicao = 0
        self.avancar()

    def avancar(self):
        """Avança para o próximo token."""
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]
            self.posicao += 1
        else:
            self.token_atual = None  #! fim dos tokens

    def esperar(self, tipo_esperado):
        """Verifica se o token atual corresponde ao tipo esperado."""
        if self.token_atual and self.token_atual[1] == tipo_esperado:
            self.avancar()
        else:
            raise SyntaxError(f"Esperado: {tipo_esperado}, encontrado: {
                              self.token_atual}")

    def analisar_programa(self):
        """Regra para FileProgram"""
        self.esperar("programa")
        self.esperar("IDENTIFICADOR")  #! nome do programa
        self.esperar("declarações")
        self.analisar_declaracoes()
        self.esperar("fimDeclaracoes")
        self.esperar("funcoes")
        self.analisar_funcoes()
        self.esperar("fimFuncoes")
        self.esperar("fimPrograma")

    def analisar_declaracoes(self):
        """Regra para declarações"""
        while self.token_atual and self.token_atual[1] == "tipoVar":
            self.esperar("tipoVar")
            self.analisar_tipo()
            self.esperar(":")
            self.analisar_variaveis()
            self.esperar(";")

    def analisar_tipo(self):
        """Regra para tipoVar"""
        tipos_validos = ["real", "inteiro",
                         "cadeia", "logico", "caracter", "vazio"]
        if self.token_atual[0] in tipos_validos:
            self.avancar()
        else:
            raise SyntaxError(f"Tipo inválido: {self.token_atual}")

    def analisar_variaveis(self):
        """Regra para variáveis"""
        self.esperar("IDENTIFICADOR")  #! primeiro identificador
        while self.token_atual and self.token_atual[0] == ",":
            self.avancar()  # Consome a vírgula
            self.esperar("IDENTIFICADOR")

    def analisar_funcoes(self):
        """Regra para funcoes"""
        while self.token_atual and self.token_atual[1] == "tipoFunc":
            self.esperar("tipoFunc")
            self.analisar_tipo()
            self.esperar(":")
            self.esperar("IDENTIFICADOR")  #! nome função
            self.esperar("(")
            if self.token_atual[1] != "DELIMITADOR":  #! parâmetros opcionais
                self.analisar_parametros()
            self.esperar(")")
            self.analisar_comando()
            self.esperar("fimFunc")

    def analisar_parametros(self):
        """Regra para parâmetros"""
        self.analisar_tipo()
        self.esperar(":")
        self.esperar("IDENTIFICADOR")
        while self.token_atual and self.token_atual[0] == ",":
            self.avancar()
            self.esperar("IDENTIFICADOR")

    def analisar_comando(self):
        """Regra para comandos"""
        if self.token_atual[1] == "DELIMITADOR" and self.token_atual[0] == "{":
            self.avancar()  #! abre bloco
            while self.token_atual and self.token_atual[0] != "}":
                self.analisar_comando()
            self.esperar("DELIMITADOR")  #! fecha bloco
        elif self.token_atual[0] == "imprime":
            self.avancar()
            self.analisar_exp_aritmetica()
        elif self.token_atual[0] == "se":
            self.avancar()
            self.esperar("(")
            self.analisar_exp_logica()
            self.esperar(")")
            self.analisar_comando()
            if self.token_atual and self.token_atual[0] == "senao":
                self.avancar()
                self.analisar_comando()
            self.esperar("fimSe")
        elif self.token_atual[0] == "enquanto":
            self.avancar()
            self.esperar("(")
            self.analisar_exp_logica()
            self.esperar(")")
            self.analisar_comando()
            self.esperar("fimEnquanto")
        elif self.token_atual[0] == "retorna":
            self.avancar()
            if self.token_atual and self.token_atual[1] in ["NUMERO", "IDENTIFICADOR"]:
                self.analisar_exp_aritmetica()
        else:
            raise SyntaxError(f"Comando inválido: {self.token_atual}")

    def analisar_exp_aritmetica(self):
        """Regra para expressões aritméticas"""
        self.analisar_termo()
        while self.token_atual and self.token_atual[0] in ["+", "-"]:
            self.avancar()
            self.analisar_termo()

    def analisar_termo(self):
        """Regra para termos de expressões"""
        self.analisar_fator()
        while self.token_atual and self.token_atual[0] in ["*", "/", "%"]:
            self.avancar()
            self.analisar_fator()

    def analisar_fator(self):
        """Regra para fatores de expressões"""
        if self.token_atual[1] in ["NUMERO", "IDENTIFICADOR"]:
            self.avancar()
        elif self.token_atual[0] == "(":
            self.avancar()
            self.analisar_exp_aritmetica()
            self.esperar(")")
        else:
            raise SyntaxError("Fator inválido na expressão")

    def analisar_exp_logica(self):
        """Regra para expressões lógicas"""
        self.analisar_exp_aritmetica()
        while self.token_atual and self.token_atual[0] in ["<=", "<", ">", ">=", "==", "!="]:
            self.avancar()
            self.analisar_exp_aritmetica()
