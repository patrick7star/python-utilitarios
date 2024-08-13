# biblioteca padrão do terminal.
from os import get_terminal_size
from unittest import (FunctionTestCase,)
from sys import path
path.append("..")
# importando 'lib' especifica a testar.
from src.tela import Tela as TelaNova, Ponto


# primeira tela, sem borda vísivel e
# contendo grade.
def testa_tela_com_grade_e_sem_borda():
   t = TelaNova(None, None,True)
   t.risca(Ponto(5, 20), 5, horizontal=False)

   t.circula(Ponto(5, 40), Ponto(10, 60))
   t.circula(Ponto(0, 0), Ponto(3, 15))
   t.circula(
      Ponto(t.linhas-5, t.colunas-10),
      Ponto(t.linhas, t.colunas)
   )
   # imprimindo...
   print(t)
...

def testa_metodo_risca():
   t = TelaNova(None, None,borda=True, grade=False)

   t.risca(Ponto(3,10), 20, simbolo='X')
   t.risca(Ponto(3, 10), 20, horizontal=False)

   # imprimindo modificação...
   print(t)
...

# testando circunscrição em todos lados e cantos.
def testa_metodo_circula():
   t = TelaNova(None, None, borda=True, grade=False)
   compr = 7
   (P, Q) = Ponto(0, 0), Ponto(compr, compr)
   t.circula(P, Q)

   (P, Q) = Ponto(t.linhas-compr, 0), Ponto(t.linhas, compr)
   t.circula(P, Q)

   (P, Q) = (
      Ponto(0, t.colunas-compr),
      Ponto(compr, t.colunas)
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(t.linhas-compr, t.colunas-compr),
      Ponto(t.linhas, t.colunas)
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(0, int(t.colunas/2)-compr),
      Ponto(compr, int(t.colunas/2))
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(t.linhas-compr, int(t.colunas/2)-compr),
      Ponto(t.linhas, int(t.colunas/2))
   )
   t.circula(P, Q)

   (P, Q) = Ponto(compr+3, 0), Ponto(2*compr, 17)
   t.circula(P, Q)

   (P, Q) = (
      Ponto(int(t.linhas/2), t.colunas-17),
      Ponto(int(t.linhas/2)+compr, t.colunas)
   )
   t.circula(P, Q)

   # imprimindo...
   print(t)
...

# testando o método de enquadradamento.
def testa_metodo_enquadra():
   t = TelaNova(10, None)
   string = "um teste apenas!"
   t.escreve(Ponto(5,30), string)
   t.enquadra(
      Ponto(3, 28),
      altura=4,
      largura=len(string) + 3
   )
   # imprimindo...
   print(t)
...

# testando circunscrição em todos lados e cantos.
def testa_metodo_defazer_circulacoes():
   t = TelaNova(None, None, borda=True, grade=False)
   compr = 7
   (P, Q) = Ponto(0, 0), Ponto(compr, compr)
   t.circula(P, Q)

   (P, Q) = Ponto(t.linhas-compr, 0), Ponto(t.linhas, compr)
   t.circula(P, Q)

   (P, Q) = (
      Ponto(0, t.colunas-compr),
      Ponto(compr, t.colunas)
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(t.linhas-compr, t.colunas-compr),
      Ponto(t.linhas, t.colunas)
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(0, int(t.colunas/2)-compr),
      Ponto(compr, int(t.colunas/2))
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(t.linhas-compr, int(t.colunas/2)-compr),
      Ponto(t.linhas, int(t.colunas/2))
   )
   t.circula(P, Q)

   (P, Q) = Ponto(compr+3, 0), Ponto(2*compr, 17)
   t.circula(P, Q)

   (P, Q) = (
      Ponto(int(t.linhas/2), t.colunas-17),
      Ponto(int(t.linhas/2)+compr, t.colunas)
   )
   t.circula(P, Q)

   # imprimindo...
   print(t)
   t.desfazer()
   print(t)
   t.desfazer()
   print(t)
   t.desfazer()
   print(t)
   t.desfazer()
   print(t)
   t.desfazer()
   t.desfazer()
   t.desfazer()
   t.desfazer()
   print(t)
   
   # agora com circulo completo.
   (A, B) = (
      Ponto(t.linhas//2 - 7, 20),
      Ponto(t.linhas//2, 40)
   )
   t.circula(A, B)
   print(t)
   t.desfazer()
   print(t)
   try:
      t.desfazer()
      print(t)
   except:
      print("o método 'Tela.desfazer' não pode ser mais usado.")
   ...
...

# testa métodos 'desfazer' e 'refazer'.

# --- ~~~ --- ~~~ executando testes --- ~~~ --- ~~~ 
testes = (
   FunctionTestCase(testa_tela_com_grade_e_sem_borda),
   FunctionTestCase(testa_metodo_risca),
   FunctionTestCase(testa_metodo_circula),
   FunctionTestCase(testa_metodo_enquadra),
   FunctionTestCase( testa_metodo_defazer_circulacoes)
)

interruptor = [
   (testes[0], True), (testes[1], True), (testes[2], True),
   (testes[3], True), (testes[4], True),
]

for (test, permissao) in interruptor:
   if permissao:
      status = "on"
   else:
      status = "off"

   print("[{:^8s}] test '{}'".format(status, test.id()))

   if permissao:
      test.run()
...
