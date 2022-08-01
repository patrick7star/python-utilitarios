"""
produz uma árvore, ramificando diretórios e arquivos
de alguma diretório passado como argumento.
"""


# biblioteca do Python:
import os, sys, enum
from os import listdir
from array import array
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

# comprime strings longas.
def comprime_str(string):
   if len(string) > 40:
      return string[0:25] + ' \u2d48 ' + string[-5::1]
   else: 
      return string
...

# função utilitaria:
def reduz_nome(string):
   if len(string) > 25:
      return string[0:8] + ' \u2d48 ' + string[-1:-5:-1]
   else: return string
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
      recuo = escrevendo_trilha.p * '¨'
      #raiz = basename(caminho) + ':'
      raiz = basename(realpath(caminho))+':'

      if escrevendo_trilha.p == 0:
         trilha.append(raiz + "\n")
      else:
         trilha.append(
            "{0}{2} {1}\n".format(
               recuo,raiz, 
               galhoVH+galhoH
            )
         )
      for pth in conteudo:
         novo_caminho = join(caminho,pth)
         escrevendo_trilha.p += 3 # entra no diretório...
         escrevendo_trilha(join(novo_caminho))
         escrevendo_trilha.p -= 3 # sai do diretório...
      ...
   else:
      if isfile(caminho):
         str = comprime_str(basename(caminho))
         recuo = (escrevendo_trilha.p) * '¨'
         trilha.append(
            "{0}{2} \"{1}\"\n".format(
               recuo, str,
               galhoVH+galhoH
            )
         )
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

   # imprime caminho, dependendo se é raíz ou subdiretório.
   if not escreve_trilha_dirs.e_raiz:
      trilha.append(basename(caminho) + ':\n')
      escreve_trilha_dirs.e_raiz = True
   else:
      # calcula o recuo baseado da profundidade.
      recuo = '¨' * escreve_trilha_dirs.p
      nome = reduz_nome(basename(caminho))
      #trilha.append("{}{} {}:\n".format(recuo,galho, nome))
      trilha.append(
         "{0}{2} {1}\n".format(
            recuo, nome, 
            galhoVH+galhoH
         )
      )
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

# retorna árvore de diretório/arquivos de determinado
# caminho.
def esboco(caminho, mostra_arquivos=False):
   """
   escreve na string global a trilha de diretórios,
   subdiretórios e arquivos; mostrar os arquivos vem
   habilitado por padrão, porém pode ser desativado, e
   a trilha apresenta apenas diretórios.
   """
   global trilha

   if not mostra_arquivos:
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

class Matriz:
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
      self._celula = '¨'
      # criando linhas do "quadro".
      for l in trilha:
         colunas = array('u', l)
         self._linhas.append(colunas)
      ...
      # igualizando colunas ...
      for l in range(len(self._linhas)):
         while len(self._linhas[l]) < qtd_c:
            self._linhas[l].append(self._celula)
      ...
   ...
   def __str__(self):
      string = []
      for linha in self._linhas:
         for celula in linha:
            string.append(celula)
         string.append('\n')
      ...
      return "".join(string)
   ...
   def __repr__(self):
      return self.__str__()
   def __getitem__(self, linha_indice):
      return self._linhas[linha_indice]
   ...
   def __sizeof__(self):
      acumulado = sum(sys.getsizeof(s) for s in self._linhas)
      acumulado += sys.getsizeof(self._linhas)
      return acumulado + sys.getsizeof(self._celula)
   ...
   def __len__(self):
      return len(self._linhas)

   def remove_grade(self):
      for linha in self._linhas:
         for c in range(len(linha)):
            if linha[c] == '¨':
               linha[c] = ' '
         ...
      ...
   ...
...

def acha_galho_dobrado(linha):
   for indice in range(len(linha)):
      if linha[indice] == galhoVH:
         return indice
   ...
   return None
...

def conserta_galhos(matriz_arvore):
   qtd = len(matriz_arvore)
   for l in range(qtd-1,0,-1):
      # índice de um "galho-vertical-horizontal".
      c = acha_galho_dobrado(matriz_arvore[l])
      try:
         if c != None:
            # proposições:
            e_raiz_do_subdir = False
            e_vacuo = False
            e_conector = False

            while not e_raiz_do_subdir:
               # atualiza proposição.
               e_raiz_do_subdir = (
                  matriz_arvore[l-1][c].isalnum() or
                  matriz_arvore[l-1][c+1].isalnum() or
                  (matriz_arvore[l-1][c] == '_' and
                  matriz_arvore[l-1][c+1] == '_') or
                  matriz_arvore[l-1][c-1].isalnum() and
                  matriz_arvore[l-1][c-3] == galhoH and
                  ':' in matriz_arvore[l-1]
               )
               e_vacuo = (
                  matriz_arvore[l-1][c] == '¨' and
                  matriz_arvore[l-1][c+1] == '¨' and
                  matriz_arvore[l-1][c-1] == '¨'
               )
               e_conector = ( matriz_arvore[l-1][c] == galhoVH)
               # alteração do galho.
               if e_vacuo:
                  matriz_arvore[l-1][c] = galhoV
               elif e_conector:
                  matriz_arvore[l-1][c] = galhoVHV
               else:
                  pass
               # sobe uma posição.
               l -= 1
            ...
         ...
      except IndexError: pass
      ...
   ...
...

def arvore(caminho, mostra_arquivos=False,
tipo_de_galho=GalhoTipo.GROSSO):
   """
   transforma o resultado da função padrão
   numa matriz.
   """
   # alterando primeiramente o tipo de galho. Se
   # não for o grosso(padrão), então fazer alteração.
   if tipo_de_galho != GalhoTipo.GROSSO:
      alterna_galho(tipo_de_galho)
   # faz um esboço inicial da árvore.
   esboco_de_trilha = esboco(caminho, mostra_arquivos)
   # matricia.
   matriz_de_trilha = Matriz(esboco_de_trilha)
   # aplica a correção de galhos.
   conserta_galhos(matriz_de_trilha)
   # remove grade-pontilhada da matriz.
   matriz_de_trilha.remove_grade()
   # conversão de string é interna a classe.
   return str(matriz_de_trilha)
...

# altera o tipo de galho global baseado no desejado
def alterna_galho(glh):
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
   ...
...

def ramifica_caminho(caminho):
   """
   dado um caminho válido, ele pega cria a 
   arvore, sendo tal caminho existente ou 
   não, baseando apenas no caminho, espeficicando
   diretório e sub-diretórios.
   """
   dirs = caminho.split(os.sep)
   alterna_galho(GalhoTipo.FINO)
   # removendo todos espaços em branco.
   while dirs.count('') > 0:
      dirs.remove('')

   # primeiro ocorrência é diferente por 
   # não ter um recuo, portando o
   # dispessando.
   primeiro_nao_ocorreu = True
   # forma galho que todos irão usar.
   galho_completo = galhoVH + 2 * galhoH
   (linhas, recuo) = ([], 0)

   while len(dirs) > 0:
      remocao = dirs.pop(0)
      if primeiro_nao_ocorreu:
         print("%s:" % remocao)
         primeiro_nao_ocorreu = False
      else:
         vacuo = recuo * ' '
         linha = "{}{}{}:".format(vacuo, galho_completo, remocao)
         linhas.append(linha)
         recuo += 3
      ...
   ...
   # removendo os dois pontos do último, pois
   # pode não ser um diretório.
   linhas[-1] = linhas[-1][0:-1]
   return "\n".join(linhas)
...

# o que pode ser importado.
__all__ = ["GalhoTipo", "ramifica_caminho", "arvore"]


# teste protótipos:
if __name__ == "__main__":
   # módulos próprios:
   from testes import executa_teste 
   from os import getenv

   def testa_Matriz():
      caminho = ".."
      trilha_esboco = esboco(caminho)
      if __debug__:
         print(trilha_esboco)
      trilha_matriz = Matriz(trilha_esboco)
      print(trilha_matriz)
      print(trilha_matriz, end="\n")
      trilha_esboco = esboco(caminho, True)
      tm = Matriz(trilha_esboco)
      print(tm, end="\n")
      print(tm, end="\n\n")

      # provavelmente funciona na maioria dos 
      # linux, definido em língua-inglesa.
      caminho = os.getenv("HOME") + '/Pictures'
      te = esboco(caminho)
      tm = Matriz(te)
      print(tm, end="\n")
      te = esboco(caminho)
      tm = Matriz(te)
      print(tm, end="\n\n")
   ...

   def testa_conserta_galhos():
      te = esboco("../../", True)
      tm = Matriz(te)
      conserta_galhos(tm)
      tm.remove_grade()
      print(tm, end="\n\n")
      te = esboco("../../")
      tm = Matriz(te)
      conserta_galhos(tm)
      tm.remove_grade()
      print(tm, end="\n\n")
   ...

   def testa_arvore():
      tree = arvore("../../")
      print(tree)
      tree = arvore("../../", True, GalhoTipo.FINO)
      print(tree)
   ...

   def teste_de_ramifica_caminho():
      caminho = join(
         getenv("HOME"), 
         "pasta_vázia", "subdir_i",
         "outra_pasta", "arquivo.txt"
      )
      arv = ramifica_caminho(caminho)
      print(arv)
   ...

   # rodando testes ...
   executa_teste(
      testa_Matriz,
      testa_conserta_galhos,
      testa_arvore,
      teste_de_ramifica_caminho
   )
...
