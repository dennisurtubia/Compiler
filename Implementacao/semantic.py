import sys
from syntax import run

def programa(node): 
    lista_declaracoes(node.children)

def lista_declaracoes(node):


def declaracao(node):
    pass

def declaracao_variaveis(node):
    pass

def inicializacao_variaveis(node):
    pass

def lista_variaveis(node):
    pass

def var(node):
    pass

def indice(node):
    pass

def tipo(node):
    pass

def declaracao_funcao(node):
    pass

def cabecalho(node):
    pass

def lista_parametros(node):
    pass


if __name__ == "__main__":
    file = open(sys.argv[1], encoding="utf8")
    code = file.read()

    raiz = run(code)
    programa(raiz)
    # print(raiz.children)

    file.close()