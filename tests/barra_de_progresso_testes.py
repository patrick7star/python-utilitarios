"""
teste da barra de progresso e sua função 
que ajuda ver onde está a computação do
total dado.
"""

# importando módulo a testar...
from biblioteca import *
# biblioteca padrão do Python:
from time import sleep

total, inicial = 15232, 102
# sintaxe padrão:
try:
   for i in range(inicial, total+total):
      print('\r', progresso(i, total),end='')
except FimDoProgressoError as E:
   print("\nnão é possível mais continuar preenchendo a barra.")
   print("aqui é o resultado final:\n%s\n"%E.progresso)

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
total =  35_921
for k in range(1, total+1):
   print('\r',progresso_redimensionavel(k, total),end='')
