import sys
from syntax import run
from anytree import PreOrderIter, Node

tabela_simbolos = {}
erros = 0
escopo = "global"

def s_semantic_analyzer():
    s_verifica_principal()

def s_run(node): 
    s_lista_declaracoes(node.children[0])

def s_lista_declaracoes(node):
    number_of_childrens = len(node.children)
    if (number_of_childrens == 1):
        s_declaracao(node.children[0])
    
    elif (number_of_childrens > 1):
        for child in node.children:
            if (child.name == "lista_declaracoes"):
                s_lista_declaracoes(child)
            else:
                s_declaracao(child)

def s_declaracao(node):
    if (node.children[0].name == "declaracao_funcao"):
        s_declaracao_funcao(node.children[0])

    elif (node.children[0].name == "declaracao_variaveis"):
        s_declaracao_variaveis(node.children[0])

    elif (node.children[0].name == "inicializacao_variaveis"):
        s_inicializacao_variaveis(node.children[0])

def s_declaracao_variaveis(node):
    global tabela_simbolos
    tipo = s_obter_tipo(node.children[0])
    var = s_obter_var(node.children[2])
    s_inserir_var_tabela(tipo, var)

def s_obter_var(node):
    return [var for var in node.children if var.name == "var"]

def s_inserir_var_tabela(tipo, vars):
    global tabela_simbolos, escopo, erros

    for var in vars:
        var_id = s_obter_id(var.children[0])
        s_verifica_crise_existencial(var_id)
        dimensoes = var.children[1:]
        dimensao = {
            "tam": len(dimensoes),
        }

        tabela_simbolos[var_id] = {
            "is_var": True,
            "tipo_var": tipo,
            "escopo": escopo,
            "inicializado": False,
            "dimensao": dimensao,
        }

def s_inserir_func_tabela(tipo_retorno, funcao_id, lista_parametros):
    global tabela_simbolos

    s_verifica_crise_existencial(funcao_id)

    tabela_simbolos[funcao_id] = {
        "isFunction": True,
        "lista_parametros": lista_parametros,
        "tipo_retorno": tipo_retorno,
    }

def s_verifica_crise_existencial(id):
    global erros
    if id in tabela_simbolos:
        tipo = "Função" if tabela_simbolos.get(id).get("is_func") else "Variável"
        
        print(f"ERRO: {tipo} '{id}' já existente")
        erros += 1
        return False

    return True

def s_declaracao_funcao(node):
    global escopo
    tipo_retorno = s_obter_tipo(node.children[0])
    (funcao_id, lista_parametros) = s_cabecalho(node.children[-1])
    escopo = funcao_id

    s_inserir_func_tabela(tipo_retorno, funcao_id, lista_parametros)

def s_cabecalho(node):
    funcao_id = s_obter_id(node.children[0])
    lista_parametros = s_obter_lista_parametros(node.children[2])
    return funcao_id, lista_parametros

def s_obter_lista_parametros(node):
    nodes = [child for child in node.children if child.name == "parametro"]
    parametros = []
    for node in nodes:
        parametros.append(
            {
                "tipo": s_obter_tipo(node.children[0]),
                "parametro_id": s_obter_id(node.children[-1]),
            }
        )

    return parametros

def s_obter_tipo(node):
    return "vazio" if node.name != "tipo" else node.children[0].name

def s_obter_id(node):
    return node.children[0].name

def s_inicializacao_variaveis(node):
    pass

def s_verifica_principal():
    global tabela_simbolos, erros

    print(tabela_simbolos)
    if "principal" not in tabela_simbolos or "principal" in tabela_simbolos and "is_function" not in tabela_simbolos["principal"]:
        print("ERRO: Função principal não existente")
        erros += 1
    
    # Verificar tipo do retorno com tipo da variavel retornada

if __name__ == "__main__":
    file = open(sys.argv[1], encoding="utf8")
    code = file.read()
    file.close()

    raiz = run(code)
    
    s_run(raiz)

s_semantic_analyzer()