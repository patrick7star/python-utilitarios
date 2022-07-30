# biblioteca padrão do terminal.
from os import get_terminal_size
# importando 'lib' especifica a testar.
from biblioteca import tela_otimizada, executa_teste
Ponto = tela_otimizada.Ponto


# primeira tela, sem borda vísivel e
# contendo grade.
def testa_tela_com_grade_e_sem_borda():
   t = tela_otimizada.Tela(None, None,True)
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
   t = tela_otimizada.Tela(None, None,borda=True, grade=False)

   t.risca(Ponto(3,10), 20, simbolo='X')
   t.risca(Ponto(3, 10), 20, horizontal=False)

   # imprimindo modificação...
   print(t)
...

# testando circunscrição em todos lados e cantos.
def testa_metodo_circula():
   t = tela_otimizada.Tela(None, None, borda=True, grade=False)
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
   t = tela_otimizada.Tela(10, None)
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
   t = tela_otimizada.Tela(None, None, borda=True, grade=False)
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
executa_teste(
   testa_tela_com_grade_e_sem_borda,
   testa_metodo_risca,
   testa_metodo_circula,
   testa_metodo_enquadra,
   testa_metodo_defazer_circulacoes
)
