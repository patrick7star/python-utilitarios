
# colocando toda a biblioteca aqui.
from sys import path
path.append("../../src")
from random import choice
# biblioteca padrão do terminal.
from os import get_terminal_size
from tela_i import (Ponto, Tela)
import unittest


class ClasseTela(unittest.TestCase):
   def tela_com_grade_e_sem_borda(self):
      # primeira tela, sem borda vísivel e
      # contendo grade.
      t = Tela(None, None,True)
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

   def metodo_risca(self):
      t = Tela(None, None,borda=True, grade=False)

      t.risca(Ponto(3,10), 20, simbolo='X')
      t.risca(Ponto(3, 10), 20, horizontal=False)

      # imprimindo modificação...
      print(t)
   ...

   def metodo_circula(self):
      # testando circunscrição em todos lados e cantos.
      t = Tela(None, None, borda=True, grade=False)
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

   def metodo_enquadra(self):
      # testando o método de enquadradamento.
      t = Tela(10, None)
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

   def metodo_defazer_circulacoes(self):
      # testando circunscrição em todos lados e cantos.
      t = Tela(None, None, borda=True, grade=False)
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
...

class ClasseMatriz(unittest.TestCase):
   def indexacaoComum(self):
      m = Matriz(20, 40,grade=True)
      self.assertEqual(m[10][10], '.')
      # mudando diagonal principal.
      for k in range(20):
         if choice([True, False]):
            m[k][2*k] = '#'
         else:
            m[k][2*k] = '@'
      ...
      for p in range(20):
         char = m[p][2*p]
         self.assertTrue(
            char == '#' 
            or char == '@'
         )
      ...
      print(m)
   ...
...


if __name__ == "__main__":
   unittest.main()
