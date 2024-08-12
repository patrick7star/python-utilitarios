"""
Produz uma árvore, ramificando diretórios e arquivos de alguma diretório 
passado como argumento.
"""

# o que pode ser exportado.
__all__ = ["GalhoTipo", "ramifica_caminho", "arvore"]

# biblioteca do Python:
import os, sys, enum
from os import listdir
from array import array
from os.path import (
   basename, join, realpath,
   isdir, isfile, abspath
)
from decimal import Decimal
from queue import SimpleQueue
from pathlib import Path


# Acumulador de trilhas de strings:
trilha = []
# Recuo padrão na construção(para ser visível).
RECUO_SIMBOLO = '¨'

# novos galhos:
GALHO_H = "\u2501"  # novo design do traço horizontal.
GALHO_V = "\u2503"  # novo design do traço vertical.
GALHO_VH = "\u2517" # traço vertical-horizontal.
GALHO_VHV = "\u2523" # traço vertical-horizonta-vertical.


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

def escrevendo_trilha(caminho: Path, trilha: SimpleQueue, 
  profundidade: Decimal):
   """ Vai escrevendo trilhas, e colocando as na fila. """
   # Computando e formando recuo de cada subdir ou arquivo.
   qtd = int(profundidade) * 3
   recuo = qtd * RECUO_SIMBOLO

   # váriavel global para transportar concatenação a outras funções.
   if caminho.is_dir():
      # lista contendo diretórios e arquivos.
      conteudo = listdir(caminho)
      # raíz dos arquivos listados.
      raiz = str(caminho.name) + ':'

      if profundidade.is_zero():
         fmt = str(raiz) + "\n"
         trilha.put(fmt)
      else:
         fmt = "{0}{2} {1}\n".format(recuo, raiz, GALHO_VH + GALHO_H)
         trilha.put(fmt)

      for path in conteudo:
         novo_caminho = caminho.joinpath(path)
         profundidade += Decimal(1) 
         escrevendo_trilha(novo_caminho, trilha, profundidade)
         profundidade -= Decimal(1)
      ...
   else:
      if caminho.is_file():
         _str = comprime_str(str(caminho.name))
         fmt = "{0}{2} \"{1}\"\n".format(recuo, _str, GALHO_VH+GALHO_H)
      else:
         trilha.put(
            "{0}{2} \"{1}\"(desconhecido)\n"
            .format(recuo, _str, GALHO_VH+GALHO_H)
         )
      trilha.put(fmt)
      ...
   ...
...

def escreve_trilha_dirs(path: Path, lines: SimpleQueue, depth: Decimal,
  is_root: Decimal):
   """
   Faz uma trilha, atravesando os subdiretórios, porém ramifica apenas os 
   diretórios, ou seja, os arquivos são ocultados.
   """
   # imprime caminho, dependendo se é raíz ou subdiretório.
   if is_root.is_zero():
      lines.put(str(path.name) + ":\n")
      is_root += 1
   else:
      # calcula o recuo baseado da profundidade.
      recuo = RECUO_SIMBOLO * int(depth)
      nome = reduz_nome(str(path.name))

      lines.put("{0}{2} {1}\n".format( recuo, nome, GALHO_VH + GALHO_H))
   ...

   # lista contendo diretórios.
   subdiretorios = [d for d in path.iterdir() if d.is_dir()]

   for sb in subdiretorios:
      depth += 3
      escreve_trilha_dirs(sb, lines, depth, is_root)
      depth -= 3
   ...
...

def esboco(caminho, mostra_arquivos=False):
   """
   Escreve na string global a trilha de diretórios, subdiretórios e 
   arquivos; mostrar os arquivos vem habilitado por padrão, porém pode ser 
   desativado, e a trilha apresenta apenas diretórios.
   """
   trilha = [] # Permite tal função ser Thread-Safe.
   # Parâmetros comuns entre as chamadas:
   path = Path(caminho)
   depth = Decimal(0)
   fila = SimpleQueue()
   
   if (not mostra_arquivos):
      raiz_count = Decimal(0)
      escreve_trilha_dirs(path, fila, depth, raiz_count)
   else:
      escrevendo_trilha(path, fila, depth)

   ...
   # Transferindo fila(na operação FIFO) para uma lista de formar a 
   # manter a compatibilidade.
   while (not fila.empty()):
      linha = fila.get()
      trilha.append(linha)
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
      if linha[indice] == GALHO_VH:
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
                  matriz_arvore[l-1][c-3] == GALHO_H and
                  ':' in matriz_arvore[l-1]
               )
               e_vacuo = (
                  matriz_arvore[l-1][c] == '¨' and
                  matriz_arvore[l-1][c+1] == '¨' and
                  matriz_arvore[l-1][c-1] == '¨'
               )
               e_conector = ( matriz_arvore[l-1][c] == GALHO_VH)
               # alteração do galho.
               if e_vacuo:
                  matriz_arvore[l-1][c] = galhoV
               elif e_conector:
                  matriz_arvore[l-1][c] = GALHO_VHV
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

def arvore(caminho, mostra_arquivos=False, tipo_de_galho=GalhoTipo.GROSSO):
   """
   Transforma o resultado da função padrão numa matriz.
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
   global GALHO_VH, GALHO_VHV, GALHO_H, galhoV

   if glh ==  GalhoTipo.GROSSO:
      GALHO_H = "\u2501"
      galhoV = "\u2503"
      GALHO_VH = "\u2517"
      GALHO_VHV = "\u2523"
   elif glh == GalhoTipo.FINO:
      GALHO_H = "\u2500"
      galhoV = "\u2502"
      GALHO_VH = "\u2570"
      GALHO_VHV = "\u251c"
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
   galho_completo = GALHO_VH + 2 * GALHO_H
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


# teste protótipos:
if __name__ == "__main__":
   # módulos próprios:
   from unittest import FunctionTestCase
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

   def novo_design_da_formacao_de_trilha():
      path = Path("../../python-utilitarios")
      depth = Decimal(0)
      F = SimpleQueue()

      print(path)
      print(depth)
      print(F)

      rascunho = escrevendo_trilha(path, F, depth)
      print("Total de linhas: %d" % F.qsize())
   ...

   def esboco_desta_biblioteca():
      caminho = "../../python-utilitarios"
      print("caminho: '%s'" % caminho)
      meu_esboco = esboco(caminho, True)
      print("Esboço feito:\n", meu_esboco)
   ...

   def formacao_de_arvore_desta_biblioteca():
      caminho = "../../python-utilitarios"
      tree_fmt_only_dirs = arvore(caminho, False, GalhoTipo.FINO)
      tree_fmt = arvore(caminho, True, GalhoTipo.FINO)

      print(tree_fmt_only_dirs)
      print(tree_fmt)
   ...

   testes_unitarios = [
      FunctionTestCase(testa_Matriz),
      FunctionTestCase(testa_conserta_galhos),
      FunctionTestCase(teste_de_ramifica_caminho),
      FunctionTestCase(testa_arvore),
      FunctionTestCase(novo_design_da_formacao_de_trilha),
      FunctionTestCase(esboco_desta_biblioteca),
      FunctionTestCase(formacao_de_arvore_desta_biblioteca)
   ]

   for (n, teste) in enumerate(testes_unitarios):
      print ("\n{}º teste:".format(n + 1))
      teste.run()
...
