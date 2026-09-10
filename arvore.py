"""
   Produz uma árvore, ramificando diretórios e arquivos de alguma diretório
 passado como argumento.
"""

# o que pode ser exportado.
__all__ = ["GalhoTipo", "ramifica_caminho", "arvore"]

# Biblioteca do Python:
import os, sys, enum
from os import listdir
from os.path import (basename, join, realpath, isdir, isfile, abspath)
from decimal import Decimal
from queue import SimpleQueue
from pathlib import Path
# Submódulos:
from .tree.grade import (Matriz)


# Acumulador de trilhas de strings:
trilha = []
# Recuo padrão na construção(para ser visível).
RECUO_SIMBOLO = '¨'
# Novos galhos:
GALHO_H     = "\u2501"  # novo design do traço horizontal.
GALHO_V     = "\u2503"  # novo design do traço vertical.
GALHO_VH    = "\u2517" # traço vertical-horizontal.
GALHO_VHV   = "\u2523" # traço vertical-horizonta-vertical.
# Margem de busca da matriz:
MARGEM_DE_VARREDURA = 1
MARGEM = MARGEM_DE_VARREDURA


class GalhoTipo(enum.Enum):
   "Enumerador para personalizar os tipos de galhos a usar."
   GROSSO = enum.auto()
   FINO = enum.auto()

def arvore(caminho, mostra_arquivos=False, tipo=GalhoTipo.FINO) -> str:
   """
   Pega caminho, varre todo ele se for um diretório, tanto subdiretórios
   como arquivos, tudo no formato de uma árvore. O retorno será uma string
   com toda uma formatação.
   """
   # Alterando primeiramente o tipo de galho. Se não for o grosso(padrão), 
   # então fazer alteração.
   if tipo != GalhoTipo.GROSSO:
      alterna_galho(tipo)

   visivel = mostra_arquivos
   # Faz um esboço inicial da árvore.
   esboco = cria_esboco(caminho, visivel)
   # Transforma array com linhas numa matriz.
   matriz = Matriz(esboco)
   # Aplica correção no desenho numa matriz.
   preenche_espacos_vazios(matriz)
   complementa_galhos_falhados(matriz)
   # Remove grade interna da matriz.
   matriz.remove_grade()

   # conversão de string é interna a classe.
   return str(matriz)

#+===============+================+==============+=============+============+
#                          Interface Privada
#+===============+================+==============+=============+============+
def alterna_galho(tipo) -> None:
   "Altera o tipo de galho global baseado no desejado."
   # Galhos globais "escoporados".
   global GALHO_VH, GALHO_VHV, GALHO_H, GALHO_V

   match tipo:
      case GalhoTipo.GROSSO:
         GALHO_H = "\u2501"
         GALHO_V = "\u2503"
         GALHO_VH = "\u2517"
         GALHO_VHV = "\u2523"
      case GalhoTipo.FINO:
         GALHO_H = "\u2500"
         GALHO_V = "\u2502"
         GALHO_VH = "\u2570"
         GALHO_VHV = "\u251c"
      case _:
         raise ValueError("tipo não existe!")

def ramifica_caminho(caminho):
   """
   Dado um caminho válido, ele pega cria a arvore, sendo tal caminho
   existente ou não, baseando apenas no caminho, espeficicando diretório e
   sub-diretórios.
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

# comprime strings longas.
def comprime_str(string):
   if len(string) > 40:
      return string[0:25] + ' \u2d48 ' + string[-5::1]
   else: 
      return string

def reduz_nome(string):
   if len(string) > 25:
      return string[0:8] + ' \u2d48 ' + string[-1:-5:-1]
   else: return string

def escrevendo_trilha(caminho: Path, trilha: SimpleQueue,
  profundidade: Decimal) -> None:
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

def escreve_trilha_dirs(path: Path, lines: SimpleQueue, depth: Decimal,
  is_root: Decimal) -> None:
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

def cria_esboco(caminho, mostra_arquivos=False):
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

   # Adicionando à raíz primeiramente ...
   raiz = path.absolute().name
   trilha.append(str(raiz))

   # Transferindo fila(na operação FIFO) para uma lista de formar a 
   # manter a compatibilidade.
   while (not fila.empty()):
      linha = fila.get()
      trilha.append(linha)

   trilha_feita = "".join(trilha)
   # zerando trilha para próxima chamada.
   trilha.clear()

   return trilha_feita

def acha_lacuna_na_arvore(In: Matriz, linha: int) -> int:
   "Retorna o índice da posição do caractére ou 'null' se não achou nada."
   matriz = In
   input_a = matriz[linha]
   ULTIMO = len(input_a)
   VACUO = RECUO_SIMBOLO

   for k in range(0, ULTIMO - MARGEM):
      m = linha - 1
      input_b = matriz[m][k]

      if input_a[k] == GALHO_VH and input_b == VACUO:
         return k
   return None

def preenche_espacos_vazios(Input: Matriz) -> None:
   output = Input
   qtd = len(Input)
   fim = (qtd - 1)
   VACUO = RECUO_SIMBOLO

   for linha in range(fim, MARGEM, -1):
      # índice de um "galho-vertical-horizontal".
      coluna = acha_lacuna_na_arvore(Input, linha)

      # Se não houver nesta linha, apenas pula para a próxima superior.
      if coluna is None: continue

      for l in range(linha - 1, MARGEM - 1, -1):
         if output[l][coluna] == GALHO_VH:
            break
         # Verifica se bate num galho dobrado.
         output[l][coluna] = GALHO_V
         # Sobe uma posição do galho encontrado.

def acha_falha_nos_galhos(In: Matriz, linha: int) -> int:
   "Retorna o índice da posição do caractére ou 'null' se não achou nada."
   matriz = In
   input_a = matriz[linha]
   ULTIMO = len(input_a)
   VACUO = RECUO_SIMBOLO

   for k in range(0, ULTIMO - MARGEM):
      inferior = input_a[k]
      superior = matriz[linha - 1][k]

      # Todas as configurações identificadas nas àrvores amostradas:
      configuracao_a = (inferior == GALHO_VH and superior == GALHO_VH)
      configuracao_b = (inferior == GALHO_V and superior == GALHO_VH)
      configuracao_c = (inferior == GALHO_VHV and superior == GALHO_VH)

      if  configuracao_a or configuracao_b or configuracao_c:
         return k
   return None

def complementa_galhos_falhados(Input: Matriz) -> None:
   """
   Depois de preencher vácuos com um galho reto, ainda é preciso alinhar 
   galhos destoantes um dos outros. Este aqui faz isso, conecta varios 
   tipos de falhas de galhos um no outro, num algoritmo parecido com o
   outro, porém, ele não itera vários depois de achado, apenas conserta
   o superior.
   """
   output = Input
   qtd = len(Input)
   fim = (qtd - 1)
   VACUO = RECUO_SIMBOLO

   for linha in range(fim, MARGEM - 1, -1):
      # índice de um "galho-vertical-horizontal".
      coluna = acha_falha_nos_galhos(Input, linha)

      # Se não houver nesta linha, apenas pula para a próxima superior.
      if coluna is None: continue

      # Verifica se bate num galho dobrado.
      output[linha - 1][coluna] = GALHO_VHV

#+===============+================+==============+=============+============+
#                          Testes Unitários
#+===============+================+==============+=============+============+
from unittest import (TestCase)

class FuncaoQueConstroiArvore(TestCase):
   def runTest(self):
      input = Path().absolute()
      output = arvore(input, True)
      print(output)

class PrototipoDaFuncaoArvore(TestCase):
   def runTest(self):
      raiz = Path()
      esboco = cria_esboco(raiz, True)
      matriz = Matriz(esboco)

      print("\nAntes de qualquer mudança:")
      print(matriz)

      preenche_espacos_vazios(matriz)
      complementa_galhos_falhados(matriz)

      print("\nApós preenchimento:")
      print(matriz)

      matriz.remove_grade()

class RamificacaoDesteDiretorio(TestCase):
   def runTest(self):
      raiz = Path()
      output = arvore(raiz, True)

      print(output)
