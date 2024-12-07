import re

# Definindo os tipos de tokens que o analisador irá reconhecer
tokens = [
    ("PALAVRA_CHAVE", r"\b(PROGRAMA|FIMPROGRAMA|FIMDECLARACOES|FIMFUNC|FUNCOES|IMPRIME|SE|SENAO|ENQUANTO|RETORNA|VAZIO|LOGICO|REAL|INTEIRO|CADEIA|CARACTER|DECLARACOES)\b", 101),
    ("DELIMITADOR", r"[{}();,:]", 102),
    ("IDENTIFICADOR", r"\b[A-Z_][A-Z0-9_]{0,29}\b", 103),  # Nomes
    ("NUMERO", r"\b\d+(\.\d+)?\b", 104),  # Valores Numéricos
    ("OPERADOR_ARITMETICO", r"[\+\-\*/%]", 105),  # Matemática
    ("OPERADOR_LOGICO", r"[<>!=]=?|==|#", 106),  # Lógica
    ("CADEIA", r'"[^"]{0,30}"', 107),  # Vetor
    ("ESPACO", r"\s+", 108),  # Vazio
    ("DESCONHECIDO", r".", 999),  # Token inválido
]

class AnalisadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo.upper()
        self.tokens = []
        self.posicao = 0
        self.linha_atual = 1
        self.tabela_simbolos = {}

    def remover_comentarios(self):
        codigo_limpo = ""
        i = 0
        while i < len(self.codigo):
            if self.codigo[i:i+2] == "//":  # Comentário de linha
                # Ignorar tudo até a quebra de linha
                while i < len(self.codigo) and self.codigo[i] != '\n':
                    i += 1
            elif self.codigo[i:i+2] == "/*":  # Comentário de múltiplas linhas
                # Ignorar até o fechamento do comentário */
                i += 2
                while i < len(self.codigo) and self.codigo[i:i+2] != "*/":
                    i += 1
                i += 2  # Avançar para depois do "*/"
            else:
                # Copiar o caractere se não for parte de um comentário
                codigo_limpo += self.codigo[i]
                i += 1
        return codigo_limpo

    def analisar(self):
        # Limpar o código removendo os comentários antes de começar a análise léxica
        codigo_sem_comentarios = self.remover_comentarios()
        self.codigo = codigo_sem_comentarios.upper()  # Garantir que o código está em maiúsculas

        while self.posicao < len(self.codigo):
            match = None
            for tipo_token, regex, codigo in tokens:
                pattern = re.compile(regex, re.DOTALL | re.MULTILINE)
                match = pattern.match(self.codigo, self.posicao)
                if match:
                    valor = match.group(0)

                    # Processar outros tokens
                    if tipo_token == "IDENTIFICADOR":
                        # Adiciona identificador à tabela de símbolos se for a primeira vez
                        indice_tab_simb = self.tabela_simbolos.setdefault(valor, len(self.tabela_simbolos) + 1)
                    else:
                        indice_tab_simb = None
                    
                    # Adiciona o token à lista de tokens (sem comentários)
                    self.tokens.append((valor, codigo, indice_tab_simb, self.linha_atual))
                    self.posicao += len(valor)
                    self.linha_atual += valor.count("\n")
                    break

            # Tratamento de caracteres desconhecidos
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
            arquivo.write("\nRELATORIO DA ANALISE LEXICA. Texto fonte analisado: Teste.242\n")  # Alteração da extensão para .242
            arquivo.write("-" * 70 + "\n")
            for valor, codigo, indice_tab_simb, linha in self.tokens:
                arquivo.write(f"Lexeme: {valor}, Codigo: {codigo}, IndiceTabSimb: {indice_tab_simb}, Linha: {linha}\n")
                arquivo.write("-" * 70 + "\n")
        print(f"Relatorio gerado em {nome_arquivo}")
    
    def gerar_relatorio_tab(self, nome_arquivo, equipe, integrantes):
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Codigo da Equipe: {equipe}\n")
            arquivo.write("Componentes:\n")
            for integrante in integrantes:
                arquivo.write(f"  {integrante}\n")
            arquivo.write("\nRELATORIO DA TABELA DE SIMBOLOS. Texto fonte analisado: Teste.242\n") 
            for valor, codigo, indice_tab_simb, linha in self.tokens:
                arquivo.write(f"Entrada: {indice_tab_simb if indice_tab_simb else 'N/A'}, Codigo: {codigo}, Lexeme: {valor}\n")
                arquivo.write(f"QtdCharAntesTrunc: {len(valor)}, QtdCharDepoisTrunc: {len(valor)}\n")
                arquivo.write(f"TipoSimb: {'IDENTIFICADOR' if indice_tab_simb else 'OUTRO'}, Linhas: {linha}\n")
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
    // Este é um comentário de linha
fimFunc
"""

# Informações da equipe
equipe = "02"
integrantes = [
    "Adrian Widmer; adrian.widmer@aln.senaicimatec.edu.br; (71)99284-7135",
    "Giulia Franca; giulia.franca@aln.senaicimetec.edu.br; (71)xxxx-xxxx",
    "Sicrano da Silva; sicrano.silva@ucsal.edu.br; (71)99999-9999",
    "Marcelo Silveira; marcelo.s.filho@aln.senaicimatec.edu.br; (71)99348-2808"
]

# Executando
analisador = AnalisadorLexico(codigo)
tokens = analisador.analisar()
#analisador.gerar_relatorio("saida.LEX", equipe, integrantes)
analisador.gerar_relatorio_tab("saida.TAB", equipe, integrantes)



