import re

# Definindo os tipos de tokens que o analisador irá reconhecer
tokens = [
    ("PALAVRA_CHAVE", r"\b(programa|fimPrograma|fimDeclaracoes|fimFunc|funcoes|imprime|se|senao|enquanto|retorna|vazio|logico|real|inteiro|cadeia|caracter|declaracoes)\b", 101),
    ("DELIMITADOR", r"[{}();,:]", 102),
    ("IDENTIFICADOR", r"\b[a-zA-Z_][a-zA-Z0-9_]{0,29}\b", 103),
    ("NUMERO", r"\b\d+(\.\d+)?\b", 104),
    ("OPERADOR_ARITMETICO", r"[\+\-\*/%]", 105),
    ("OPERADOR_LOGICO", r"[<>!=]=?|==|#", 106),
    ("CADEIA", r'"[^"]{0,30}"', 107),
    ("ESPACO", r"\s+", 108),
    ("COMENTARIO", r"/\*.*?\*/", 109),  # Comentário de múltiplas linhas
    ("COMENTARIO_LINHA", r"//[^\n]*", 110),  # Comentário de linha
    ("DESCONHECIDO", r".", 999),
]

class AnalisadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo  # Mantendo o código com acentos
        self.tokens = []
        self.posicao = 0
        self.linha_atual = 1
        self.tabela_simbolos = {}

    def analisar(self):
        while self.posicao < len(self.codigo):
            match = None
            for tipo_token, regex, codigo in tokens:
                pattern = re.compile(regex, re.DOTALL | re.MULTILINE)
                match = pattern.match(self.codigo, self.posicao)
                if match:
                    valor = match.group(0)
                    
                    # Se o token for um comentário, identificar e avançar
                    if tipo_token == "COMENTARIO":
                        self.tokens.append((valor, 109, None, self.linha_atual))
                        self.posicao += len(valor)
                        self.linha_atual += valor.count("\n")
                        break
                    
                    if tipo_token == "COMENTARIO_LINHA":
                        self.tokens.append((valor, 110, None, self.linha_atual))
                        self.posicao += len(valor)
                        self.linha_atual += valor.count("\n")
                        break
                    
                    # Processar outros tokens
                    indice_tab_simb = self.tabela_simbolos.setdefault(valor, len(self.tabela_simbolos) + 1) if tipo_token == "IDENTIFICADOR" else None
                    self.tokens.append((valor, codigo, indice_tab_simb, self.linha_atual))
                    self.posicao += len(valor)
                    self.linha_atual += valor.count("\n")
                    break
            if not match:
                caractere_invalido = self.codigo[self.posicao]
                self.tokens.append((caractere_invalido, 999, None, self.linha_atual))
                self.posicao += 1
        return self.tokens

    def gerar_relatorio(self, nome_arquivo, equipe, integrantes):
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Codigo da Equipe: {equipe}\n")
            arquivo.write("Componentes:\n")
            for integrante in integrantes:
                arquivo.write(f"  {integrante}\n")
            arquivo.write("\nRELATORIO DA ANALISE LEXICA. Texto fonte analisado: Teste.231\n")
            arquivo.write("-" * 70 + "\n")
            for valor, codigo, indice_tab_simb, linha in self.tokens:
                arquivo.write(f"Lexeme: {valor}, Codigo: {codigo}, IndiceTabSimb: {indice_tab_simb}, Linha: {linha}\n")
                arquivo.write("-" * 70 + "\n")
        print(f"Relatorio gerado em {nome_arquivo}")

# Testando com o código ajustado
codigo = """
programa exemplo;
declaracoes
    real : x, y;
    cadeia : texto;
    inteiro : resultado;
fimDeclaracoes
funcoes
    inteiro : soma(x, y);
    retorna x + y;
    imprime "Resultado: ", resultado;
    /* Isso é um comentário
       que deve ser ignorado
       até o fechamento */
    /* Outro comentário aqui */
fimFunc
"""

# Informações da equipe
equipe = "02"
integrantes = [
    "Adrian Widmer; adrian.widmer@aln.senaicimatec.edu.br; (71)99284-7135",
    "Giulia Franca; giulia.franca@aln.senaicimetec.edu.br; (71)xxxx-xxxx",
    "Sicrano da Silva; sicrano.silva@ucsal.edu.br; (71)99999-9999"
]

# Executando
analisador = AnalisadorLexico(codigo)
tokens = analisador.analisar()
analisador.gerar_relatorio("saida.LEX", equipe, integrantes)
