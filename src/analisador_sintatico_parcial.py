import os

#todo ESSA PORRA AQUI TEM QUE PRINPAR A CARALHA DO .TAB NO FORMATO LA. LEX JA TA CERTO.
#todo EH SO PEGAR TOKENS E FORMATAR. TO CANSADO. VOU DORMIR.


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens gerados pelo léxico

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

    def gerar_relatorio_tab(self, nome_arquivo, equipe, integrantes):
        """Gera o relatório .TAB com a tabela de símbolos, ignorando espaços e quebras de linha."""   

        caminho_arquivo_tab = os.path.splitext(nome_arquivo)[0] + ".TAB"

        with open(caminho_arquivo_tab, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Código da Equipe: {equipe}\n")
            arquivo.write("Componentes:\n")
            for integrante in integrantes:
                arquivo.write(f"  {integrante}\n")
            arquivo.write(f"\nRELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {os.path.basename(nome_arquivo)}\n")

            tabela_simbolos = {}
            for token in self.tokens:
                # Ignorar espaços em branco e quebras de linha
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
