"""
   Implementação de matriz que dá uma visualização bidimensional do que foi
 desenhado. Assim sua manipulação também fica bem mais fácil e acessível.
"""
from array import array

# Constante que determina o símbolo de vázio no desenho de grade.
VAZIO = '¨'

class Matriz:
   "Uma matriz desenhada para a manipulação da string de árvore gerada."
   def __init__(self, trilha):
      # dividindo strings pela quebra-de-linha.
      trilha = trilha.split('\n')
      trilha.remove('')
      # quantia total de linhas.
      qtd_l = len(trilha)
      # linha com mais caractéres. 
      qtd_c = max(len(s) for s in trilha)
      # "reference array" contendo "compact arrays"
      # por motivos de otimização.
      self._linhas = []
      # tipo de preenchimento padrão da célula.
      #self._celula = '¨'
      self._celula = VAZIO
      # criando linhas do "quadro".
      for l in trilha:
         colunas = array('w', l)
         self._linhas.append(colunas)

      # igualizando colunas ...
      for l in range(len(self._linhas)):
         while len(self._linhas[l]) < qtd_c:
            self._linhas[l].append(self._celula)

   def __str__(self):
      string = []

      for linha in self._linhas:
         for celula in linha:
            string.append(celula)
         string.append('\n')

      return "".join(string)

   def __repr__(self):
      return self.__str__()
   def __getitem__(self, linha_indice):
      return self._linhas[linha_indice]

   def __sizeof__(self):
      acumulado = sum(sys.getsizeof(s) for s in self._linhas)
      acumulado += sys.getsizeof(self._linhas)
      return acumulado + sys.getsizeof(self._celula)

   def __len__(self):
      return len(self._linhas)

   def remove_grade(self):
      for linha in self._linhas:
         for c in range(len(linha)):
            if linha[c] == '¨':
               linha[c] = ' '

