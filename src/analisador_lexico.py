import re

# Definindo os tipos de tokens que vamos reconhecer
tokens = [
    ("PALAVRA_CHAVE", r"\b(programa|fimPrograma|fimDeclaracoes|fimFunc|funcoes|imprime|se|senao|enquanto|retorna|vazio|logico|real|inteiro|cadeia|caracter|declaracoes)\b"),
    ("DELIMITADOR", r"[{}();,;:]"),  # Incluindo vírgula e dois-pontos
    ("IDENTIFICADOR", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("NUMERO", r"\b\d+\b"),
    ("OPERADOR_ARITMETICO", r"[\+\-\*/%]"),
    ("OPERADOR_LOGICO", r"[<>!=]=?|==|#"),
    ("ESPACO", r"\s+"),
    ("DESCONHECIDO", r"."),  #! caso não seja reconhecido
]

class AnalisadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []
        self.posicao = 0

    def analisar(self):
        while self.posicao < len(self.codigo):
            match = None
            for tipo_token, regex in tokens:
                pattern = re.compile(regex)
                match = pattern.match(self.codigo, self.posicao)
                if match:
                    valor = match.group(0)
                    if tipo_token != "ESPACO":  # Ignora espaços
                        self.tokens.append((valor, tipo_token))
                    self.posicao += len(valor)
                    break

            if not match:
                #! se nao encontrar nenhum token valido, levanta erro de caractere invalido
                raise SyntaxError(f"Caractere inválido em posição {self.posicao}: {self.codigo[self.posicao]}")
        
        return self.tokens

#! teste do Analisador Léxico
codigo = """
programa exemplo;
declaracoes
    real : x, y;
fimDeclaracoes
funcoes
    inteiro : somar(x, y);
    retorna x + y;
fimFunc
fimPrograma
"""

#! criando o analisador e executando a análise léxica
analisador = AnalisadorLexico(codigo)
tokens = analisador.analisar()

# Exibindo os tokens encontrados
for token in tokens:
    print(token)
