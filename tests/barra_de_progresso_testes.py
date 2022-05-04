"""
teste da barra de progresso e sua função
que ajuda ver onde está a computação do
total dado.
"""

# importando módulo a testar...
from biblioteca import *
# biblioteca padrão do Python:
from time import sleep
from os import get_terminal_size

# separador de testes:
def separador():
   # obtendo largura da tela.
   largura = get_terminal_size().columns
   qtd = largura // 4
   # espaço vertical de uma linha.
   print("")
   for i in range(qtd):
      print("~~~",end=" ")
   # espaço vertical de duas linhas.
   print("\n\n")
...

# executa teste em tais funções.
def executa_tal_funcao(funcao):
   # reparando nome da função.
   novo_nome = (
      funcao
      .__name__
      .replace("testa", "")
      .strip("_")
   )
   # nova mensagem sobre o que está acontecendo...
   print("'{}' testando ...\n".format(novo_nome))
   # chamando tal função...
   funcao()
   # delimitando separador.
   separador()
...

# total a cumprir padronizado.
TOTAL = 500_000

def teste_progresso():
   (total, inicial) = TOTAL, 102
   # sintaxe padrão:
   try:
      for i in range(inicial, total+1):
         print('\r', progresso(i, total),end='')
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
      print('\r',progresso_redimensionavel(k, total),end='')
...

# faz o teste do novo objeto que trabalha
# com percentuais.
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
   bpt.start()
   for valor in range(0, TOTAL+1):
      # atualiza o valor.
      bpt += valor
      # visualizando barra se possível.
      # visualizando barra se possível.
      string = str(bpt)
      if string != "None":
         print('\r', string, end="")
   ...
   if string != "None":
      print('\r', string, end="")
      print("executado corretamente.")
...

def testa_ProgressoTemporal_I():
   bpt = ProgressoTemporal_I(TOTAL)
   for valor in range(0, TOTAL+1):
      # atualiza o valor.
      bpt += valor
      # visualizando barra se possível.
      string = str(bpt)
      if string != "None":
         print('\r', string, end="")
   ...
   string = str(bpt)
   if string != "None":
      print('\r', string, end="")
   print(bpt, bpt, bpt, sep="\n")
...

# executando testes ...
executa_tal_funcao(teste_progresso)
executa_tal_funcao(testa_progresso_rotulo)
executa_tal_funcao(testa_progresso_redimensionavel)
executa_tal_funcao(testa_ProgressoPercentual)
executa_tal_funcao(testa_ProgressoTemporal)
executa_tal_funcao(testa_ProgressoTemporal_I)
