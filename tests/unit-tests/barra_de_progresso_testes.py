"""
teste da barra de progresso e sua função
que ajuda ver onde está a computação do
total dado.
Todos testes aqui rodados, apelam apenas para
avaliação manual.
"""

# importando módulo a testar...
from re import T
# importando módulo a testar...
from unittest import FunctionTestCase, main
from sys import path
path.append("../../src/")
from barra_de_progresso import *
# biblioteca padrão do Python:
from time import sleep
from os import get_terminal_size

# total a cumprir padronizado.
TOTAL = 500_000

def progressoBasico():
   total = 100
   # sintaxe padrão:
   try:
      # testando a versão comum.
      for i in range(total):
         print('\r', progresso(i + 1, total),end='')
         sleep(1/2) # 500 ms
      # testando o com dados.
      for j in range(total*10):
         barra = progresso(j + 1, total, dados=True)
         print( '\r', barra, end='')
         sleep(1/100) # 100 ms.
      ...
   except FimDoProgressoError as E:
      print("\nprogresso finalizado.")
...

# temporizador.
def temporizador(T):
   if type(T) != int: raise TypeError
   ti = time()
   def aux():
      tf = time()
      delta_t = int(abs(tf-ti))
      if delta_t != T:
         return False
      else: return True
   return aux
...

def progressoRotulo():
   titulo = "The Conjuring 3: The End is Coming.avi"
   fim = 10**4
   for x in range(1, fim+1):
      print('\r', progresso_rotulo(titulo, x, fim, True), end='')

   titulo = "Madre Tereza de Calcultar e sua Família.mkv"
   for x in range(1, fim+1):
      print('\r', progresso_rotulo(titulo, x, fim, False), end='')

   titulo = "Die Hard.mkv"
   for x in range(1, fim+1):
      print('\r', progresso_rotulo(titulo, x, fim, False), end='')
   print("\n")
...

def progresso_rotulo_nao_dinamico():
   print("var \"aux\" deletada?","aux" not in dir(),end="\n\n")
   k = 1
   while k <= 100_000:
      sleep(1)
      print(progresso_rotulo("UM MARMANJO EM APUROS.avi", k, 100_000))
      k *= 10

   print(progresso_rotulo("UM MARMANJO EM APUROS.avi",
                           10, 100, dinamico=False))
   print(progresso_rotulo("UM MARMANJO EM APUROS.avi",
                           30, 100, dinamico=False))
   print(progresso_rotulo("UM MARMANJO EM APUROS.avi",
                           50, 100, dinamico=False))
   print(progresso_rotulo("UM MARMANJO EM APUROS.avi",
                           90, 100, dinamico=False))
...

def progressoRedimensionavel():
   total =  35_921
   for k in range(1, total+1):
      print('\r',progresso(k, total, redimensiona=True),end='')
...

def progressoPercentual():
   bp = ProgressoPercentual(TOTAL)
   for valor in range(0,TOTAL+1):
      bp += valor
      # visualizando barra se possível.
      string = str(bp)
      if string != "None":
         print('\r', string, end="")
   # verificando se cumprir a impressão em 100%
   print(bp)
   print(bp)
   ...
...

def progressoTemporal():
   bpt = ProgressoTemporal(TOTAL)
   (vazias, barras) = (0, 0)
   for valor in range(1, TOTAL+1):
      # atualiza o valor.
      bpt += valor
      print('\r', bpt, end="")
   ...
   # esgotando chamadas e produzindo exceção.
   print("\nchamando repetidas vezes após o fim:")
   for _ in range(10):
      try:
         print(bpt)
      except:
         print("não possível mais usar barra de progresso")
   ...
...

FunctionTestCase(
   progressoBasico,
   description="""
      \ro nível mais básico do progresso
      \rcontido na biblioteca.
   """
)
FunctionTestCase(
   progressoRotulo,
   description = """
      \rUm tipo de progresso, na estrutura do básico,
      \rporém com um rótulo(uma string passada como
      \rargumento) em movimento, ele tipo se move
      \rà cada 1,5seg.
   """
)
FunctionTestCase(progressoRedimensionavel)
FunctionTestCase(progressoTemporal)
FunctionTestCase(progressoPercentual)
FunctionTestCase(progresso_rotulo_nao_dinamico)

if __name__ == "__main__":
   main(verbosity=2)
