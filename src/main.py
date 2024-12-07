import os
import sys
from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico

integrantes = [
    "Adrian Widmer; adrian.widmer@aln.senaicimatec.edu.br; (71)99284-7135",
    "Giulia Franca; giulia.franca@aln.senaicimetec.edu.br; (71)99348-2808",
    "Marcelo Silveira; marcelo.s.filho@aln.senaicimatec.edu.br; (71)99348-2808",
    "Icaro Canela; ícaro.almeida@aln.senaicimatec.edu.br;(71)98157-4815"
]

def processar_arquivo(nome_arquivo):
    if not os.path.isfile(nome_arquivo):
        print(f"Erro: O arquivo {nome_arquivo} não foi encontrado.")
        return

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        codigo_fonte = arquivo.read()

    # Análise léxica
    analisador_lexico = AnalisadorLexico(codigo_fonte)
    tokens, tabela_simbolos = analisador_lexico.analisar()

    # Análise sintática
    analisador_sintatico = AnalisadorSintatico(tokens)
    analisador_sintatico.analisar_programa()

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    nome_base = os.path.splitext(os.path.basename(nome_arquivo))[0]

    # Caminhos para os relatórios
    caminho_relatorio_lex = os.path.join(diretorio_atual, f"{nome_base}.LEX")
    caminho_relatorio_tab = os.path.join(diretorio_atual, f"{nome_base}.TAB")

    # Geração do relatório léxico
    analisador_sintatico.gerar_relatorio_lex(caminho_relatorio_lex, "Equipe 02", integrantes)

    # Geração do relatório TAB somente se não houver erros sintáticos
    if not analisador_sintatico.erros_sintaticos:
        analisador_sintatico.gerar_relatorio_tab(tokens, caminho_relatorio_tab, integrantes)
        print("Relatório .TAB gerado com sucesso.")
    else:
        print("Relatório .TAB não gerado devido a erros na análise sintática.")
        print("Erros sintáticos encontrados:")
        for erro in analisador_sintatico.erros_sintaticos:
            print(f"- {erro}")

def main():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_testes = os.path.join(diretorio_atual, "../tests")
    nome_arquivo = None

    # Busca por arquivos de teste no diretório padrão
    if os.path.exists(diretorio_testes):
        for arquivo in os.listdir(diretorio_testes):
            if arquivo.endswith(".242"):
                nome_arquivo = os.path.join(diretorio_testes, arquivo)
                break

    # Caso nenhum arquivo seja encontrado e nenhum argumento seja fornecido
    if nome_arquivo is None and len(sys.argv) < 2:
        print("Erro: Nenhum arquivo .242 encontrado em 'tests' e nenhum arquivo fornecido. Arraste um arquivo .242 para o ícone do executável.")
        return

    if nome_arquivo is None:
        nome_arquivo = sys.argv[1]

    processar_arquivo(nome_arquivo)

if __name__ == "__main__":
    main()
