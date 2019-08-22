import ply.lex as lex

tokens = (
    'ID',
    'INTEIRO',
    'FLUTUANTE',
    'ATRIBUICAO'
    'FIM',
    'SE',
    'REPITA',
    'ATE',
    'LEIA',
    'ESCREVA',
    'RETORNO',
    'ENTAO',
    'SENAO',
    'OPERADOR_RELACIONAL_MENOR',
    'OPERADOR_RELACIONAL_MAIOR', 
    'OPERADOR_RELACIONAL_IGUAL',
    'OPERADOR_RELACIONAL_DIFERENTE'
    'OPERADOR_RELACIONAL_MENOR_IGUAL',
    'OPERADOR_RELACIONAL_MAIOR_IGUAL',
    'OPERADOR_SOMA',
    'OPERADOR_SUBTRACAO',
    'OPERADOR_DIVISAO',
    'OPERADOR_MULTIPLICACAO',
    'OPERADOR_LOGICO_E',
    'OPERADOR_LOGICO_OU',
    'OPERADOR_NEGACAO',
    'ABRE_PARENTESES',
    'FECHA_PARENTESES',
    'ABRE_COLCHETES',
    'FECHA_COLCHETES'
)

reserveds = {
    'se' = 'SE'
    'repita' = 'REPITA'
    'principal' = 'PRINCIPAL'
    'inteiro' = 'INTEIRO'
    'fim' = 'FIM'
}

t_ID = r'\d'
t_ATRIBUICAO = r':='
t_FIM = r'FIM'
t_SE = r'SE'
t_REPITA = r'REPITA'
t_ATE = r'ATE'
t_LEIA = r'LEIA'
t_ESCREVA = r'ESCREVA'
t_RETORNO = r'RETORNO'
t_ENTAO = r'ENTAO'
t_SENAO = r'SENAO'
t_OPERADOR_RELACIONAL_MENOR = r'<'
t_OPERADOR_RELACIONAL_MAIOR = r'>'
t_OPERADOR_RELACIONAL_IGUAL = r'='
t_OPERADOR_RELACIONAL_DIFERENTE = r'<>'
t_OPERADOR_RELACIONAL_MENOR_IGUAL = r'<='
t_OPERADOR_RELACIONAL_MAIOR_IGUAL = r'>='
t_OPERADOR_SOMA = r'\+'
t_OPERADOR_SUBTRACAO = r'-'
t_OPERADOR_DIVISAO = r'\'
t_OPERADOR_MULTIPLICACAO = r'\*'
t_OPERADOR_LOGICO_E = r'&&'
t_OPERADOR_LOGICO_OU = r'||'
t_OPERADOR_NEGACAO = r'!'
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_ABRE_COLCHETES = r'\['
t_FECHA_COLCHETES = r'\]'

def t_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLUTUANTE(t):
    r'\d+.\d+'
    t.value = float(t.value)
    return t