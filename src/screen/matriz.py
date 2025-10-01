"""
  O objeto está sendo separados em arquivos menores, primeiro porque os
 testes unitários crescem o código; segundo, pois eles são arquivos
 estruturas individuais indepedentes, e não precisam ocupar o mesmo arquivo.
 Nem faço ideia, porque cheguei a colocar-lo nele.
"""
from array import array as Array
from enum import (auto, Enum)

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
