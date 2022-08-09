
"""
Transferindo utilitários para cá, já que 
o código transcendeu as 400 linhas. Aqui
ficará as funções e procedimentos, assim 
como classes e demais relacionados, ao 
revestimento da tabela com caractéres Unicode.
"""

# próprios módulos:
from texto import MatrizTexto
from tabelas_variaveis import *

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

def acha_linhas(ts):
   (altura, largura) = ts.dimensao()
   lista_de_posicoes = [(0, 1, BARRA_H)]

   # primeira as colunas
   for y in range(1, altura-1):
      for x in range(1, largura-1):
         e_uma_borda = (
            ts[y][x] == BARRA and
            ts[y][x-1] == BARRA and 
            ts[y][x+1] == BARRA and
            ts[y-1][x] != BARRA and
            ts[y+1][x] != BARRA
         )
         if e_uma_borda:
            lista_de_posicoes.append((y, x, BARRA_H))
      ...
   ...
   # tratando de casos especiais.
   for x in range(1, largura-1):
      # cuidando das barras horizontais
      # na parte inferior.
      positivo_superior = (
         ts[0][x] == BARRA and
         ts[1][x] != BARRA and
         ts[y][x-1] == ts[y][x+1] == BARRA
      )
      if positivo_superior:
         lista_de_posicoes.append((0, x, BARRA_H))
      # agora a parte inferior.
      y = altura-1
      positivo_inferior = (
         ts[y][x] == BARRA and
         ts[y-1][x] != BARRA and
         ts[y][x-1] == ts[y][x+1] == BARRA
      )
      if positivo_inferior:
         lista_de_posicoes.append((y, x, BARRA_H))

   return lista_de_posicoes
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
                BARRA == ts[y][x]
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

def acha_os_tes(ts):
   (altura, largura) = ts.dimensao()
   lista_de_posicoes = []

   for y in range(1, altura-1):
      for x in range(1, largura-1):
         t_deitado_direita = (
            ts[y][x] == BARRA and 
            ts[y][x-1] == BARRA and 
            ts[y][x+1] == MARGEM and
            ts[y-1][x] == BARRA and 
            ts[y+1][x] == BARRA
         )
         if t_deitado_direita:
            lista_de_posicoes.append((y, x, BARRA_T_DIREITA))

         t_deitado_a_esquerda = (
            ts[y][x] == BARRA and 
            ts[y][x-1] == MARGEM and 
            ts[y][x+1] == BARRA and
            ts[y-1][x] == BARRA and 
            ts[y+1][x] == BARRA
         )
         
         if t_deitado_a_esquerda:
            lista_de_posicoes.append((y, x, BARRA_T_ESQUERDA))
      ...
   ...
   # tratando de casos especiais.
   for x in range(1, largura-1):
      y = 0
      alvo_iii = (
         ts[y][x] == BARRA and 
         ts[y][x+1] == BARRA and 
         ts[y][x-1] == BARRA and 
         ts[y+1][x] == BARRA
      )
      if alvo_iii:
         lista_de_posicoes.append((y, x, BARRA_T))
      y = altura-1
      alvo_iv = (
         ts[y][x] == BARRA and 
         ts[y][x-1] == BARRA and 
         ts[y][x+1] == BARRA and 
         ts[y-1][x] == BARRA
      )
      
      if alvo_iv:
         lista_de_posicoes.append((y, x, BARRA_T_INVERTIDO))
   ...
   # agora nas laterais.
   for y in range(1, altura-1):
      x = 0
      alvo = (
         ts[y][x] == BARRA and 
         ts[y][x+1] == BARRA and
         ts[y+1][x] == BARRA and 
         ts[y-1][x] == BARRA
      )
      if alvo:
         lista_de_posicoes.append((y, x, BARRA_T_ESQUERDA))

      x = largura - 1
      outro_alvo = (
         ts[y][x] == BARRA and 
         ts[y][x-1] == BARRA and 
         ts[y+1][x] == BARRA and 
         ts[y-1][x] == BARRA
      )
      if outro_alvo:
         lista_de_posicoes.append((y, x, BARRA_T_DIREITA))
   ...

   return lista_de_posicoes
...


def reveste(tabela_str):
   if type(tabela_str) != TabelaStrMatriz:
      raise TypeError()

   posicoes = [
      acha_cantos(tabela_str),
      acha_colunas(tabela_str),
      acha_cruzilhadas(tabela_str), 
      acha_linhas(tabela_str),
      acha_os_tes(tabela_str)
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