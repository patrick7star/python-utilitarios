"""
teste da barra de progresso e sua função
que ajuda ver onde está a computação do
total dado.
"""

# importando módulo a testar...
from re import T
from biblioteca import *
# biblioteca padrão do Python:
from time import sleep
from os import get_terminal_size

# total a cumprir padronizado.
TOTAL = 500_000


def teste_progresso():
   total = TOTAL//2, 1
   # sintaxe padrão:
   try:
      # testando a versão comum.
      for i in range(TOTAL //2):
         print('\r', progresso(i + 1, TOTAL//2),end='')
      # testando o com dados.
      for j in range(TOTAL//2):
         barra = progresso(j + 1, TOTAL//2, dados=True)
         print( '\r', barra, end='')
      ...
   except FimDoProgressoError as E:
      print("\nnão é possível mais continuar preenchendo a barra.")
      print("aqui é o resultado final:\n%s\n"%E.progresso)
   ...
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

def testa_progresso_rotulo():
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

def testa_progresso_rotulo_nao_dinamico():
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

def testa_progresso_redimensionavel():
   total =  35_921
   for k in range(1, total+1):
      print('\r',progresso(k, total, redimensiona=True),end='')
...

def testa_ProgressoPercentual():
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

def testa_ProgressoTemporal():
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

# executando testes ...
executa_teste(
   teste_progresso,
   #testa_progresso_rotulo,
   #testa_progresso_redimensionavel,
   #testa_ProgressoPercentual,
   #testa_ProgressoTemporal
)
