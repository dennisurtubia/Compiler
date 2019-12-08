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
            s_declaracao(child)

def s_lista_argumentos(node):
    return [s_expressao(child) for child in node.children if child.name == 'expressao']

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
        s_verifica_crise_existencial(var_id, 'var')
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

    s_verifica_crise_existencial(funcao_id, 'func')

    tabela_simbolos[funcao_id] = {
        "is_function": True,
        "lista_parametros": lista_parametros,
        "tipo_retorno": tipo_retorno,
        "utilizada": False,
        "retorno": None,
    }

def s_declaracao_funcao(node):
    tipo_retorno = s_obter_tipo(node.children[0])
    (funcao_id, lista_parametros) = s_cabecalho(node.children[-1])

    s_inserir_func_tabela(tipo_retorno, funcao_id, lista_parametros)

def s_cabecalho(node):
    global escopo

    funcao_id = s_obter_id(node.children[0])
    escopo = funcao_id
    
    lista_parametros = s_obter_lista_parametros(node.children[2])
    
    s_corpo(node.children[4])
    
    return funcao_id, lista_parametros

def s_corpo(node):
    for child in node.children:
        if child.name == 'acao':
            s_acao(child)
            
def s_acao(node):
    child = node.children[0]
    if child.name == 'declaracao_variaveis':
        s_declaracao_variaveis(child)

    elif child.name == 'se':
        s_se(child)

    elif child.name == 'repita':
        s_repita(child)

    elif child.name == 'leia':
        s_leia(child)

    elif child.name == 'escreva':
        s_escreva(child)

    elif child.name == 'retorna':
        s_retorna(child)

    elif child.name == 'expressao':
        s_expressao(child)

def s_expressao(node):
    child = node.children[0]
    if child.name == 'expressao_logica':
        return s_expressao_logica(child)

def s_expressao_logica(node):
    child = node.children[0]
    if child.name == 'expressao_simples':
        return s_expressao_simples(child)

def s_expressao_simples(node):
    child = node.children[0]
    if child.name == 'expressao_aditiva':
        return s_expressao_aditiva(child)

def s_expressao_aditiva(node):
    child = node.children[0]
    if child.name == 'expressao_multiplicativa':
        return s_expressao_multiplicativa(child)

def s_expressao_multiplicativa(node):
    child = node.children[0]
    if child.name == 'expressao_unaria':
        return s_expressao_unaria(child)

def s_expressao_unaria(node):
    child = node.children[0]
    if child.name == 'fator':
         return s_fator(child)

def s_fator(node):
    child = node.children[0]
    if child.name == 'chamada_funcao':
        return s_chamada_funcao(child)

    if child.name == 'var':
        return s_obter_id(child.children[0])

def s_chamada_funcao(node):
    global erros, tabela_simbolos

    funcao_id = s_obter_id(node.children[0])
    parametros_chamada = s_lista_argumentos(node.children[2])
    parametros_funcao = tabela_simbolos.get(funcao_id).get("lista_parametros")

    try:
        if tabela_simbolos.get(funcao_id).get("is_var"):
            print(f"ERRO: Chamada a função ‘{funcao_id}’ que não foi declarada")
            erros += 1

    except (AttributeError):
        print(f"ERRO: Chamada a função ‘{funcao_id}’ que não foi declarada")
        erros += 1

    if funcao_id == 'principal':
        print("Erro: Chamada para a função principal não permitida")

    if len(parametros_funcao) != len(parametros_chamada):
        print(f"ERRO: Chamada à função ‘{funcao_id}’ com número de parâmetros diferente que o declarado")
        erros += 1

    tabela_simbolos[funcao_id]["utilizada"] = True

    print(tabela_simbolos.get(funcao_id))

def s_inicializacao_variaveis(node):
    pass

    # Verificar tipo do retorno com tipo da variavel retornada

def s_se(node):
    pass

def s_repita(node):
    pass

def s_leia(node):
    pass

def s_escreva(node):
    pass

def s_retorna(node):
    pass

def s_obter_tipo(node):
    return "vazio" if node.name != "tipo" else node.children[0].name

def s_obter_id(node):
    return node.children[0].name

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

def s_verifica_principal():
    global tabela_simbolos, erros

    if (("principal" not in tabela_simbolos) or ("principal" in tabela_simbolos and not tabela_simbolos.get("principal").get("is_function"))):
        print("ERRO: Função principal não declarada.")
        erros += 1

def s_verifica_crise_existencial(id, insert_type):
    global erros, escopo

    if id in tabela_simbolos:
        tipo = "Função" if tabela_simbolos.get(id).get("is_function") else "Variável"

        if tabela_simbolos.get(id).get("escopo") == escopo:
            print(f"ERRO: Variável ‘{id}’ já declarada anteriormente no escopo ‘{escopo}’")
            erros += 1

        elif tipo == "Função" and insert_type == "func":
            print(f"ERRO: {tipo} '{id}' já existente")
            erros += 1

        elif tipo == 'Variável' and insert_type == 'func':
            print(f"ERRO: {tipo} '{id}' já existente")
            erros += 1

if __name__ == "__main__":
    file = open(sys.argv[1], encoding="utf8")
    code = file.read()
    file.close()

    raiz = run(code)
    
    s_run(raiz)

s_semantic_analyzer()