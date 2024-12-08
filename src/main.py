import os
import sys

from analisador_lexico import AnalisadorLexico
from analisador_sintatico_parcial import AnalisadorSintaticoParcial, AnalisadorSintatico

integrantes = [
    "Adrian Widmer; adrian.widmer@aln.senaicimatec.edu.br; (71)99284-7135",
    "Giulia Franca; giulia.franca@aln.senaicimetec.edu.br; (71)99348-2808",
    "Marcelo Silveira; marcelo.s.filho@aln.senaicimatec.edu.br; (71)99348-2808",
    "Icaro Canela; icaro.almeida@aln.senaicimatec.edu.br; (71)98157-4815"
]

def processar_arquivo(nome_arquivo):
    if not os.path.isfile(nome_arquivo):
        print(f"Erro: O arquivo {nome_arquivo} não foi encontrado.")
        return

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        codigo_fonte = arquivo.read()

    analisador_lexico = AnalisadorLexico(codigo_fonte)
    tokens, tabela_simbolos = analisador_lexico.analisar()
    
    analisador_sintatico_parcial = AnalisadorSintaticoParcial(tokens)
    analisador_sintatico_erro = AnalisadorSintatico(tokens)

    # Corrigindo a forma de construção do caminho dos relatórios
    diretorio_atual = os.path.dirname(os.path.abspath(sys.executable))  # Corrigido para garantir que usa o diretório do executável
    nome_base = os.path.splitext(os.path.basename(nome_arquivo))[0]

    # Corrigir caminho dos relatórios
    caminho_relatorio_lex = os.path.join(diretorio_atual, f"{nome_base}.LEX")
    caminho_relatorio_tab = os.path.join(diretorio_atual, f"{nome_base}.TAB")

    # Gerar relatórios
    analisador_sintatico_parcial.gerar_relatorio_lex(caminho_relatorio_lex, "Equipe 02", integrantes)
    analisador_sintatico_parcial.gerar_relatorio_tab(caminho_relatorio_tab, "Equipe 02", integrantes)
    analisador_sintatico_erro.programa()

def main():
    diretorio_atual = os.path.dirname(os.path.abspath(sys.executable))  # Usando o diretório do executável
    diretorio_testes = os.path.join(diretorio_atual, "../tests")
    nome_arquivo = None

    if os.path.exists(diretorio_testes):
        for arquivo in os.listdir(diretorio_testes):
            if arquivo.endswith(".242"):
                nome_arquivo = os.path.join(diretorio_testes, arquivo)
                break

    if nome_arquivo is None and len(sys.argv) < 2:
        print("Erro: Nenhum arquivo .242 encontrado em 'tests' e nenhum arquivo fornecido. Arraste um arquivo .242 para o ícone do executável.")
        return

    if nome_arquivo is None:
        nome_arquivo = sys.argv[1]

    processar_arquivo(nome_arquivo)

if __name__ == "__main__":
    main()
