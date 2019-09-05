import utils
from sys import argv
import ply.lex as lex


if __name__ == "__main__":
    f = open(argv[1], "r")
    source_code = f.read()
    f.close()

    lexer = lex.lex(module=utils)
    lexer.input(source_code)
    while True:
        tok = lexer.token()
        if not tok:
            break
        # print(tok.type, '=', tok.value, '\n', 'Linha: ', tok.lineno, '\n')
        print(tok.type)
