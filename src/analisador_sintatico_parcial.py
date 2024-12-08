import tabulate

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
            headers = ["Lexeme", "Código", "Índice da Tabela de Símbolos", "Linha"]
            tokens_table = [
                [
                    token['Lexeme'],
                    token['Código'],
                    token['Entrada'] if token['Entrada'] is not None else 'N/A',
                    ", ".join(map(str, token['Linhas']))
                ]
                for token in self.tokens
            ]
            
            # Escreve no arquivo
            arquivo.write(tabulate(tokens_table, headers=headers, tablefmt="grid"))
            arquivo.write("\n")
        
        print(f"Relatório .LEX gerado em {nome_arquivo}")

    def gerar_relatorio_tab(self, nome_arquivo, integrantes):
            """Gera o relatório .TAB com a tabela de símbolos, apenas se a análise sintática for válida."""
            caminho_arquivo_tab = os.path.splitext(nome_arquivo)[0] + ".TAB"

            # Gerando o relatório .TAB
            with open(caminho_arquivo_tab, "w", encoding="utf-8") as arquivo:
                arquivo.write("Código da Equipe: 99\n")
                arquivo.write("Componentes:\n")
                for integrante in integrantes:
                    arquivo.write(f"  {integrante}\n")
                arquivo.write(f"\nRELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {os.path.basename(nome_arquivo)}\n")

                # Cabeçalho para a tabela
                arquivo.write("Entrada | Código | Lexeme | QtdCharAntesTrunc | QtdCharDepoisTrunc | TipoSimb | Linhas\n")
                arquivo.write("-----------------------------------------------------------------------------------------\n")

                # Escrevendo os dados na tabela
                for simbolo in tabela_simbolos.values():
                    linhas = ", ".join(map(str, sorted(simbolo["Linhas"])))  # Ordenando as linhas para melhor exibição
                    arquivo.write(f"{simbolo['Entrada']} | {simbolo['Código']} | {simbolo['Lexeme']} | "
                                f"{simbolo['QtdCharAntesTrunc']} | {simbolo['QtdCharDepoisTrunc']} | "
                                f"{simbolo['TipoSimb']} | ({linhas})\n")
                    arquivo.write("-----------------------------------------------------------------------------------------\n")

            print(f"Relatório .TAB gerado em {caminho_arquivo_tab}")