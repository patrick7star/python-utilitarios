"""
produz uma árvore, ramificando diretórios e arquivos
de alguma diretório passado como argumento.
"""


# biblioteca do Python:
import os.path, os, sys, enum
from os import listdir
from os.path import (
   basename, join, realpath,
   isdir, isfile, abspath
)

# abre arquivo temporário para
# escreva trilha de espaços, não vai
# ser "acumulada" numa string, pois
# a função é recursiva.
trilha = []
vazio = ' '
galho = "\u0b72\u07fa\u07fa" # modelo 1
#galho = "\u0582\u07fa\u07fa" # modelo 2

# símbolos que representa dos galhos:
galho_v = galho[0]
galho_h = galho[1]

# novos galhos:
galhoH = "\u2501"  # novo design do traço horizontal.
galhoV = "\u2503"  # novo design do traço vertical.
galhoVH = "\u2517" # traço vertical-horizontal.
galhoVHV = "\u2523" # traço vertical-horizonta-vertical.


# enum para personalizar os tipos de galhos a usar.
class GalhoTipo(enum.Enum):
   GROSSO = enum.auto()
   FINO = enum.auto()
...

# transforma string formatada numa matriz,
# tomada suas dimensões e, supondo que seja
# "multi-linha".
def matriciar_string(string):
   linhas = string.split('\n')
   # calculando um número fixo para todas colunas.
   colunas = max([len(s) for s in linhas])
   matriz = [list(s) for s in linhas]
   # consertando matriz, expandindo até o número fixo de colunas.
   for i in range(len(matriz)):
      linha = matriz[i] # endreço para linha da matriz.
      # verifica se têm o máximo de colunas,
      # se não tiver, então será completado com "espaços".
      if len(linha) < colunas:
         diferenca = abs(colunas-len(linha))
         matriz[i] += list('¨' * diferenca)
      ...
   ...
   return matriz
...

# imprime uma matriz.
def imprime_matriz(matriz):
   (m, n) = (len(matriz), len(matriz[0]))
   print('*' * (n+4))
   for i in range(m):
      print('* ',end='')
      for j in range(n):
         print(matriz[i][j],end='')
      print(' *')
   ...
   print('*' * (n+4))
...

def escrevendo_trilha(caminho):
   """
   escreve a trilha dado o caminho.
   a função tem sua variável de estado.
   """
   # váriavel global para transportar concatenação a outras funções.
   global trilha
   if isdir(caminho):
      # lista contendo diretórios e arquivos.
      conteudo = listdir(caminho)
      # raíz dos arquivos listados.
      recuo = escrevendo_trilha.p * ' '
      raiz = basename(caminho) + ':'

      # só aciona uma única vez, para atender o caso
      # da raíz principal, de onde "brotem os galhos".
      if not escrevendo_trilha.raiz:
         trilha.append(raiz + '\n')
         escrevendo_trilha.raiz = True
      else:
         trilha.append('{}{} {}\n'.format(recuo, galho, raiz))
      for pth in conteudo:
         novo_caminho = join(caminho,pth)
         escrevendo_trilha.p += 3 # entra no diretório...
         escrevendo_trilha(join(novo_caminho))
         escrevendo_trilha.p -= 3 # sai do diretório...
      ...
   else:
      if isfile(caminho):
         # comprime strings longas.
         def comprime_str(string):
            if len(string) > 40:
               return string[0:25] + ' \u2d48 ' + string[-5::1]
            else: return string
         ...
         str = comprime_str(basename(caminho))
         recuo = (escrevendo_trilha.p) * ' '
         trilha.append("{}{} \"{}\"\n".format(recuo, galho,str))
      ...
   ...
...

def escreve_trilha_dirs(caminho):
   """
   faz uma trilha, atravesando os subdiretórios, porém
   ramifica apenas os diretórios.
   """
   # conserta sintaxe do caminho.
   caminho = realpath(caminho)
   global trilha
   # função utilitaria:
   def reduz_nome(string):
      if len(string) > 25:
         return string[0:8] + ' \u2d48 ' + string[-1:-5:-1]
      else: return string
   ...

   # imprime caminho, dependendo se é raíz ou subdiretório.
   if not escreve_trilha_dirs.e_raiz:
      trilha.append(basename(caminho) + ':\n')
      escreve_trilha_dirs.e_raiz = True
   else:
      # calcula o recuo baseado da profundidade.
      recuo = ' ' * escreve_trilha_dirs.p
      nome = reduz_nome(basename(caminho))
      trilha.append("{}{} {}:\n".format(recuo,galho, nome))
   ...

   # lista contendo diretórios.
   subdirs = [
      join(caminho, d)
      for d in listdir(caminho)
      if isdir(join(caminho,d))
   ]
   for sb in subdirs:
      escreve_trilha_dirs.p += 3
      escreve_trilha_dirs(sb)
      escreve_trilha_dirs.p -= 3
   ...
...

# o algoritmo segue-se deste modo:
# analisa coluna por coluna.
# registras as falhas, naquelas colunas que contém linhas verticas.
# sobreescreve tais falhas.
def conserta_arvore(matriz_arvore):
   coords = []
   linhas, colunas = len(matriz_arvore), len(matriz_arvore[0])
   ma = matriz_arvore # referência a matriz.
   for j in range(colunas):
      ha_linha = False
      nao_esta_entre = False
      for i in range(linhas):
         if ma[i][j] ==galho_v:
            ha_linha = True
         if ha_linha and ma[i][j].isspace():
            coords.append((i,j))
      ...
   ...
   # preenchendo espaços em branco.
   for (i,j) in coords: ma[i][j] = galho_v
   #imprime_matriz(matriz_arvore)
   # consertando última linha:
   ha_linha, n, m = False, colunas, linhas
   for j in range(n):
      caractere_i = ma[m-2][j]
      if caractere_i == galho_v: ha_linha = True
      if caractere_i.isspace() and ha_linha:
         ma[m-2][j] = galho_h
   ...
   for i in range(m):
      for j in range(n):
         if ma[i][j] == '\"' and matriz_arvore[i][j-1] ==galho_v:
            ma[i][j-1]= ' '
         if (ma[i][j] == galho_v and
             ma[i][j+1].isascii() and
             ma[i][j-1] == galho_h):
               ma[i][j] = ' '
      ...
   ...

# retorna árvore de diretório/arquivos de determinado
# caminho.
def esboco(caminho, mostra_arquivos=False):
   """
   escreve na string global a trilha de diretórios,
   subdiretórios e arquivos; mostrar os arquivos vem
   habilitado por padrão, porém pode ser desativado, e
   a trilha apresenta apenas diretórios.
   """
   global trilha,trilha_temp

   if mostra_arquivos:
      escreve_trilha_dirs.p = 0
      escreve_trilha_dirs.e_raiz = False
      escreve_trilha_dirs(caminho)
   else:
      escrevendo_trilha.p = 0 #inicializando em zero.
      escrevendo_trilha.raiz = False
      escrevendo_trilha(caminho)
   ...
   trilha_feita = "".join(trilha)
   # zerando trilha para próxima chamada.
   trilha.clear()

   return trilha_feita
...

# transforma uma matriz numa string, supondo
# que cada linha dela é uma linha, ou seja,
# adiciona quebra de linha.
def matriz_para_string(matriz):
   # dimensões da matriz.
   m,n = len(matriz), len(matriz[0])
   # "apaga" caractéres oculpadores de espaços da função "matriciar..."
   for i in range(m):
      for j in range(n):
         if matriz[i][j] == '¨':
            matriz[i][j]=' '
      ...
   ...
   # transforma numa string novamente.
   s = ""
   for linha in matriz:
      for celula in linha:
         s += celula
      s += '\n'
   ...
   return s
...

def arvore(caminho, mostra_arquivos=False):
   """
   transforma o resultado da função padrão
   numa matriz.
   """
   caminho = os.path.normpath(caminho)
   matriz_tree = matriciar_string(esboco(caminho, mostra_arquivos))
   conserta_arvore(matriz_tree) # aplica a correção de galhos.
   # troca e conecta galhos:
   reveste(matriz_tree)
   # tira galhos gerados por falha no algoritmo.
   remove_excesso(matriz_tree)
   # transforma numa string novamente.
   return matriz_para_string(matriz_tree)
...

def reveste(matriz):
   """
   faz o mesmo que o anterior, porém com galhos
   representando caractéres mais bonitos.
   """
   # dimensão da matriz:
   (L,C) = len(matriz),len(matriz[0])

   # reformando árvore:
   for i in range(L):
      for j in range(C):
         try:
            # proposições:
            # galho que conecta dois verticas
            # e há horizontais no meio:
            p1 = matriz[i][j] == galho_v
            p2 = matriz[i+1][j] == galho_v
            p3 = matriz[i][j+1] == matriz[i][j+2] == galho_h

            # fim de árvore, conecta a última sub-árvore:
            q1 = matriz[i][j] == galho_v
            q2 = matriz[i][j+1]==matriz[i][j+2] == galho_h
            q3 = matriz[i-1] == galho_v or matriz[i+1][j] == galhoVHV

            # galhos soltos indivídualmente, só contectam;
            # não ramíficam em sub-árvores:
            r1 = matriz[i][j] == galho_v
            r2 = (matriz[i+1][j] == galho_v or
                  matriz[i+1][j] == galhoVHV or
                  matriz[i+1][j] == galhoVH or
                  matriz[i+1][j].isascii())
            r3 = matriz[i-1][j]==galho_v or matriz[i-1][j] == galhoVHV

            if p1 and p2 and p3:
               matriz[i][j] = galhoVHV
               matriz[i][j+1] = galhoH
               matriz[i][j+2] = galhoH
            elif q1 and q2:
               matriz[i][j] = galhoVH
               matriz[i][j+1] = galhoH
               matriz[i][j+2] = galhoH
            elif r1 and r2:
               matriz[i][j] = galhoV

         except IndexError:
            # em caso de erro de indexação apenas
            # ignore, talvez não seja o caractére/
            # posicão que quero.
            pass
   return matriz_para_string(matriz)

def remove_excesso(matriz_arv):
   "mesmo resultado que árvore anteriores, porém algoritmo diferente"
   # dimensão da matriz.
   y_max, x_max = len(matriz_arv), len(matriz_arv[0])

   for l in range(y_max):
      for c in range(x_max):
         try:
            caso1 = (
               matriz_arv[l][c] == galhoV and
               matriz_arv[l+1][c].isspace() and
               matriz_arv[l+1][c-1] == galhoH and
               (matriz_arv[l+1][c+1].isalnum() or
               matriz_arv[l+1][c+1] == '\"') and
               (matriz_arv[l-1][c] == galhoVHV or
               matriz_arv[l-1][c] == galhoV)
            )

            caso2 = (
               matriz_arv[l][c] == galhoH and
               matriz_arv[l][c-1] == galhoH and
               matriz_arv[l][c+1] == galhoVH and
               matriz_arv[l][c+2] == galhoH
            )
         except IndexError:
            pass
         else:
            if caso2:
               (y, x) = l, c
               matriz_arv[y][x] = vazio
               x -= 1
               matriz_arv[y][x] = vazio
               x -= 1
               while matriz_arv[y][x] != galhoVHV:
                  matriz_arv[y][x] = vazio
                  y -= 1
               matriz_arv[y][x] = galhoVH

            if caso1:
               (y, x) = l, c
               while matriz_arv[y][x] != galhoVHV:
                  matriz_arv[y][x] = vazio
                  y -=1
               matriz_arv[y][x] = galhoVH
      ...
   ...
...

def alterna_galho(glh):
   " altera o tipo de galho global baseado no desejado"
   # galhos globais "escoporados".
   global galhoVH, galhoVHV, galhoH, galhoV

   if glh ==  GalhoTipo.GROSSO:
      galhoH = "\u2501"
      galhoV = "\u2503"
      galhoVH = "\u2517"
      galhoVHV = "\u2523"

   elif glh == GalhoTipo.FINO:
      galhoH = "\u2500"
      galhoV = "\u2502"
      galhoVH = "\u2570"
      galhoVHV = "\u251c"
   pass
...

# o que pode ser importado.
__all__ = [
   "GalhoTipo", "arvore", 
   "alterna_galho", "matriciar_string"
]


# teste protótipos:
if __name__ == "__main__":
   if sys.platform == "linux":
      nucleo = os.getenv("HOME")+"/Documents"
      caminho = nucleo + '/códigos/numeros_primos_gerados/'
      print(esboco(caminho))
      print(esboco(caminho, True))

      # provavelmente funciona na maioria dos 
      # linux, definido em língua-inglesa.
      caminho = os.getenv("HOME") + '/Pictures'
      print(esboco(caminho))
      print(esboco(caminho, True))
   ...
...
