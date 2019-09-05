inteiro: num

{ comentario teste }

inteiro crescente(inteiro: num)
  se num = 0 então
    escreva(num)
  senão
    num := num - 1
    crescente(num)
    num := num + 1
    escreva(num)
  fim

inteiro principal()
  leia(num)
  crescente(num)
