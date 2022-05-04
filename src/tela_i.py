
"""
extensão para otimizar o módulo 'tela'.

"""
# importando biblioteca padrão do Python.
from array import array
import os, sys, copy

class Matriz:
   def __init__(self, qtd_l, qtd_c, grade=False):
      # "reference array" contendo "compact arrays"
      # por motivos de otimização.
      self._linhas = []
      # tipo de preenchimento padrão da célula.
      if grade:
         self._celula = '.'
      else:
         self._celula = ' '
      # criando linhas do "quadro".
      for q in range(qtd_l):
         colunas = array('u', [self._celula]*qtd_c)
         self._linhas.append(colunas)
      ...
   ...
   def altera(self, linha, coluna, char):
      # se não for uma novo caractére em branco.
      if char != self._celula:
         self._linhas[linha][coluna] = char
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
      return self._linhas[linha_indice]
   ...
   def __sizeof__(self):
      acumulado = sum(sys.getsizeof(s) for s in self._linhas)
      acumulado += sys.getsizeof(self._linhas)
      return acumulado + sys.getsizeof(self._celula)
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

class Tela:
   """
    Tal classe é muito útil para impressão na tela.
   Ela oferece um monte de ferramentas para você
   personalizar o máximo tal impressão: de "rabiscar
   o terminal" para produzir desenhos; também escrever
   palavras; listar-las também de várias maneiras. É
   realmente algo para ser reutilizado em várias outra
   aplicações para fazer impressões.
   """
   def __init__(self, linhas, colunas, grade=False, borda=False):
      """
      pega  a dimensão da tela de terminal, cria
      ou não uma borda e etc.  """
      dimensao = os.get_terminal_size()
      # Número de colunas do gráfico.
      # Lembre-se que, o máximo é algo menor
      # ou igual a dimensão do terminal.
      # A segunda linha é o número de linhas.
      if colunas != None: 
         self.colunas = colunas-1
      else:
         self.colunas = dimensao.columns

      if linhas == None:
         self.linhas = dimensao.lines - 3
      else:
         self.linhas = linhas-1

      # Matriz que representa a tela do programa.
      # Ela terá as dimensões dos dados passados,
      # ou o padrão do terminal.
      self.matriz = Matriz(
         self.linhas,
         self.colunas,
         grade
      )

      if borda:
         (L, C) = self.linhas, self.colunas
         # cantos:
         # superior-esquerdo:
         self.matriz[0][0] = '\u250c'
         # inferior-esquerdo:
         self.matriz[L-1][0] = '\u2514'
         # inferior-direito:
         self.matriz[L-1][C-1] = '\u2518'
         # superior-direito:
         self.matriz[0][C-1] = '\u2510'
         # linha vertical:
         for y in range(1, L-1):
            self.matriz[y][0]="\u2502"
            self.matriz[y][C-1] = "\u2502"
         # linha horizontal:
         for x in range(1, C-1):
            self.matriz[0][x] = "\u2500"
            self.matriz[L-1][x] = "\u2500"

      # uma pilha contendo todas as coordenadas
      # de rabiscos na tela, então quando for
      # desfazer(apagar) à última coisa rabiscada
      # ou escrita na tela, têm o conjunto
      # de coordenadas no topo da pilha.
      self.realizacoes = []
      pass

   def __str__(self):
      "retorna uma string representando a tela toda formatada"
      s = ''
      for i in range(self.linhas):
         for j in range(self.colunas):
            s += self.matriz[i][j]
         # adicionando quebra de linha.
         s +='\n'
      return s
   ...

   def risca(self, ponto, comprimento, simbolo='$', horizontal=True):
      """
      faz uma rabisco na tela horizontal/vertical
      de comprimento dado, partindo de uma "linha" e
      "coluna" dada. Há um símbolo padrão, que pode ser
      alterado.
      """
      # se for horizontal, bem,... rabiscar horizontalmente.
      coords = []
      (L, C) = tuple(ponto)
      if horizontal:
         for j in range(comprimento):
            # se exceder o limite de colunas, continar
            # o processo na linha abaixo.
            if (j+C) > (self.colunas-1):
               self.matriz[L+1][j-comprimento] = simbolo
               coords.append((L+1, j-comprimento))
            else:
               self.matriz[L][C+j] = simbolo
               coords.append((L,C+j))
            ...
            # gravando riscos.
            self.realizacoes.append(tuple(coords))
         ...
      else:
         # no outro caso, desenhar na vertical.
         for i in range(comprimento):
            if (i+L) > (self.linhas-1):
               self.matriz[i-comprimento][C+1] = simbolo
               coords.append((i-comprimento,C+1))
            else:
               self.matriz[L+i][C] = simbolo
               coords.append((L+i,C))
            ...
         ...
         self.realizacoes.append(tuple(coords))
   ...

   def limpa(self):
      "limpa toda tela, rabiscos, listas, caractéres e mais."
      for i in range(self.linhas):
         for j in range(self.colunas):
            self.matriz[i][j] = self.simbolo
      ...
   ...

   def marca(self, ponto, simbolo='x'):
      """
      Escreve uma letra em determinada posição da
      tela. A posição tem que ser válida, do caso
      contrário nada acontecerá. Existe um símbolo
      padrão de preenchimento, porém, se for dado
      algum, ele será substituído.
      """
      # para não mexer em todo código, apenas "apelidação".
      (L, C) = tuple(ponto)
      # verificando se a posição passada é
      # válida.
      p = L >= 0 and L <= (self.linhas-1)
      q = C >= 0 and C <= (self.colunas-1)
      # se for marcar na matriz.
      if p and q:
         self.matriz[L][C] = simbolo
         # adicionando registro feito.
         self.realizacoes.append((L,C))
      ...
   ...

   def escreve(self, ponto, string):
      """Escreve uma string dada a posição. Se a
      posição não for válida, ele não escreve
      a string, com ser válido, digo ela não
      transbordar a dimensão da tela."""
      # apelidação para reutilizar o código sem
      # ficar remexendo cada canto.
      (L, C) = tuple(ponto)
      # proposições:
      # se não transbordará em colunas.
      A = (C+len(string)) <= self.colunas-1
      # se não transbordará em linhas.
      B = L <= self.linhas-1
      # verifica se o tamanho da string dado
      # a posição onde colocar-lá não transborda.
      if A and B:
         # lista para todas coordenadas preenchidas.
         coords = []
         for (j, c) in enumerate(string):
            self.matriz[L][C+j] = c
            coords.append((L,C+j))
         # registrando strings escritas.
         self.realizacoes.append(tuple(coords))
      ...
   ...

   def lista_strings(self, ponto, * strings):
      """Lista um monte de strings na ordem que
      foram dadas. Se alguma tranbordar tanto
      colunas como linhas, serão cortadas."""
      # apelido para não precisar remexer todo código.
      (L, C) = tuple(ponto)
      filtro = []
      # Vamos considerar todas strings como
      # válidas, não cortando para encaxar
      # o número de linhas. Posteriormente,
      # vamos eliminar as que quebram o
      # número de colunas.
      for s in strings:
         if C + len(s) <= self.colunas-1:
            filtro.append(s)
      # escrevendo cada uma das strings na forma
      # de lista.
      coords = [] # bloco de realizações feitas.
      for i,s in enumerate(filtro):
         self.escreve(L+i,C,s)
         # remove e registra realização feita.
         coords.append(self.realizacoes.pop())
      # agora adicionando-as formalmente...
      self.realizacoes.append(tuple(coords))
      ...
   ...

   def enquadra(self, ponto, altura=4, largura=5):
      """ enquadra de determinado ponto. Faz o mesmo
      que o circunscreve, porém, será preciso apena
      o primeiro ponto/coordenada, e se quiser
      passar altura ou largura do retângulo, que já
      tem tamanhos definidos. """
      ponto_A = ponto
      ponto_B = Ponto(ponto.lin + altura, ponto.col + largura)
      self.circula(ponto_A, ponto_B)
   ...

   def circula(self, A, B):
      "desenha uma retângulo dado dois pontos distintos"
      # algum for diferente em tipo.
      if not (isinstance(A, Ponto) and isinstance(B, Ponto)):
         raise TypeError("um dos argumentos não são do tipo 'Ponto'")
      elif A < B:
         # caso o B esteja no C.S.E, recursão, só para
         # em termos de "namespace" não precisar escrever
         # bem mais código.
         self.circula(B, A)
      ...

      # proposições:
      # ponto 'A' no canto superior esquerdo.
      p1 = A > B
      # verifica se ambos os pontos estão no limite do quadro.
      # como parte-se de que o ponto B não está no canto superior
      # esquerdo, então ele sempre está mais inferior ao ponto
      # 'A' e mais para o lado direito deste também, ou seja, só
      # é preciso verifica ele para tal.
      p2 = (B.lin <= self.linhas)
      p3 = (B.col <= self.colunas)

      # comprimentos:
      (v, h) = abs(A.lin-B.lin), abs(A.col-B.col)
      # argumentos válidos.
      if p1 and p2 and p3:
         # marcar todos coordenadas, ou estrutura delas
         # marcada na chamada desta função:
         #coords = []
         # verifica se o ponto 'A' está no canto 
         # nos cantos da Tela:
         canto_superior_esquerdo = A == Ponto(0, 0)
         canto_superior_direito = (B.col == self.colunas and A.lin == 0)
         canto_inferior_direito = B == Ponto(self.linhas, self.colunas)
         canto_inferior_esquerdo = (A.col == 0 and B.lin == self.linhas)
         lateral_esquerda = (A.col == 0 and A.lin > 0)
         lateral_direita = (B.col == self.colunas and B.lin < self.linhas)
         no_teto = (A.lin == 0 and A.col > 0)
         no_solo = (B.lin == self.linhas and B.col < self.colunas)

         if canto_superior_esquerdo:
            pontoP = Ponto(B.lin, 1)
            self.risca(pontoP, h, simbolo='*')
            pontoQ = Ponto(1, B.col)
            self.risca(
               pontoQ, v,
               horizontal=False,
               simbolo='*'
            )
         elif canto_inferior_direito:
            self.risca(A, h-1, simbolo='*')
            self.risca(
               A, v-1,
               horizontal=False,
               simbolo='*'
            )
         elif canto_inferior_esquerdo:
            ponto_P = Ponto(A.lin, A.col + 1)
            self.risca(ponto_P, h)
            ponto_Q = Ponto(A.lin, B.col)
            self.risca(
               ponto_Q, v-1,
               simbolo='+',
               horizontal=False
            )
         elif canto_superior_direito:
            ponto_P = Ponto(A.lin + 1, A.col)
            self.risca(
               ponto_P, v,
               simbolo='+',
               horizontal=False
            )
            ponto_Q = Ponto(B.lin, A.col)
            self.risca(ponto_Q, h-1, simbolo='+')
         elif no_teto:
            ponto_A = Ponto(A.lin + 1, A.col)
            self.risca(
               ponto_A, v - 1,
               simbolo='+',
               horizontal=False
            )
            ponto_B = Ponto(B.lin, A.col)
            self.risca(ponto_B, h, simbolo='+')
            ponto_C = Ponto(A.lin + 1, B.col)
            self.risca(
               ponto_C, v - 1,
               simbolo='+',
               horizontal=False
            )
         elif no_solo:
            self.risca(
               A, v-1,
               simbolo='+',
               horizontal=False
            )
            self.risca(A, h, simbolo='+')
            ponto_P = Ponto(A.lin, B.col)
            self.risca(
               ponto_P, v-1,
               simbolo='+',
               horizontal=False
            )
            pass
         elif lateral_esquerda:
            ponto_P = Ponto(A.lin, 1)
            self.risca(ponto_P, h, simbolo='+')
            ponto_P = Ponto(B.lin, 1)
            self.risca(ponto_P, h, simbolo='+')
            ponto_P = Ponto(A.lin, B.col)
            self.risca(
               ponto_P, v,
               simbolo='+',
               horizontal=False
            )
         elif lateral_direita:
            self.risca(A, h-1, simbolo='+')
            self.risca(
               A, v, simbolo='+',
               horizontal=False
            )
            ponto = Ponto(B.lin, A.col)
            self.risca(ponto, h-1, simbolo='+')
            pass
         else:
            # lado superior do retângulo.
            self.risca(A, h, simbolo='*')
            # lado esquerdo do retângulo.
            self.risca(A, v,  simbolo='*',horizontal=False)
            # lado inferior do retângulo
            # acrescenta um, pois... bem corrige o erro..
            ponto = Ponto(B.lin, A.col)
            self.risca(ponto, h+1, simbolo='*')
            # lado direito do retângulo.
            ponto = Ponto(A.lin, B.col)
            self.risca(ponto, v, simbolo='*', horizontal=False)
            pass
      ...
   ...

   def __sizeof__(self):
      return sys.getsizeof(self.matriz) + sys.getsizeof(self.realizacoes)
...

# determinando o que será importado.
__all__ = ["Tela", "Ponto"]


if __name__ == "__main__":
   m = Matriz(10, 70, True)
   print(m,end="\n\n")
   m.altera(6, 35, '@'); m.altera(4, 35, '#'); m.altera(5, 35, 'X')
   print("indexa(5, 35) = ", m[5][35])
   print(m,end="\n\n")
   print("indexa(5, 35) = ", m[5][35])
   print("mudando...\naltera(4, 34) = '*'")
   m[4][34] = '*'
   print(m,end="\n\n")
...
