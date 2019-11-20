from sys import argv
import ply.lex as lex

reserved = {
    'se': 'SE',
    'repita': 'REPITA',
    'fim': 'FIM',
    'flutuante': 'FLUTUANTE',
    'retorna': 'RETORNA',
    'então': 'ENTAO',
    'senão': 'SENAO',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'até': 'ATE',
    'inteiro': 'INTEIRO',
}

tokens = [
    'ID',
    'NOTACAO_CIENTIFICA',
    'NUMERO_FLUTUANTE',
    'NUMERO_INTEIRO',
    'ATRIBUICAO',
    'DOIS_PONTOS',
    'OPERADOR_RELACIONAL_MENOR',
    'OPERADOR_RELACIONAL_MAIOR',
    'OPERADOR_RELACIONAL_IGUAL',
    'OPERADOR_RELACIONAL_DIFERENTE',
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
    'FECHA_COLCHETES',
    'VIRGULA'
] + list(reserved.values())

t_ATRIBUICAO = r':='
t_OPERADOR_RELACIONAL_MENOR = r'<'
t_OPERADOR_RELACIONAL_MAIOR = r'>'
t_OPERADOR_RELACIONAL_IGUAL = r'='
t_OPERADOR_RELACIONAL_DIFERENTE = r'<>'
t_OPERADOR_RELACIONAL_MENOR_IGUAL = r'<='
t_OPERADOR_RELACIONAL_MAIOR_IGUAL = r'>='
t_OPERADOR_SOMA = r'\+'
t_OPERADOR_SUBTRACAO = r'-'
t_OPERADOR_DIVISAO = r'\/'
t_OPERADOR_MULTIPLICACAO = r'\*'
t_OPERADOR_LOGICO_E = r'&&'
t_OPERADOR_LOGICO_OU = r'\|\|'
t_OPERADOR_NEGACAO = r'!'
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_ABRE_COLCHETES = r'\['
t_FECHA_COLCHETES = r'\]'
t_VIRGULA = r','
t_DOIS_PONTOS = r':'

t_ignore = ' \t'


def t_COMMENT(t):
    r'{(.|\n)*?}'
    t.lexer.lineno += t.value.count('\n')
    pass


def t_NOTACAO_CIENTIFICA(t):
    r'[+-]?[1-9](\.\d+)?[Ee][-+]?\d+'
    t.value = float(t.value)
    return t


def t_NUMERO_FLUTUANTE(t):
    r'[+-]?\d+\.(\d+)?'
    t.value = float(t.value)
    return t


def t_NUMERO_INTEIRO(t):
    r'[+-]?\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[A-Za-záàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ_]+[0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Caractere ilegal: '%s';" % t.value[0])
    print("Linha número: %d \n" % t.lineno)
    t.lexer.skip(1)

lexer = lex.lex()
