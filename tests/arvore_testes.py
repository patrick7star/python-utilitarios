#!/usr/bin/python3 -O

# biblioteca padrão do Python:
import os, sys, time, unittest
from math import floor
from timeit import timeit, Timer
from threading import Thread
from decimal import Decimal
from queue import SimpleQueue
# importando módulos a testar:
sys.path.append("..")
from src.tree.arvore_old import arvore as arvore_i
from utilitarios import arvore as modulo_arvore

# Extraindo função...
arvore_ii = modulo_arvore.arvore

"""
  O teste abaixo funciona apenas em plataforma linux; e se tiver os 
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
   tipo = modulo_arvore.GalhoTipo.FINO
   # testando novo código otimizado.
   print(arvore_ii(caminho))
   print(arvore_ii(caminho, True, tipo))
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
...

from time import sleep
def benchmark_em_diretorio_mais_profundo():
   # agora com um diretório mais cumprido.
   caminho = os.path.join(os.getenv("HOME"), "Documents/códigos")
   seg_i = Decimal(0); seg_ii = Decimal(0)
   QTD = 1

   def teste_1():
      nonlocal seg_i

      decorrido = timeit(
         "tree(path, False)",
         number = QTD,
         globals = {
            "tree":arvore_i,
            "path":caminho
         }
      )
      seg_i += Decimal.from_float(decorrido)
   ...

   def teste_2():
      nonlocal seg_ii

      decorrido = timeit(
         "tree(path, mostra_arquivos=False)",
         number = QTD,
         globals = {
            "tree":arvore_ii,
            "path":caminho
         }
      )
      seg_ii += Decimal.from_float(decorrido)
   ...

   medida_1 = Thread(target=teste_1, name="medida(1)")
   medida_2 = Thread(target=teste_2, name="medida(2)")
   pool = SimpleQueue()
   pool.put(medida_1); pool.put(medida_2)
   
   # Começando juntas o teste...
   medida_2.start(); medida_1.start()

   # Aguardando ambas...
   while not pool.empty():
      medida = pool.get()
      
      medida.join(timeout=0.582)

      if medida.is_alive():
         pool.put(medida)
      else:
         print("A thread '%s' terminou." % medida.name)

   #medida_1.join(); medida_2.join();

   ordem_info(arvore_i, float(seg_i), arvore_ii, float(seg_ii))
...

def benchmark_de_arvores():
   caminho = "../"; QTD = 10 
   seg = Decimal(0)

   def teste1(a: Timer):
      nonlocal seg
      decorrido = medida_i.timeit(QTD)
      seg += Decimal.from_float(decorrido)
   ...

   # Definindo segundo teste para ser executado posteriormente.
   medida_i = Timer(
      stmt = "tree(path, False)",
      globals = {
         "tree":arvore_i,
         "path":caminho
      }
   )
   tredi = Thread(target=teste1, args=(medida_i,))
   tredi.start()

   tempo_ii = timeit(
      stmt = "tree(path, mostra_arquivos=False)",
      number = QTD,
      globals = {
         "tree": arvore_ii,
         "path": caminho
      }
   )
   print("Execução de '{}' finalizada.".format(arvore_ii.__name__))
   tredi.join()
   tempo_i = float(seg)

   # Análise detalhada:
   ordem_info(arvore_i, tempo_i, arvore_ii, tempo_ii)
...

if sys.platform == "linux":
   t1 = unittest.FunctionTestCase(testa_arvore_i)
   t2 = unittest.FunctionTestCase(testa_arvore_ii)
   t3 = unittest.FunctionTestCase(benchmark_de_arvores)
   t4 = unittest.FunctionTestCase(benchmark_em_diretorio_mais_profundo)

   # Testes acimas declarados, e se deseja executa-lô ou não.
   testes = [(t1, False), (t2, False), (t3, False), (t4, True)]

   for (test, modo) in testes: 
      assert isinstance(test, unittest.TestCase)
      assert isinstance(modo, bool)

      if modo: 
         test.run()
      else:
         nome = test.id()
         print("[  off  ] {}".format(nome))
...
