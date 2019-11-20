
import ply.yacc as yacc
from anytree import Node
from lexer import tokens
import sys
from anytree.exporter import UniqueDotExporter

raiz = None

def p_programa(p):
    """ programa : lista_declaracoes """
    global raiz

    raiz = Node("programa")
    p[0] = raiz
    p[1].parent = raiz

def p_lista_declaracoes(p):
    """ lista_declaracoes : lista_declaracoes declaracao
        | declaracao    
    """
    lista_declaracoes = Node("lista_declaracoes")
    p[0] = lista_declaracoes

    if len(p) > 2:
        for child in p[1].children:
            child.parent = p[0]

        p[2].parent = lista_declaracoes

    else:
        p[1].parent = p[0]

def p_declaracao(p):
    """ declaracao : declaracao_variaveis
        | inicializacao_variaveis
        | declaracao_funcao
    """
    declaracao = Node("declaracao")
    p[0] = declaracao
    p[1].parent = declaracao

def p_declaracao_variaveis(p):
    """ declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis """
    
    declaracao_variaveis = Node("declaracao_variaveis")
    p[0] = declaracao_variaveis

    p[1].parent = declaracao_variaveis
    
    dois_pontos = Node("DOIS_PONTOS", parent=declaracao_variaveis)
    Node(p[2], parent=dois_pontos)
    p[2] = dois_pontos
    
    p[3].parent = declaracao_variaveis

def p_declaracao_variaveis_error1(p):
    """ declaracao_variaveis : tipo DOIS_PONTOS error  """
    print("Lista de variaveis com erro")
    exit(1)

def p_declaracao_variaveis_error(p):
    """ declaracao_variaveis : tipo DOIS_PONTOS  """
    print("Lista de variaveis faltando")
    exit(1)

def p_inicializacao_variaveis(p):
    """ inicializacao_variaveis : atribuicao """
    inicializacao_variaveis = Node("inicializacao_variaveis")
    p[0] = inicializacao_variaveis
    p[1].parent = inicializacao_variaveis

def p_tipo(p):
    """ tipo : INTEIRO
        | FLUTUANTE
    """
    tipo = Node("tipo")
    p[0] = tipo
    t = Node(p[1], parent=tipo)
    Node(p[1], parent=t)
    p[1] = t

def p_declaracao_funcao(p):
    """ declaracao_funcao : tipo cabecalho
        | cabecalho
    """
    declaracao_funcao = Node("declaracao_funcao")

    p[0] = declaracao_funcao
    p[1].parent = declaracao_funcao

    if len(p) > 2:
        p[2].parent = declaracao_funcao

def p_lista_variaveis(p):
    """ lista_variaveis : lista_variaveis VIRGULA var
        | var
    """
    lista_variaveis = Node("lista_variaveis")

    p[0] = lista_variaveis

    if len(p) > 2:
        for child in p[1].children:
            child.parent = p[0]

        virgula = Node("virgula", parent=lista_variaveis)
        Node(p[2], parent=virgula)
        p[2] = virgula

        p[3].parent = lista_variaveis
    else:
        p[1].parent = p[0]


def p_var(p):
    """ var : ID
        | ID indice
    """
    var = Node("var")
    p[0] = var

    id = Node("ID", parent=var)
    Node(p[1], parent=id)
    p[1] = id
    
    if len(p) > 2:
        for ind in p[2]:
            ind.parent = var 

def p_indice(p):
    """ indice : indice ABRE_COLCHETES expressao FECHA_COLCHETES
        | ABRE_COLCHETES expressao FECHA_COLCHETES
    """
    indice = Node("indice")


    if len(p) == 4:
        abre_colchetes = Node("ABRE_COLCHETES", parent=indice)
        Node(p[1], parent=abre_colchetes)
        p[1] = abre_colchetes

        p[2].parent = indice

        fecha_colchetes = Node("FECHA_COLCHETES", parent=indice)
        Node(p[3], parent=fecha_colchetes)
        p[3] = fecha_colchetes

        p[0] = [indice]

    else:

        abre_colchetes = Node("ABRE_COLCHETES", parent=indice)
        Node(p[2], parent=abre_colchetes)
        p[2] = abre_colchetes

        p[3].parent = indice

        fecha_colchetes = Node("FECHA_COLCHETES", parent=indice)
        Node(p[4], parent=fecha_colchetes)
        p[4] = fecha_colchetes

        p[0] = p[1] + [indice]
 

def p_cabecalho(p):
    """ cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo FIM """
    cabecalho = Node("cabecalho")

    p[0] = cabecalho

    id = Node("ID", parent=cabecalho)
    Node(p[1], parent=id)
    p[1] = id

    abre_parenteses = Node("ABRE_PARENTESES", parent=cabecalho)
    Node(p[2], parent=abre_parenteses)
    p[2] = abre_parenteses

    p[3].parent = cabecalho

    fecha_parenteses = Node("FECHA_PARENTESES", parent=cabecalho)
    Node(p[4], parent=fecha_parenteses)
    p[4] = fecha_parenteses

    p[5].parent = cabecalho

    fim = Node("FIM", parent=cabecalho)
    Node(p[6], parent=fim)
    p[6] = fim

def p_cabecalho_error_fim(p):
    """ cabecalho : ID ABRE_PARENTESES lista_parametros FECHA_PARENTESES corpo """
    print("TOKEN FIM faltante\n Funcao: %s" % (p[1]))
    global raiz
    raiz = None
    exit(1)

def p_lista_parametros(p):
    """ lista_parametros : lista_parametros VIRGULA parametro
        | parametro
        | vazio
    """
    lista_parametros = Node("lista_parametros")
    p[0] = lista_parametros

    if len(p) > 2:
        for child in p[1].children:
            child.parent = p[0]

        virgula = Node("VIRGULA", parent=lista_parametros)
        Node(p[2], parent=virgula)
        p[2] = virgula

        p[3].parent = lista_parametros

    else:
        p[1].parent = lista_parametros

def p_acao(p):
    """ acao : expressao
        | declaracao_variaveis
        | se
        | repita
        | leia
        | escreva
        | retorna
    """
    acao = Node("acao")
    p[0] = acao
    p[1].parent = acao

def p_corpo(p):
    """ corpo : corpo acao
        | vazio
    """
    corpo = Node("corpo")
    p[0] = corpo

    if len(p) > 2:
        for child in p[1].children:
            child.parent = corpo
        
        p[2].parent = p[0]

    else:
        p[1].parent = p[0]

def p_parametro(p):
    """ parametro : tipo DOIS_PONTOS ID
        | parametro ABRE_COLCHETES FECHA_COLCHETES
    """
    parametro = Node("parametro")
    p[0] = parametro
    p[1].parent = parametro
    
    if p[2] == ":":
        dois_pontos = Node("DOIS_PONTOS", parent=parametro)
        Node(p[2], parent=dois_pontos)
        p[2] = dois_pontos

        id = Node("ID", parent=parametro)
        Node(p[3], parent=id)
        p[3] = id

    
    else:
        abre_colchetes = Node("ABRE_COLCHETES", parent=parametro)
        Node(p[2], parent=abre_colchetes)
        p[2] = abre_colchetes

        fecha_colchetes = Node("FECHA_COLCHETES", parent=parametro)
        Node(p[3], parent=fecha_colchetes)
        p[3] = fecha_colchetes


def p_se(p):
    """ se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM
    """
    se = Node("se")
    p[0] = se
    p[1] = Node("SE", parent=se)
    p[2].parent = se
    p[3] = Node("ENTAO", parent=se)
    p[4].parent = se

    if len(p) > 6:
        p[5] = Node("SENAO", parent=se)

        p[6].parent = se
        p[7] = Node("FIM", parent=se)

    
    else:
        p[5] = Node("FIM", parent=se)

def p_se_error_entao(p):
    """ se : SE expressao error
    """
    print("ENTAO faltante")
    exit(1)


def p_repita(p):
    """ repita : REPITA corpo ATE expressao """
    repita = Node("repita")
    p[0] = repita

    r = Node("REPITA", parent=repita)
    Node(p[1], parent=r)
    p[1] = r

    p[2].parent = repita

    a = Node("ATE", parent=repita)
    Node(p[3], parent=a)
    p[3] = a

    p[4].parent = repita

def p_atribuicao(p):
    """ atribuicao : var ATRIBUICAO expressao """
    atribuicao = Node("atribuicao")
    p[0] = atribuicao
    p[1].parent = atribuicao
    p[2] = Node(p[2], parent=atribuicao)
    p[3].parent = atribuicao

def p_leia(p):
    """ leia : LEIA ABRE_PARENTESES var FECHA_PARENTESES """
    leia = Node("leia")
    p[0] = leia
    p[1] = Node("LEIA", parent=leia)

    abre_parenteses = Node("ABRE_PARENTESES", parent=leia)
    Node(p[2], parent=abre_parenteses)
    p[2] = abre_parenteses

    p[3].parent = leia

    fecha_parenteses = Node("FECHA_PARENTESES", parent=leia)
    Node(p[4], parent=fecha_parenteses)
    p[4] = fecha_parenteses

def p_escreva(p):
    """ escreva : ESCREVA ABRE_PARENTESES expressao FECHA_PARENTESES """
    escreva = Node("escreva")
    p[0] = escreva
    p[1] = Node("ESCREVA", parent=escreva)

    abre_parenteses = Node("ABRE_PARENTESES", parent=escreva)
    Node(p[2], parent=abre_parenteses)
    p[2] = abre_parenteses

    p[3].parent = escreva


    fecha_parenteses = Node("FECHA_PARENTESES", parent=escreva)
    Node(p[4], parent=fecha_parenteses)
    p[4] = fecha_parenteses

def p_retorna(p):
    """ retorna : RETORNA ABRE_PARENTESES expressao FECHA_PARENTESES """
    retorna = Node("retorna")
    p[0] = retorna
    p[1] = Node("RETORNA", parent=retorna)
    p[2] = Node("ABRE_PARENTESES", parent=retorna)
    p[3].parent = retorna
    p[4] = Node("FECHA_PARENTESES", parent=retorna)

def p_expressao(p):
    """ expressao : expressao_logica
        | atribuicao
    """
    expressao = Node("expressao")
    p[0] = expressao
    p[1].parent = expressao

def p_expressao_logica(p):
    """ expressao_logica : expressao_simples
        | expressao_logica operador_logico expressao_simples
    """
    expressao_logica = Node("expressao_logica")
    p[0] = expressao_logica
    p[1].parent = expressao_logica
    
    if len(p) > 2:
        p[1].parent = expressao_logica
        p[2].parent = expressao_logica
        p[3].parent = expressao_logica

def p_expressao_simples(p):
    """ expressao_simples : expressao_aditiva
        | expressao_simples operador_relacional expressao_aditiva
    """
    expressao_simples = Node("expressao_simples")
    p[0] = expressao_simples
    p[1].parent = expressao_simples

    if len(p) > 2:
        p[2].parent = expressao_simples
        p[3].parent = expressao_simples
    
def p_expressao_aditiva(p):
    """ expressao_aditiva : expressao_multiplicativa
        | expressao_aditiva operador_soma expressao_multiplicativa
    """
    expressao_aditiva = Node("expressao_aditiva")
    p[0] = expressao_aditiva
    p[1].parent = expressao_aditiva

    if len(p) > 2:
        p[2].parent = expressao_aditiva
        p[3].parent = expressao_aditiva

def p_expressao_multiplicativa(p):
    """ expressao_multiplicativa : expressao_unaria
        | expressao_multiplicativa operador_multiplicacao expressao_unaria
    """
    expressao_multiplicativa = Node("expressao_multiplicativa")
    p[0] = expressao_multiplicativa
    p[1].parent = expressao_multiplicativa

    if len(p) > 2:
        p[2].parent = expressao_multiplicativa
        p[3].parent = expressao_multiplicativa

def p_expressao_unaria(p):
    """ expressao_unaria : fator
        | operador_soma fator
        | operador_negacao fator
    """
    expressao_unaria = Node("expressao_unaria")
    p[0] = expressao_unaria
    p[1].parent = expressao_unaria

    if len(p) > 2:
        p[2].parent = expressao_unaria

def p_operador_relacional_menor(p):
    """ operador_relacional : OPERADOR_RELACIONAL_MENOR """
    operador_relacional = Node("operador_relacional")
    p[0] = operador_relacional
    p[1] = Node("OPERADOR_RELACIONAL_MENOR", parent=operador_relacional)

def p_operador_relacional_maior(p):
    """ operador_relacional : OPERADOR_RELACIONAL_MAIOR """
    operador_relacional = Node("operador_relacional")
    p[0] = operador_relacional
    p[1] = Node("OPERADOR_RELACIONAL_MAIOR", parent=operador_relacional)

def p_operador_relacional_igual(p):
    """ operador_relacional : OPERADOR_RELACIONAL_IGUAL """
    operador_relacional = Node("operador_relacional")
    p[0] = operador_relacional
    p[1] = Node("OPERADOR_RELACIONAL_IGUAL", parent=operador_relacional)

def p_operador_relacional_diferente(p):
    """ operador_relacional : OPERADOR_RELACIONAL_DIFERENTE """
    operador_relacional = Node("operador_relacional")
    p[0] = operador_relacional
    p[1] = Node("OPERADOR_RELACIONAL_DIFERENTE", parent=operador_relacional)

def p_operador_relacional_menor_igual(p):
    """ operador_relacional : OPERADOR_RELACIONAL_MENOR_IGUAL """
    operador_relacional = Node("operador_relacional")
    p[0] = operador_relacional
    p[1] = Node("OPERADOR_RELACIONAL_MENOR_IGUAL", parent=operador_relacional)

def p_operador_relacional_maior_igual(p):
    """ operador_relacional : OPERADOR_RELACIONAL_MAIOR_IGUAL """
    operador_relacional = Node("operador_relacional")
    p[0] = operador_relacional
    p[1] = Node("OPERADOR_RELACIONAL_MAIOR_IGUAL", parent=operador_relacional)

def p_operador_soma(p):
    """ operador_soma : OPERADOR_SOMA
        | OPERADOR_SUBTRACAO
    """
    operador_soma = Node("operador_soma")
    p[0] = operador_soma

    p[1] = Node(p[1], parent=operador_soma)

def p_operador_logico(p):
    """ operador_logico : OPERADOR_LOGICO_E
        | OPERADOR_LOGICO_OU 
    """
    operador_logico = Node("operador_logico")
    p[0] = operador_logico

    if p[1] == "OPERADOR_LOGICO_E":
        p[1] = Node("OPERADOR_LOGICO_E", parent=operador_logico)


    else:
        p[1] = Node("OPERADOR_LOGICO_OU", parent=operador_logico)


def p_operador_negacao(p):
    """ operador_negacao : OPERADOR_NEGACAO """
    operador_negacao = Node("operador_negacao")
    p[0] = operador_negacao

    operador = Node("OPERADOR_NEGACAO", parent=operador_negacao)
    Node(p[1], parent=operador)
    p[1] = operador

def p_operador_multiplicacao(p):
    """ operador_multiplicacao : OPERADOR_MULTIPLICACAO
        | OPERADOR_DIVISAO
    """
    operador_multiplicacao = Node("operador_multiplicacao")
    p[0] = operador_multiplicacao

    operador = Node(p[1], parent=operador_multiplicacao)
    Node(p[1], parent=operador)
    p[1] = operador

def p_fator(p):
    """ fator : ABRE_PARENTESES expressao FECHA_PARENTESES
        | var
        | chamada_funcao
        | numero
    """
    fator = Node("fator")
    p[0] = fator

    if len(p) > 2:
        abre_parenteses = Node("ABRE_PARENTESES", parent=fator)
        Node(p[1], parent=abre_parenteses)
        p[1] = abre_parenteses

        p[2].parent = fator
        
        fecha_parenteses = Node("FECHA_PARENTESES", parent=fator)
        Node(p[3], parent=fecha_parenteses)
        p[3] = fecha_parenteses


    else:
        p[1].parent = fator

def p_numero_inteiro(p):
    """ numero : NUMERO_INTEIRO """
    numero = Node("numero")
    p[0] = numero
    
    numero_inteiro = Node("NUMERO_INTEIRO", parent=numero)
    Node(p[1], parent=numero_inteiro)
    p[1] = numero_inteiro

def p_numero_flutuante(p):
    """ numero : NUMERO_FLUTUANTE """
    numero = Node("numero")
    p[0] = numero

    numero_flutuante = Node("NUMERO_FLUTUANTE", parent=numero)
    Node(p[1], parent=numero_flutuante)
    p[1] = numero_flutuante

def p_numero_notacao_cientifica(p):
    """ numero : NOTACAO_CIENTIFICA """
    numero = Node("numero")
    p[0] = numero

    notacao_cientifica = Node("NOTACAO_CIENTIFICA", parent=numero)
    Node(p[1], parent=notacao_cientifica)
    p[1] = notacao_cientifica

def p_chamada_funcao(p):
    """ chamada_funcao : ID ABRE_PARENTESES lista_argumentos FECHA_PARENTESES """
    chamada_funcao = Node("chamada_funcao")
    p[0] = chamada_funcao

    id = Node("ID", parent=chamada_funcao)
    Node(p[1], parent=id)
    p[1] = id

    abre_parenteses = Node("ABRE_PARENTESES", parent=chamada_funcao)
    Node(p[2], parent=abre_parenteses)
    p[2] = abre_parenteses

    fecha_parenteses = Node("FECHA_PARENTESES", parent=chamada_funcao)
    Node(p[4], parent=fecha_parenteses)
    p[4] = fecha_parenteses

def p_lista_argumentos(p):
    """ lista_argumentos : lista_argumentos VIRGULA expressao
        | expressao
        | vazio
    """
    lista_argumentos = Node("lista_argumentos")
    p[0] = lista_argumentos

    if len(p) > 2:
        p[1].parent = lista_argumentos
        virgula = Node("VIRGULA", parent=lista_argumentos)
        Node("VIRGULA", parent=virgula)
        p[2] = virgula

    else:
        p[1].parent = lista_argumentos

def p_vazio(p):
    """ vazio : """
    vazio = Node("vazio")
    p[0] = vazio
    pass


def p_error(p):
    if p:
        global raiz
        print("Erro de sintaxe próximo à linha {} e ao token: {}".format(p.lineno, p.value))
        raiz = None
        exit(1)
    return

def run(code):
    parser = yacc.yacc()

    try:
        parser.parse(code, debug=False)
    except Exception as e:
        raise e
    
    if (raiz):
        print("Gerando a imagem da árvore")
        UniqueDotExporter(raiz).to_picture("arvore.png")
        return raiz
    else:
        print("Não foi possível gerar a árvore sintática")
