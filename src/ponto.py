"""
  O objeto está sendo separados em arquivos menores, primeiro porque os
 testes unitários crescem o código; segundo, pois eles são arquivos
 estruturas individuais indepedentes, e não precisam ocupar o mesmo arquivo.
 Nem faço ideia, porque cheguei a colocar-lo nele.
"""
import sys

class Ponto:
   """
   Objeto tipo coordenada para cuidar bem dos pontos do programa, ao 
   decorrer do programa, muitos são utilizados.
   """
   def __init__(self, y, x):
      # só aceita valores positivos.
      if y < 0 or x < 0:
         raise ArithmeticError("valor negativo no par \"(y, x)\"")
      else:
         self.lin = y
         self.col = x

   def _getX(self) -> int | float:
      return self.col
   # Acesso de atributos. Apenas isso, a atribuição não será permitida.
   # Para isso, apenas crie um novo 'Ponto'.
   x = property(_getX, None, None, "Valor da coordenada x.")
   @property
   def y(self) -> int | float:
      "Valor da coordenada y."
      return self.lin

   def distancia(self, ponto):
      " cálcula a distância entre dois pontos "
      # parâmetro tem que ser do tipo ponto.
      if type(ponto) != type(Ponto):
         raise TypeError("argumento do tipo errado! tem que ser 'Ponto'")
      # varições verticais e horizontais.
      dy2 = (ponto.lin - self.lin)**2
      dx2 = (ponto.col - self.col)**2
      # fórmula para computar distância.
      return sqrt(dy2 + dx2)
   ...

   def __eq__(self, ponto):
      " verifica se ponto passado é igual a instância "
      return (ponto.lin == self.lin and ponto.col == self.col)
   ...

   def __ne__(self, ponto):
      " verifica se o argumento(um ponto) é diferente da instância "
      # parte do presuposto que ambos não são iguais.
      return not (self ==  ponto)
   ...

   def __gt__(self, ponto):
      """
      verifica se a instância está no canto superior
      esquerdo da tela, em relação ao ponto passado
      como argumento. """
      # eles tem que inicialmente, não serem o
      # mesmo, ou seja, não estarem na mesma posição.
      p1 = self != ponto
      # não são aceitos mesmos 'y' ou 'x'
      # dos pontos.
      p2 = self.lin < ponto.lin
      p3 = self.col < ponto.col

      # as três posições tem que ser
      # verídicas.
      return p1 and p2 and p3
   ...

   def __lt__(self, ponto):
      """
      verifica se a instância não está, no canto
      superior esquerdo, relativo ao ponto passado
      como argumento. """
      # eles tem que inicialmente, não serem o
      # mesmo, ou seja, não estarem na mesma posição.
      p = self != ponto
      # o resto é a negação do método anterior, se ele
      # no caso identifica o ponto superior esquerdo da 
      # relação, este aqui, reconhece quem não é 
      # tal ponto.
      return (self > ponto) and p

   def __xor__(self, ponto):
      # eles não podem está na mesma coluna...
      colunas_distintas = self.col != ponto.col
      # nem na mesma linha
      linhas_distintas = self.lin != ponto.lin
      # ambos acima tem que ser válidas.
      return colunas_distintas and linhas_distintas
   ...
   def __sizeof__(self):
      return sys.getsizeof(self.x) + sys.getsizeof(self.y)
   ...

   def __iter__(self):
      self._primeiro_ja_foi = False
      self._segundo_ja_foi = False
      return self
   ...

   def __next__(self):
      if not self._primeiro_ja_foi:
         self._primeiro_ja_foi = True
         return self.lin
      elif not self._segundo_ja_foi:
         self._segundo_ja_foi = True
         return self.col
      else:
         raise StopIteration("sem mais valores a iterar!")
   ...

# == == == == == == == == == == == === == == == == == == == == == == == ===
#                          Testes Unitários 
# == == == == == == == == == == == === == == == == == == == == == == == ===
from unittest import (TestCase)

class AcessoAtributosDoPonto(TestCase):
   def runTest(self):
      A = Ponto(15, 3)

      print("Coordenada(x): %d" % A.x)
      print("Coordenada(y): %d" % A.y)
