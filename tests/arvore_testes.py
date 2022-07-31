#!/usr/bin/python3 -O

# biblioteca padrão do Python:
import os, sys, time
from math import floor
from timeit import timeit
# importando módulos a testar:
from biblioteca import alterna_galho, GalhoTipo, arvore, arvore_ii

"""
o teste abaixo funciona apenas em
plataforma linux; e se tiver os
diretórios/sub-diretórios explicitados.
"""

def testa_arvore_i():
   """
   testando protótipos de funções que funcionam
   apenas no módulo, e não podem ser importados
   para não ficar entulhando tudo que já tem.
   """
   print("esboço em como foi construído o projeto:")
   no_modulo = os.system("/usr/bin/python3 -B ../src/arvore.py")
   # tempo para visualizar o resultado.
   if __debug__:
      time.sleep(5)

   # mudando expessura do galho.
   alterna_galho(GalhoTipo.FINO)

   nucleo = os.getenv("HOME") + "/Documents"

   caminho = nucleo + '/códigos'
   print(arvore(caminho))
   print(arvore(caminho, True))
...

def testa_arvore_ii():
   nucleo = os.getenv("HOME") + "/Documents"

   caminho = nucleo + '/códigos'
   # testando novo código otimizado.
   print(arvore_ii.arvore(caminho))
   print(arvore_ii.arvore(caminho, True, arvore_ii.GalhoTipo.FINO))
...

# funções utilitarios de BDA:
def ordem_info(f1, t1, f2, t2):
   f1_mais_rapida = False 
   f2_mais_rapida = False 
   if t1 < t2:
      # menos tempo, então é MAIS eficiente.
      simbolo = ">"
      f1_mais_rapida = True
   elif t1 > t2:
      # função(f1) é MENOS eficiente pois leva mais tempo.
      simbolo = "<"
      f2_mais_rapida = True
   else:
      # dificilmente ocorrerá este caso, a menos é claro,
      # que se arredonde o número.
      simbolo = "="
   ...
   if f1.__name__ == f2.__name__:
      # obtendo nome do arquivo de ambos.
      complemento1 = f1.__code__.co_filename
      complemento2 = f2.__code__.co_filename
      # extranindo apenas o nome do caminho completo
      # e sua extensão.
      if os.path.isfile(complemento1):
         complemento1 = os.path.basename(complemento1)
         indice = complemento1.index('.')
         complemento1 = complemento1[0:indice]
      ...
      if os.path.isfile(complemento2):
         complemento2 = os.path.basename(complemento2)
         indice = complemento2.index('.')
         complemento2 = complemento2[0:indice]
      ...
      nome1 = complemento1 + "::" + f1.__name__
      nome2 = complemento2 + "::" +  f1.__name__
   else:
      nome1 = f1.__name__
      nome2 = f2.__name__
   ...
   print(
      "\n'%s'[%0.2fseg]  %s  '%s'[%0.2fseg]"
      %( nome1, t1, simbolo, nome2, t2)
   )
   if f1_mais_rapida:
      fator = floor(t2 // t1)
      print(
         "'{}' é {} mais veloz que '{}'."
         .format(nome1, fator, nome2)
      )
   elif f2_mais_rapida:
      fator = floor(t1 // t2)
      print(
         "'{}' é {} mais veloz que '{}'."
         .format(nome2, fator, nome1)
      )
   else:
      print("equiparado")
   ...

def benchmark_de_arvores():
   caminho = "../"
   qtd = 100
   tempo_i = timeit(
      "arvore_i(pth, False)",
      number = qtd,
      globals = {
         "arvore_i":arvore,
         "pth":caminho
      }
   )
   tempo_ii = timeit(
      "arvore_ii(pth, False)",
      number = qtd,
      globals = {
         "arvore_ii":arvore_ii.arvore,
         "pth":caminho
      }
   )

   assert tempo_i > tempo_ii
   if tempo_i > tempo_ii:
      ordem_info(
         arvore_ii.arvore, tempo_ii,
         arvore,
         tempo_i
      )

   # agora com um diretório mais cumprido.
   caminho = os.path.join(os.getenv("HOME"), "Documents/códigos")
   qtd = 2
   tempo_i = timeit(
      "arvore_i(pth, False)",
      number = qtd,
      globals = {
         "arvore_i":arvore,
         "pth":caminho
      }
   )
   # ainda tem que valer tal ordem.
   assert tempo_i > tempo_ii
   ordem_info(
      arvore, tempo_i,
      arvore_ii.arvore,
      tempo_ii
   )
...

if sys.platform == "linux":
   from biblioteca import executa_teste
   "executando todos testes ..."
   executa_teste(
      testa_arvore_i,
      testa_arvore_ii,
      benchmark_de_arvores
   )
...
