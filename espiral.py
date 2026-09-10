"""
   Tentar criar um código para me ceder coordenadas de forma espiral; ou um 
 dado intervalo bidimensional.
"""

# o que será importado.
__all__ = ["range_bidimensional", "espiral"]

from collections.abc import (Generator)
from screen.tela_objetos import (Ponto)


def espiral(ponto: Ponto) -> Generator[Ponto]:
   """ 
      Dá um pares-ordenados(no formato tela, não matemático) para um desenho 
   formando uma espiral nascendo de um ponto passado.
   """

   # Funções que mudam a direção das cordenadas iniciais.
   def baixo():
      nonlocal  ponto
      ponto.lin += 1
   def direita():
      nonlocal ponto
      ponto.col += 1
   def esquerda():
      nonlocal ponto
      ponto.col -= 1
   def cima():
      nonlocal ponto
      ponto.lin -= 1

   # Funções numa ordem crescente de quatro.
   DIRECOES = (baixo, esquerda, cima, direita)
   quantia = 0 # contador e chave.

   while quantia <= 12:
      # Gera uma quantia 'q' inicialmente.
      for k in range(quantia):
         DIRECOES[quantia % 4]()
         #yield(Ponto(y, x))
         yield(ponto)

      # Aumenta a quantia a criar, e a chave para nova função computada.
      quantia += 1


def range_bidimensional(centro: Ponto, raio: int) -> Generator[Ponto]:
   """ 
     Pega um ponto e circunda ela com todos pontos formando um quadrado, 
   dado ele como centro. O "raio"(metade do lado de tal quadrado também tem 
   de ser informado também, com um limite. 
   """
   # Par ordenado baseado em tela, não-matemático molde.
   y, x = centro
   # Acha ponto superior esquerdo.
   x -= raio; y -= raio
   a = int(x); b = int(x) + 2 * raio
   c = int(y); d = int(y) + 2 * raio

   # Partindo deste ponto superior-esquerdo mapeia todo o quadrado.
   for i in range(a, b):
      for j in range(c, d):
         yield(Ponto(j, i))

# == == == == == == == == == == == === == == == == == == == == == == == == ==
#                          Testes Unitários 
# == == == == == == == == == == == === == == == == == == == == == == == == ==
import unittest, curses

class DemonstracaoSimplesEmCurses(unittest.TestCase):
   def setUp(self):
      self.janela = curses.initscr()
      (H, L) = self.janela.getmaxyx()
      self.H = H
      self.L = L
      self.meio = Ponto(H / 2, L / 2)

      curses.noecho()
      curses.curs_set(0)

   def tearDown(self): curses.endwin()

   def runTest(self):
      # Ponto médio da janela.
      SIMBOLO = 'o'

      for point in espiral(self.meio):
         (x, y) = int(point.col), int(point.lin)

         self.janela.addstr(1, 4, "linha: {}  coluna: {}" .format(y, x))
         self.janela.addch(y, x, SIMBOLO)
         self.janela.refresh()
         curses.napms(400)

class RangeBidimensional(DemonstracaoSimplesEmCurses):
   def runTest(self):
      # Ponto médio da janela.
      SIMBOLO = 'o'

      for point in range_bidimensional(self.meio, 4):
         (x, y) = int(point.col), int(point.lin)

         self.janela.addstr(1, 4, "linha: {}  coluna: {}" .format(y, x))
         self.janela.addch(y, x, SIMBOLO)
         self.janela.refresh()
         curses.napms(400)


