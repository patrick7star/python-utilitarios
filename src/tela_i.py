
""" extensão para otimizar o módulo 'tela'."""

# importando biblioteca padrão do Python.
from os import get_terminal_size
from sys import platform, getsizeof
# re-exportando.
from tela_objetos import *


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
      dimensao = get_terminal_size()
      # Número de colunas do gráfico.
      # Lembre-se que, o máximo é algo menor
      # ou igual a dimensão do terminal.
      # A segunda linha é o número de linhas.
      if colunas != None: 
         self.colunas = colunas-1
      else:
         self.colunas = dimensao.columns
         # resolvendo o conflito no powershell
         # por enquanto...
         if platform == "win32":
            self.colunas -= 1

      if linhas == None:
         self.linhas = dimensao.lines - 3
      else:
         self.linhas = linhas-1

      # Matriz que representa a tela do programa.
      # Ela terá as dimensões dos dados passados,
      # ou o padrão do terminal.
      self._matriz = Matriz(
         self.linhas,
         self.colunas,
         grade
      )

      if borda:
         (L, C) = self.linhas, self.colunas
         # cantos:
         # superior-esquerdo:
         self._matriz[0][0] = '\u250c'
         # inferior-esquerdo:
         self._matriz[L-1][0] = '\u2514'
         # inferior-direito:
         self._matriz[L-1][C-1] = '\u2518'
         # superior-direito:
         self._matriz[0][C-1] = '\u2510'
         # linha vertical:
         for y in range(1, L-1):
            self._matriz[y][0]="\u2502"
            self._matriz[y][C-1] = "\u2502"
         # linha horizontal:
         for x in range(1, C-1):
            self._matriz[0][x] = "\u2500"
            self._matriz[L-1][x] = "\u2500"

      # uma pilha contendo todas as coordenadas
      # de rabiscos na tela, então quando for
      # desfazer(apagar) à última coisa rabiscada
      # ou escrita na tela, têm o conjunto
      # de coordenadas no topo da pilha.
      self._realizacoes = []
      pass

   def __str__(self):
      "retorna uma string representando a tela toda formatada"
      s = ''
      for i in range(self.linhas):
         for j in range(self.colunas):
            s += self._matriz[i][j]
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
      # lista de coordenadas e o símbolo que estava, 
      # antes decode ser sobreposto, pelo novo 
      # rabisco na Tela.
      modificacoes = []
      (L, C) = tuple(ponto)
      if horizontal:
         for j in range(comprimento):
            # se exceder o limite de colunas, continar
            # o processo na linha abaixo.
            if (j+C) > (self.colunas-1):
               (x, y) = (j-comprimento, L+1)
               antigo_simbolo = self._matriz[y][x]
               self._matriz[y][x] = simbolo
            else:
               (y, x) = (L, C+j)
               antigo_simbolo = self._matriz[y][x]
               self._matriz[y][x] = simbolo
            ...
            modificacoes.append((y, x, antigo_simbolo))
            # gravando riscos.
            #self.realizacoes.append(tuple(coords))
         ...
      else:
         # no outro caso, desenhar na vertical.
         for i in range(comprimento):
            if (i+L) > (self.linhas-1):
               (y, x) = (i-comprimento, C+1)
               antigo_simbolo = self._matriz[y][x]
               self._matriz[y][x] = simbolo
            else:
               (y, x) = (L+i, C)
               antigo_simbolo = self._matriz[y][x]
               self._matriz[L+i][C] = simbolo
            ...
            modificacoes.append((y, x, antigo_simbolo))
         ...
      self._realizacoes.append(tuple(modificacoes))
   ...

   def limpa(self):
      "limpa toda tela, rabiscos, listas, caractéres e mais."
      for i in range(self.linhas):
         for j in range(self.colunas):
            self._matriz[i][j] = self.simbolo
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
         # adicionando registro feito.
         modificacao = (L, C, self._matriz[L][C])
         self.realizacoes.append(modificacao)
         self._matriz[L][C] = simbolo
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
         for (j, char) in enumerate(string):
            (y, x) = (L, C+j)
            coords.append((y, x, self._matriz[y][x]))
            self._matriz[y][x] = char
         ...
         # registrando strings escritas.
         self._realizacoes.append(tuple(coords))
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
         self.escreve(L+i, C, s)
         # remove e registra realização feita.
         coords.append(self.realizacoes.pop())
      # agora adicionando-as formalmente...
      self._realizacoes.append(tuple(coords))
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
         canto_superior_direito = (
            B.col == self.colunas and 
            A.lin == 0
         )
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
            self._agromera_modificacoes(2)
         elif canto_inferior_direito:
            self.risca(A, h-1, simbolo='*')
            self.risca(
               A, v-1,
               horizontal=False,
               simbolo='*'
            )
            self._agromera_modificacoes(2)
         elif canto_inferior_esquerdo:
            ponto_P = Ponto(A.lin, A.col + 1)
            self.risca(ponto_P, h)
            ponto_Q = Ponto(A.lin, B.col)
            self.risca(
               ponto_Q, v-1,
               simbolo='+',
               horizontal=False
            )
            self._agromera_modificacoes(2)
         elif canto_superior_direito:
            ponto_P = Ponto(A.lin + 1, A.col)
            self.risca(
               ponto_P, v,
               simbolo='+',
               horizontal=False
            )
            ponto_Q = Ponto(B.lin, A.col)
            self.risca(ponto_Q, h-1, simbolo='+')
            self._agromera_modificacoes(2)
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
            self._agromera_modificacoes(3)
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
            self._agromera_modificacoes(3)
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
            self._agromera_modificacoes(3)
         elif lateral_direita:
            self.risca(A, h-1, simbolo='+')
            self.risca(
               A, v, simbolo='+',
               horizontal=False
            )
            ponto = Ponto(B.lin, A.col)
            self.risca(ponto, h-1, simbolo='+')
            self._agromera_modificacoes(3)
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
            self._agromera_modificacoes(4)
         ...
      ...
   ...

   def __sizeof__(self):
      tm = getsizeof(self._matriz)
      tr = getsizeof(self._realizacoes)
      dcol = getsizeof(self.colunas)
      dlin = getsizeof(self.linhas)
      return tm + tr + dcol + dlin
   ...
   
   def desfazer(self):
      "tal procedimento restaura estado antes da modificação"
      # erro caso não haja mais Ctrl-Z's
      if len(self._realizacoes) == 0:
         raise Exception("Tela está vázia[SEM MODIFICAÇÕES]")
         
      # coordenadas e símbolo posteriores da 
      # última modificação.
      ultima_modificacao = self._realizacoes.pop()
      # apenas "branquear a tela novamente."
      for celula in ultima_modificacao:
         (y, x, char) = celula
         self._matriz[y][x] = char
      ...
   ...
   
   # como algumas funções usam outras funções
   # para realizar alterações na 'Tela', a pilha 
   # de "últimas modificações" ficam com 'n' 
   # feitas(sendo este 'n', o número que o procedimento
   # realiza usando funções que geram as "últimas
   # modificações") no total. Vamos aglomerar
   # todos estes 'n' em só uma, e colocar de 
   # volta na 'Pilha'. A quantia 'n' terá que 
   # ser contada pelo codificador na hora.
   def _agromera_modificacoes(self, qtd):
      # lista para criar única modificação.
      modificacao = []
      while qtd > 0:
         remocao = self._realizacoes.pop()
         modificacao.extend(list(remocao))
         qtd -= 1
      ...
      # então empilha novamente.
      self._realizacoes.append(tuple(modificacao))
   ...
...

# determinando o que será importado.
__all__ = ["Tela", "Ponto"]


if __name__ == "__main__":
   from testes import executa_teste
   def teste_generico_da_nova_matriz():
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
   
   def testa_metodo_desfazer():
      t = Tela(None, None, grade=True)
      t.risca(Ponto(3, 7), 24)
      t.risca(Ponto(1, 16), 13, simbolo='+', horizontal=False)
      print("mostrando tela", t, sep='\n')
      t.desfazer()
      print("tela depois de desfeito", t, sep='\n')
      t.desfazer()
      print(t)
   ...
   
   executa_teste(
   teste_generico_da_nova_matriz,
   testa_metodo_desfazer
   )
...
