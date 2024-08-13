"""
 Acessório importantissímo para gerar os gráfico
no console de tal biblioteca. Na verdade o potencial
de reutilização de tal biblioteca é o máximo possível.
"""

# bibliotecas:
import os, sys, copy

# determinando o que será importado.
__all__ = ["Tela", "Ponto"]

from typing import TypeVar, Tuple
# tipo genérico para valor interno ao ponto, podem ser decimais ou
# inteiros simples.
T = TypeVar("T", int, float)

class Ponto:
   __slot__ = ["lin", "col"]
   """
   objeto tipo coordenada para cuidar bem dos pontos do programa, ao
   decorrer do programa, muitos são utilizados.
   """
   def __init__(self, y: T, x: T) -> None:
      # só aceita valores positivos.
      if y < 0 or x < 0:
         raise ArithmeticError("valor negativo no par \"(y, x)\"")
      else:
         self.lin = y
         self.col = x
      pass

   def distancia(self, p) -> T:
      " cálcula a distância entre dois pontos "
      # parâmetro tem que ser do tipo ponto.
      if isinstance(ponto, Ponto):
         raise TypeError("argumento do tipo errado! tem que ser 'Ponto'")
      # varições verticais e horizontais.
      dy2 = (p.lin - self.lin)**2
      dx2 = (p.col - self.col)**2
      # fórmula para computar distância.
      return sqrt(dy2 + dx2)
   ...

   def __eq__(self, q):
      " verifica se ponto passado é igual a instância "
      return (q.lin == self.lin and q.col == self.col)

   def __ne__(self, ponto):
      " verifica se o argumento(um ponto) é diferente da instância "
      # parte do presuposto que ambos não são iguais.
      return not (self ==  ponto)

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

from collections.abc import Iterator
# tupla com quatro coordenadas, sendo elas colineares entre sí, no
# objetivo de formar um retângulo. Eles estão distribuídos do começo,
# sendo o ponto superior esquerdo ao inferior direito, baseado numa
# movimentação no sentido anti-horário.
Retangulo = Tuple[Ponto, Ponto, Ponto, Ponto]

from enum import (Enum, auto)
# adicionando nos métodos e artificios ao classe acima.
class Ponto(Ponto):
   __slot__ = ["iteracao_terminada", "ordenada"]

   def colinear(self, a: Ponto) -> bool:
      "não podem está sob uma mesma linha vertical ou horizontal."
      return a.y == self.y or self.x == a.x

   @staticmethod
   def _ajusta_pontos(p: Ponto, q: Ponto) -> (Ponto, Ponto):
      """
      retorna tupla com ponto inferior à esquerda de superior à direita.
      Mas o que quer dizer direita e esquerda aqui? Bem, se o ponto está
      contido -- e não se pode está adjascente a ele -- no retângulo
      formado pelas projeções do ponto mais distante, então ele é menor,
      assim dever está à esquerda, e o ponto da projeção do retângulo,
      à direita.
      """
      (xP, yP, xQ, yQ) = (p.x, p.y, q.x, q.y)
      if (xP > xQ and yP > yQ):
         # inverte a ordem dos argumentos dado na tupla.
         return (q, p)
      else:
         # apenas retorna a ordem anterior.
         return (p, q)
   ...

   # o arranjo certo de pontos.
   class Disposicao(Enum):
      # pontos, respectivamnete, superior-esquerdo e inferior-direito.
      SEID = auto()
      # pontos superior-direito e inferior-esquerdo, nesta ordem.
      SDIE = auto()
   ...

   @staticmethod
   def _modo(p: Ponto, q: Ponto) -> Disposicao:
      (xP, yP, xQ, yQ) = (p.x, p.y, q.x, q.y)

      if (xP < xQ) and (yP < yQ):
         return Ponto.Disposicao.SEID
      elif (yP > yQ) and (xP < xQ):
         return Ponto.Disposicao.SDIE
      else:
         raise ValueError("pontos não são válidos(diagonais)!")
   ...

   @staticmethod
   def retangulo(p: Ponto, q: Ponto) -> Retangulo:
      """
      dado dois pontos "não-colienares"(quero dizer que não tem
      coordenadas coincidentes), ele retorna uma tupla com quatro
      pontos, entre eles estes, representando as vértices do retângulo
      que os pontos dados formam. Eles seguirão o seguinte padrão:
      do ponto superior-esquerdo sendo o primeiro, e o inferior-esquerdo
      o último, arranjados no sentido horário.
      """
      # não aceita pontos "colineares", ou seja, numa mesma reta.
      if p.colinear(q):
         raise ValueError(
            "pontos com coordenadas correspodente,"
            + " não são válidos."
         )
      ...

      (p, q) = Ponto._ajusta_pontos(p, q)
      # vendo se os pontos estão distribuídos na forma superior-esquerdo
      # e inferior-direito, ou, superior-direito e inferior esquerdo.
      match Ponto._modo(p, q):
         case Ponto.Disposicao.SEID:
            # superior-direito:
            b = Ponto(p.y, q.x)
            # inferior-esquerdo:
            d = Ponto(q.y, p.x)
            # superior-esquerdo e inferior-direito, respectivamente:
            a = p; c = q;
         case Ponto.Disposicao.SDIE:
            # superior-esquerdo:
            a = Ponto(p.y, q.x)
            # inferior-direito:
            c = Ponto(q.y, p.x)
            # superior-direito e inferior-esquerdo:
            b = p; d = q;
         case _:
            raise Exception("nunca chega até aqui")
      ...
      return (a, b, c, d)
   ...

   # funções de acessos das duas coordenadas.
   def valor_abssissa(self):
      return self.col
   def valor_ordenada(self):
      return self.lin

   # acesso via coordenadas padrões.
   x = property(valor_abssissa, None, None, None)
   y = property(valor_ordenada, None, None, None)

   # modo de formar lista ou tuplas com este tipo.
   def __iter__(self) -> Iterator[T]:
      self.ordenada = False
      self.iteracao_terminada = False
      return self
   ...
   def __next__(self) -> T:
      if (not self.ordenada):
         self.ordenada = True
         return self.lin
      elif self.iteracao_terminada:
         raise StopIteration("ambos y e x já foram iterados!")
      else:
         self.iteracao_terminada = True
         return self.col
   ...

   # modo de visualizar a estrutura de dados.
   def __str__(self) -> str:
      return "Ponto: y={} e x={}".format(self.lin, self.col)

   def __repr__(self) -> str:
      return "({}, {})".format(self.y, self.x)
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
   def __init__(self, L, C, grade=False,borda=False):
      """
      pega  a dimensão da tela de terminal, cria
      ou não uma borda e etc.  """
      dimensao = os.get_terminal_size()
      # Número de colunas do gráfico.
      # Lembre-se que, o máximo é algo menor
      # ou igual a dimensão do terminal.
      # A segunda linha é o número de linhas.
      if C > dimensao.columns or C <= 20:
         self.colunas = dimensao.columns
      else:
         self.colunas = C-1

      if L > dimensao.lines or L <= 5:
         self.linhas = dimensao.lines - 3
      else:
         self.linhas = L-1

      # Matriz que representa a tela do programa.
      # Ela terá as dimensões dos dados passados,
      # ou o padrão do terminal.
      if grade:
         self.simbolo = '.'
      else:
         self.simbolo = ' '
      self.matriz = [[self.simbolo for i in range(self.colunas)]
                     for j in range(self.linhas)]

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

   def risca(self, L, C, comprimento, simbolo='$', horizontal=True):
      """
      faz uma rabisco na tela horizontal/vertical
      de comprimento dado, partindo de uma "linha" e
      "coluna" dada. Há um símbolo padrão, que pode ser
      alterado. """
      # se for horizontal, bem,... rabiscar horizontalmente.
      coords = []
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
            # gravando riscos.
            self.realizacoes.append(tuple(coords))
      else:
         # no outro caso, desenhar na vertical.
         for i in range(comprimento):
            if (i+L) > (self.linhas-1):
               self.matriz[i-comprimento][C+1] = simbolo
               coords.append((i-comprimento,C+1))
            else:
               self.matriz[L+i][C] = simbolo
               coords.append((L+i,C))
         self.realizacoes.append(tuple(coords))

   def limpa(self):
      "limpa toda tela, rabiscos, listas, caractéres e mais."
      for i in range(self.linhas):
         for j in range(self.colunas):
            self.matriz[i][j] = self.simbolo
      ...

   def marca(self, L,C,simbolo='x'):
      """
      Escreve uma letra em determinada posição da
      tela. A posição tem que ser válida, do caso
      contrário nada acontecerá. Existe um símbolo
      padrão de preenchimento, porém, se for dado
      algum, ele será substituído."""
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

   def escreve(self, L,C, string):
      """Escreve uma string dada a posição. Se a
      posição não for válida, ele não escreve
      a string, com ser válido, digo ela não
      transbordar a dimensão da tela."""
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

   def lista_strings(self, L, C, * strings):
      """Lista um monte de strings na ordem que
      foram dadas. Se alguma tranbordar tanto
      colunas como linhas, serão cortadas."""
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

    # Cria um retângulo dado dois pontos(dua
    # coordenadas).
   def circunscreve(self, *coordenadas):
      "desenha uma retângulo dado dois pontos distintos"
      # simplificando coordenadas.
      try:
         (l1,c1,l2,c2) = (coordenadas[0][0], coordenadas[0][1],
                          coordenadas[1][0], coordenadas[1][1])
         # unpacking pontos.
         (A, B) = coordenadas
      except:
         sys.exit('erro de sintaxe!')

      # proposições:
      # Verificando... primeiro, se há duas coordenadas.
      # Segundo, se cada coordenada têm apenas dois valores.
      p1 = (len(coordenadas) == len(coordenadas[0]) ==
          len(coordenadas) == 2)
      # Ambos pares distintos.
      p2 = coordenadas[0] != coordenadas[1]
      # tem que está superior no caso das linhas, e,
      # a esquerda no caso das colunas; digo, o/a
      # primeiro(a)/ponto coordenada em relação ao segundo.
      p3 = (c1 < c2) and (l1 < l2)
      # verifica se ambos os pontos estão no limite do quadro.
      p4 = ((0 <= l1 <= self.linhas) and (0<=c1<= self.colunas) and
            (0 <= l2 <= self.linhas) and (0 <= c2 <= self.colunas))
      # verifica transbordamento da coluna.
      p5 = ((0<=l1<=self.linhas) and (0<=c1<=self.colunas) and
            (0<=l2<=self.linhas) and (c2 > self.colunas))
      # verica um transbordamento das linhas.
      p6 = ((0<=l1<=self.linhas) and (0<=c1<=self.colunas) and
          (l2 > self.linhas) and (0 <= c2 <= self.colunas))

      # marcar todos coordenadas, ou estrutura delas
      # marcada na chamada desta função:
      coords = []
      if p3 and p1 and p2 and p4:
         # comprimentos:
         v, h = abs(l1-l2),abs(c1-c2)
         # lado superior do retângulo.
         self.risca(l1,c1, h)
         # lado esquerdo do retângulo.
         self.risca(l1,c1,v,horizontal=False)
         # lado inferior do retângulo.
         self.risca(l2,c1,h+1) # acrescenta um, pois... bem corrige o erro.
         # lado direito do retângulo.
         self.risca(l1, c2,v,horizontal=False)
         # remove e registrar as quatro feitas.
         for i in range(4):
            coords.append(self.realizacoes.pop())
         else:
            # adicionando formalmente...
            self.realizacoes(tuple(coords))
      else:
         if not p3:
            # se o 1º ponto estiver mais "distante" que
            # o 2º, usar da recursividade chamando
            # a função com parâmetros permutados.
            self.circunscreve((l2,c2),(l1,c1))
         elif not p4:
            if p5 and (not p6):
               # comprimentos dos lados:
               v,h = abs(l1-l2),abs(self.colunas-c1)
               # escrevendo lado superior...
               self.risca(l1,c1,h)
               # ... agora, escrvendo lado inferior...
               self.risca(l2,c1, h)
               #... por fim, barra esquerda.
               self.risca(l1,c1, v,horizontal=False)
               self.realizacoes.append((self.realizacoes.pop(),
                                       self.realizacoes.pop(),
                                       self.realizacoes.pop()))
            elif (not p5) and p6:
               # comprimentos dos lados:
               (v,h) = abs(self.linhas-l1), abs(c1-c2)
               # escrevendo lado superior...
               self.risca(l1,c1,h)
               #... agora, barra esquerda ...
               self.risca(l1,c1, v,horizontal=False)
               # ... por fim, barra direita.
               self.risca(l1,c2, v,horizontal=False)
               for i in range(3):
                  coords.append(self.realizacoes.pop())
               self.realizacoes.append(tuple(coords))
            else:
               # comprimentos dos lados:
               h,v = abs(c1-self.colunas), abs(l1-self.linhas)
               # escrevendo lado superior...
               self.risca(l1,c1,h)
               #... agora, barra esquerda ...
               self.risca(l1,c1, v,horizontal=False)
               self.realizacoes.append((self.realizacoes.pop(),
                                       self.realizacoes.pop()))
      ...

   def enquadra(self, L, C, altura=4, largura=5):
      """ enquadra de determinado ponto. Faz o mesmo
      que o circunscreve, porém, será preciso apena
      o primeiro ponto/coordenada, e se quiser
      passar altura ou largura do retângulo, que já
      tem tamanhos definidos. """
      self.circunscreve((L,C), (L+altura,C+largura))
      pass

   def circula(self, A, B):
      "desenha uma retângulo dado dois pontos distintos"
      # algum for diferente em tipo.
      if not (isinstance(A,Ponto) and isinstance(B, Ponto)):
         raise TypeError("um dos argumentos não são do tipo 'Ponto'")
      elif A < B:
         # caso o B esteja no C.S.E, recursão, só para
         # em termos de "namespace" não precisar escrever
         # bem mais código.
         self.circula(B, A)

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
            self.risca(B.lin, 1, h, simbolo='*')
            self.risca(1, B.col, v, horizontal=False, simbolo='*')
            pass

         elif canto_inferior_direito:
            self.risca(A.lin, A.col, h-1, simbolo='*')
            self.risca(A.lin, A.col, v-1, horizontal=False, simbolo='*')
            pass

         elif canto_inferior_esquerdo:
            self.risca(A.lin, A.col+1, h)
            self.risca(A.lin, B.col, v-1, horizontal=False)
            pass

         elif canto_superior_direito:
            self.risca(A.lin+1, A.col, v, simbolo='s', horizontal=False)
            self.risca(B.lin, A.col, h-1, simbolo='d')
            pass

         elif no_teto:
            self.risca(A.lin+1, A.col, v-1,  horizontal=False)
            self.risca(B.lin, A.col, h)
            self.risca(A.lin+1, B.col, v-1,  horizontal=False)
            pass

         elif no_solo:
            self.risca(A.lin, A.col, v-1,  horizontal=False)
            self.risca(A.lin, A.col, h)
            self.risca(A.lin, B.col, v-1,  horizontal=False)
            pass

         elif lateral_esquerda:
            self.risca(A.lin, 1, h)
            self.risca(B.lin, 1, h)
            self.risca(A.lin, B.col, v, horizontal=False)
            pass

         elif lateral_direita:
            self.risca(A.lin, A.col, h-1)
            self.risca(A.lin, A.col, v, horizontal=False)
            self.risca(B.lin, A.col, h-1)
            pass

         else:
            # lado superior do retângulo.
            self.risca(A.lin,A.col, h, simbolo='*')
            # lado esquerdo do retângulo.
            self.risca(A.lin, A.col, v,  simbolo='*',horizontal=False)
            # lado inferior do retângulo
            # acrescenta um, pois... bem corrige o erro..
            self.risca(B.lin,A.col,h+1, simbolo='*')
            # lado direito do retângulo.
            self.risca(A.lin, B.col, v, simbolo='*', horizontal=False)
            pass
      ...
   def __sizeof__(self):
      acumulado = sum(sys.getsizeof(l) for l in self.matriz)
      return (
         acumulado +
         sys.getsizeof(self.matriz) +
         sys.getsizeof(self.linhas) +
         sys.getsizeof(self.colunas) +
         sys.getsizeof(self.realizacoes)
      )
   ...
...

import unittest

class ClassePonto(unittest.TestCase):
   @unittest.skip("método 'retângulo'ainda não terminado.")
   def resultado_de_retangulo(self):
      p = Ponto(1, 5)
      q = Ponto(6, 9)
      resultado = Ponto.retangulo(p, q)
      saida = (p, Ponto(1, 9), q, Ponto(6, 5))
      self.assertEqual(resultado, saida)
      print("resultado:", resultado)
      print("saída:", saida)

      # teste de outro:
      a = Ponto(5, 5)
      b = Ponto(9, 3)
      resultado = Ponto.retangulo(a, b)
      saida = (Ponto(5, 3), a, Ponto(9, 5), b)
      self.assertEqual(resultado, saida)
      print("resultado:", resultado)
      print("saída:", saida)
   ...
   def novo_modo_de_acessar_atributos(self):
      a = Ponto(5, 23); b = Ponto(10, 3)
      print(str(a), str(b))
      print("a ---> x={} e y={}".format(a.x, a.y))
      print("b ---> x={} e y={}".format(b.x, b.y))
   ...
   def testando_iteracao(self):
      pontos = [ Ponto(15, 30), Ponto(3, 10), Ponto(7, 16) ]
      saidas = [(15, 30), (3, 10), (7, 16)]

      for (i, p) in enumerate(pontos):
         novo_p = tuple(p)
         novo_novo_p = list(p)
         print(novo_p, novo_novo_p)
         self.assertEqual(novo_p, saidas[i])
      ...
   ...
...

if __name__ == "__main__":
   unittest.main()


