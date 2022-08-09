
"""
 Implementando a formação de Tabelas para
 minha 'biblioteca padrão' Python.
"""

from os import get_terminal_size
from copy import deepcopy
from array import array as Array

class Coluna():
   def __init__(self, rotulo, array):
      self._rol = array
      self._nome = rotulo
   ...
   
   def rol_iter(self):
      "itera todos dados do rol"
      for dado in self._rol:
         yield dado
   ...
   
   def nome(self):
      "encapsulamento, retorna o rótulo da coluna"
      return self._nome
   
   def __len__(self):
      "quantia de dados no rol"
      return len(self._rol)
...

# separador inicial das células e rótulos.
BARRA = '#'
# vácuo de espaço comum para debug.
ESPACO = ' '
# separador da borda.
MARGEM = ' '
# representação da célula vázia.
TRACOS = "---"


# ajusta baseado no comprimento passado
# "adicionando margens" a string.
def equilibra_str(string, comprimento):
   str_comprimento = len(string)
   if str_comprimento % 2 != 0:
      consertada = string + ESPACO
      return equilibra_str(consertada, comprimento)
      
   if len(string) <= comprimento:
      diferenca = abs(len(string) - comprimento)
      while len(string) < comprimento:
         string = (
            "{espaco}{}{espaco}"
            .format(string, espaco=ESPACO)
         )
      ...
   ...
   return string
...

def aglomera_colunas(coluna1, coluna2):
   linhas = []
   maior_qtd = max(len(coluna1), len(coluna2))
   
   i1 = coluna1.rol_iter()
   i2 = coluna2.rol_iter()
   
   rotulo1 = coluna1.nome()
   rotulo1 = equilibra_str(rotulo1, len(rotulo1))
   rotulo2 = coluna2.nome()
   rotulo2 = equilibra_str(rotulo2, len(rotulo2))
   linhas.append(
      "{barra}{margem}{0}{margem}{barra}{margem}{1}{margem}{barra}"
      .format(
         rotulo2, 
         rotulo1, 
         barra = BARRA,
         margem = MARGEM
      )
   )
   
   # computando o valor com mais dígitos do rols, ou
   # o rótulo com mais letras.
   mc1 = max(len(str(v)) for v in coluna1.rol_iter())
   mc2 = max(len(str(v)) for v in coluna2.rol_iter())
   mc1 = max(len(rotulo1), mc1)
   mc2 = max(len(rotulo2), mc2)
   
   # adição da margem do valor à borda
   # da tabela.
   adicao = len(MARGEM)
   while maior_qtd != 0:
      linha = BARRA
      try:
         celula = str(next(i2))
         linha += (
            MARGEM + 
            equilibra_str(celula, mc2) + 
            MARGEM + BARRA
         )
      except StopIteration:
         linha += (
            MARGEM + equilibra_str(TRACOS, mc2) 
            + MARGEM + BARRA
         )
      ...
      try:
         celula = str(next(i1))
         linha += (
            MARGEM + equilibra_str(celula, mc1) 
            + MARGEM + BARRA
         )
      except StopIteration:
         linha += (
            MARGEM + equilibra_str(TRACOS, mc1) 
            + MARGEM + BARRA
         )
      ...
      linhas.append(linha)
      maior_qtd -= 1
      del linha
   ...

   return linhas
...

# cria barras superiores, inferiores e centrais.
def tampa_tabela(linhas):
   # largura máxima da tabela.
   comprimento = len(linhas[0])
   # demilitador baseado na largura da tabela.
   barra = BARRA * comprimento
   # para computar a próxima inclusão
   # na próxima linha de cédulas.
   qtd = 0

   for indice in range(len(linhas) + 1):
      linhas.insert(indice + qtd, barra)
      qtd += 1
   ...
...

def otimiza_uso_de_tela(linhas):
   largura = get_terminal_size().columns
   # largura da tabela.
   lT = len(linhas[0])
   # espaço entre as tabelas concatenadas.
   afastamento = ESPACO * 3
   # quantas tabelas cabem dado a largura
   # do terminal. Uma divisão simples entre
   # a "largura do terminal" divido pela
   # da tabela mais o espaçamento entre 
   # elas.
   n = largura // (lT + len(afastamento))
   # altura das tabelas. Pode ser qualquer
   # valor, já que não seria fixo na impressão.
   aT= len(linhas) // n
   # fila para reter fatias e concatena-las
   # baseado na primeira retida.
   fila_de_fatias = []
   # uma lista, onde as strings que formam
   # a tabela(chamadas linhas aqui) são
   # adicionandas após removidas das demais.
   fatia = []

   # fatia igualmente as linhas passadas e
   # guarda tais fatias para anexação posteriore.
   for k in range(1, len(linhas)+1):
      if k % aT == 0:
         tampa_tabela(fatia)
         fila_de_fatias.append(fatia[:])
         fatia.clear()
      else:
         fatia.append(linhas.pop(0))
      ...
   ...

   # limpa para reutilização da referência.
   linhas.clear()
   # a primeira "fatia" é que junta tudo.
   remocao = fila_de_fatias.pop(0)
   linhas.extend(remocao)
   while len(fila_de_fatias) > 0:
      fatia_removida = fila_de_fatias.pop(0)
      indice = 0
      while len(fatia_removida) > 0:
         linha = fatia_removida.pop(0)
         linhas[indice] = (
            linhas[indice] +
            afastamento
            + linha
         )
         indice += 1
      ...
   ...
...

from texto import MatrizTexto
# cantos da tabela.
(CSE, CSD, CID, CIE) = ('\u256D', '\u256E', '\u256F', '\u2570')
(BARRA_V, BARRA_H) = ('\u2502','\u2500')
BARRA_CRUZ = '\u253c'


class TabelaStrMatriz(MatrizTexto):
   def __init__(self, tabela_str):
      largura = tabela_str.find('\n') + 1
      altura =  sum(
         1 if char == '\n' else 0
         for char in tabela_str
      ) 
      altura = len(tabela_str.split('\n'))
      super().__init__(altura, largura-1)
      k = 0
      for (y, linha) in enumerate(tabela_str.split('\n')):
         for (x, char) in enumerate(linha):
            self.altera(y % altura, x % largura, char)
         ...
      ...
   ...

   @staticmethod
   def to_matriz(tabela_str):
      # só aceita strings.
      if type(tabela_str) != str:
         raise TypeError()

      for y in range(altura):
         for x in range(largura):
            char = tabela_str[k]
            if char != '\n':
               matriz[y][x] = char
            k += 1
         ...
      ...
      return (matriz, (altura, largura))
   ...

   def __repr__(self):
      caracteres = []
      for linha in self._linhas:
         for char in linha:
            caracteres.append(char)
         caracteres.append('\n')
      ...
      return "".join(caracteres)
   ...
...


# acha colunas e linhas que são homogêneas,
# na verdade, apenas parecidas com a barra.
# Retorna um iterador com as posições de
# colunas.
def acha_colunas(ts):
   (altura, largura) = ts.dimensao()
   lista_de_posicoes = []

   for x in range(1, largura-1):
      for y in range(1, altura-1):
         e_barra_vertical = (
            ts[y][x] == BARRA and 
            ts[y][x-1] == MARGEM and
            ts[y][x+1] == MARGEM 
         )
         if e_barra_vertical:
            info = (y, x, BARRA_V)
            lista_de_posicoes.append(info)
         ...
      ...
   ...
   # caso especias da primeira e última borda.
   for y in range(1, altura-1):
      limite_esquerdo = (
         ts[y][0] == BARRA and
         ts[y][1] == MARGEM
      )
      limite_direito = (
         ts[y][largura-1] == BARRA and
         ts[y][largura-2].isspace()
      )
      if limite_esquerdo: 
         lista_de_posicoes.append((y, 0, BARRA_V))

      if limite_direito:
         lista_de_posicoes.append((y, largura-1, BARRA_V))
   ...

   return lista_de_posicoes 
...

def acha_linhas(tabela_str):
   (altura, largura) = tabela_str.dimensao()
   # primeira as colunas
   percentual = 0.0
   for y in range(altura):
      for x in range(largura):
         char = tabela_str[y][x]
         if char == BARRA:
            percentual += 1.0/float(largura)
      else:
         if 0.7 <= percentual  <= 1:
            yield(y)
      ...
      percentual = 0
   ...
...

def acha_cruzilhadas(ts):
   (altura, largura) = ts.dimensao()
   lista_de_posicoes = []
   for x in range(1,largura-1):
      for y in range(1, altura-1):
         uma_cruz_valida = (
            ts[y-1][x] == ts[y+1][x] 
                  ==
            ts[y][x+1] == ts[y][x-1]
                  == 
                BARRA 
         ) 
         if uma_cruz_valida:
            lista_de_posicoes.append((y, x, BARRA_CRUZ))
      ...
   ...
   return lista_de_posicoes
...

def acha_cantos(ts):
   (altura, largura) = ts.dimensao()
   # lista de posições.
   lista = []

   # vai do segundo caractére ao penúltimo
   # já que os cantos são adicionados sem
   # qualquer iteração.
   for x in range(1, largura-2):
      L_invertido_esquerda = (
         ts[0][x] == '#' and
         ts[0][x-1] == '#' and
         ts[1][x] and 
         ts[0][x + 1] == ESPACO
      )

      L_invertido_direita = (
         ts[0][x] == '#' and
         ts[1][x] == '#' and
         ts[0][x+1] == '#' and
         ts[0][x-1] == ESPACO
      )

      L_direita = (
         ts[altura-1][x] == '#' and
         ts[altura-1][x+1] == '#' and
         ts[altura-2][x] == '#' and
         ts[altura-1][x-1] == ESPACO
      )

      L_esquerda = (
         ts[altura-1][x] == '#' and
         ts[altura-1][x-1] == '#' and
         ts[altura-2][x] == '#' and
         ts[altura-1][x+1] == ESPACO
      )

      # a posição e o caractére que têm
      # que trocar.
      if L_invertido_direita:
         lista.append((0, x, CSE))
      elif L_invertido_esquerda:
         lista.append((0, x, CSD))

      if L_direita:
         lista.append((altura-1, x, CIE))
      elif L_esquerda:
         lista.append((altura-1, x, CID))
   ...

   # inserções de todos cantos no 
   # sentido horário.
   lista.append((0, 0, CSE))
   lista.append((0, largura-1, CSD))
   lista.append((altura-1, largura-1, CID))
   lista.append((altura-1, 0, CIE))
   return lista
...

def reveste(tabela_str):
   if type(tabela_str) != TabelaStrMatriz:
      raise TypeError()

   posicoes = [
      acha_cantos(tabela_str),
      acha_colunas(tabela_str),
      acha_cruzilhadas(tabela_str)
   ]

   for iterador in posicoes:
      esta_vazio = len(iterador) == 0
      while (not esta_vazio):
         (y, x, char) = iterador.pop()
         tabela_str.altera(y, x, char)
         # atualizando valor lógico ...
         esta_vazio = len(iterador) == 0
      ...
   ...
   return str(tabela_str)
...


# testes unitários:
if __name__ == "__main__":
   from testes import executa_teste
   from random import randint, choice

   # dados comuns:
   coluna1 = Coluna("gênero", ['M', 'F', 'F', 'F', 'M'])
   coluna2 = Coluna("idade", [14, 27, 38, 13, 51, 24])

   def imprime(array):
      print("\n".join(array), end="\n\n")

   def testa_funcao_cria_tabela():
      esboco = aglomera_colunas(coluna1, coluna2)
      imprime(esboco)
   ...

   def teste_de_funcao_tampa_tabela():
      linhas_esboco = aglomera_colunas(coluna2, coluna1)
      tampa_tabela(linhas_esboco)
      imprime(linhas_esboco)
   ...

   def testa_funcao_ct_dobradura():
      rol = list(choice(['F', 'M']) for _ in range(132))
      coluna1 = Coluna("gênero", rol)
      rol = list(randint(5, 100) for _ in range(129))
      coluna2 = Coluna("idade", rol)
      esboco_inicial = aglomera_colunas(coluna1, coluna2)
      otimiza_uso_de_tela(esboco_inicial)
      imprime(esboco_inicial)
   ...

   def testa_funcao_reveste():
      rol = list(choice(['F', 'M']) for _ in range(132))
      coluna1 = Coluna("gênero", rol)
      rol = list(randint(5, 100) for _ in range(129))
      coluna2 = Coluna("idade", rol)
      esboco_inicial = aglomera_colunas(coluna1, coluna2)
      otimiza_uso_de_tela(esboco_inicial)
      esboco = "\n".join(esboco_inicial)
      print(reveste(TabelaStrMatriz(esboco)))
   ...

   executa_teste(testa_funcao_cria_tabela)
   executa_teste(teste_de_funcao_tampa_tabela)
   executa_teste(testa_funcao_ct_dobradura)
   executa_teste(testa_funcao_reveste)
...
