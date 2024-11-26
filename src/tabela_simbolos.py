class TabelaDeSimbolos:
    def __init__(self):
        self.tabela = {}

    def adicionar(self, nome, tipo, escopo, atributos=None):
        if nome not in self.tabela:
            self.tabela[nome] = {
                "tipo": tipo,
                "escopo": escopo,
                "atributos": atributos or {}
            }
        else:
            print(f"Aviso: O identificador '{nome}' já está na tabela de símbolos.")

    def buscar(self, nome):
        return self.tabela.get(nome, None)

    def exibir(self):
        for nome, info in self.tabela.items():
            print(f"Nome: {nome}, Tipo: {info['tipo']}, Escopo: {info['escopo']}, Atributos: {info['atributos']}")
