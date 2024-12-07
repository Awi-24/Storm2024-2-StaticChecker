import re

class AnalisadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo.upper()  # Convertendo para maiúsculas para simplificação
        self.tokens = []
        self.posicao = 0
        self.linha_atual = 1
        self.tabela_simbolos = {}

    def remover_comentarios(self):
        """Remove os comentários do código, tanto de uma linha como de várias linhas."""
        codigo_limpo = ""
        i = 0
        while i < len(self.codigo):
            if self.codigo[i:i+2] == "//":  # Comentário de uma linha
                while i < len(self.codigo) and self.codigo[i] != '\n':
                    i += 1
            elif self.codigo[i:i+2] == "/*":  # Comentário de várias linhas
                i += 2
                while i < len(self.codigo) and self.codigo[i:i+2] != "*/":
                    i += 1
                i += 2
            else:
                codigo_limpo += self.codigo[i]
                i += 1
        return codigo_limpo

    def analisar(self):
        tokens_definidos = [
            ("CADEIA", r'"[^"]{0,30}"', 107),
            ("DELIMITADOR", r"[{}();,:,]", 102),
            ("IDENTIFICADOR", r"\b[A-Z_][A-Z0-9_]{0,29}\b", 103),
            ("NUMERO", r"\b\d+(\.\d+)?\b", 104),
            ("OPERADOR_ARITMETICO", r"[\+\-\*/%]", 105),
            ("OPERADOR_LOGICO", r"([<>]=?|==|#)", 106),  # Modificado para pegar todos os operadores lógicos
            ("ESPACO", r"\s+", 108),
            ("DESCONHECIDO", r".", 999),
        ]

        self.codigo = self.remover_comentarios()

        while self.posicao < len(self.codigo):
            match = None
            for tipo_token, regex, codigo in tokens_definidos:
                pattern = re.compile(regex)
                match = pattern.match(self.codigo, self.posicao)
                if match:
                    valor = match.group(0)
                    qtd_char_antes_trunc = len(valor)
                    qtd_char_depois_trunc = min(qtd_char_antes_trunc, 30)

                    if tipo_token == "IDENTIFICADOR":
                        # Armazena o identificador na tabela de símbolos, se não existir
                        indice_tab_simb = self.tabela_simbolos.setdefault(valor, len(self.tabela_simbolos) + 1)
                    else:
                        indice_tab_simb = None

                    # Verifica se o token já foi adicionado
                    token_existente = False
                    for token in self.tokens:
                        if token['Lexeme'] == valor and token['TipoSimb'] == tipo_token:
                            token_existente = True
                            break

                    if not token_existente:
                        # Adiciona o novo token à lista
                        self.tokens.append({
                            "Lexeme": valor,
                            "Código": codigo,
                            "Entrada": indice_tab_simb,
                            "Linhas": [self.linha_atual],
                            "QtdCharAntesTrunc": qtd_char_antes_trunc,
                            "QtdCharDepoisTrunc": qtd_char_depois_trunc,
                            "TipoSimb": tipo_token,
                        })

                    # Atualiza a posição no código e a contagem de linhas
                    self.posicao += len(valor)
                    self.linha_atual += valor.count("\n")
                    break

            if not match:
                # Caso o caractere seja desconhecido
                caractere_invalido = self.codigo[self.posicao]
                if caractere_invalido.isspace():  # Ignora espaços em branco
                    self.posicao += 1
                else:
                    self.tokens.append({
                        "Lexeme": caractere_invalido,
                        "Código": 999,
                        "Entrada": None,
                        "Linhas": [self.linha_atual],
                        "QtdCharAntesTrunc": 1,
                        "QtdCharDepoisTrunc": 1,
                        "TipoSimb": "DESCONHECIDO",
                    })
                    self.posicao += 1
                    
        print(self.tokens)

        # Retorna somente os tokens válidos e a tabela de símbolos
        return self.tokens, self.tabela_simbolos
