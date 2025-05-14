"""
 Para deixar o módulo 'tela' com no máximo 400 linhas, vamos colocar partes
importantes do código(como as classes 'Ponto' e 'Matriz') neste módulos. 
Serão chamadas no módulo principal e re-exportados.
"""

from array import array as Array
import sys
from enum import (auto, Enum)

# o que será importado.
__all__ = ["Matriz", "Ponto", "Lados"]

class Lados(Enum):
   SUPERIOR = auto()
   DIREITO = auto()
   INFERIOR = auto()
   ESQUERDO = auto()

class Matriz:
   def __init__(self, linhas, colunas, grade=False):
      # "reference array" contendo "compact arrays"
      # por motivos de otimização.
      self._linhas = []
      # tipo de preenchimento padrão da célula.
      if grade:
         self._celula = '.'
      else:
         self._celula = ' '
      # criando linhas do "quadro".
      for q in range(linhas):
         a = Array('u', [self._celula]*colunas)
         self._linhas.append(a)
      ...
   ...
   def __str__(self):
      string = ""
      for linha in self._linhas:
         for celula in linha:
            string += celula
         string += "\n"
      ...
      return string
   ...
   def __getitem__(self, linha_indice):
      # manda referência da array interna,
      # que também será indexada.
      return self._linhas[linha_indice]
   ...
   def __sizeof__(self):
      acumulado = sum(sys.getsizeof(s) for s in self._linhas)
      acumulado += sys.getsizeof(self._linhas)
      return acumulado + sys.getsizeof(self._celula)
   ...

   def margem(self, n: int, lado: Lados):
      "Aumenta a margem da figura em 'n' unidades, em alguma lado."
      QTD = len(self._linhas[0])
      LINHA_EM_BRANCO = Array('u', QTD * self._celula)

      match lado:
         case Lados.SUPERIOR:
            for _ in range(n):
               copia = LINHA_EM_BRANCO[:]
               self._linhas.insert(0, copia)

         case Lados.INFERIOR:
            for _ in range(n):
               copia = LINHA_EM_BRANCO[:]
               self._linhas.append(copia)

         case Lados.DIREITO:
            for subarray in self._linhas:
               for _ in range(n):
                  subarray.append(self._celula)

         case _:
            raise NotImplementedError("ainda não achei utilidade nesta")

   def dimensao(self):
      """
      retorna tupla com a dimensão, onde primeiro valor é a altura, 
      a segunda é a largura.
      """
      LINS = len(self._linhas)
      COLS = len(self._linhas[LINS - 2])

      return tuple([LINS, COLS])
...

class Ponto:
   """
   objeto tipo coordenada para cuidar bem dos
   pontos do programa, ao decorrer do programa,
   muitos são utilizados.
   """
   def __init__(self, y, x):
      # só aceita valores positivos.
      if y < 0 or x < 0:
         raise ArithmeticError("valor negativo no par \"(y, x)\"")
      else:
         self.lin = y
         self.col = x
      ...
   ...

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
...

