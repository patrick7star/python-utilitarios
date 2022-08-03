#!/usr/bin/python3.8

# bibliotecas:
from curses import (
   napms, initscr, init_pair, wrapper,
   A_BOLD, color_pair, start_color,
   curs_set, noecho, COLOR_BLACK, 
   KEY_RESIZE, endwin
)
from os import get_terminal_size, execv
from random import choice
from math import floor
# meus módulos:
from roleta import Roleta
from array import array as Array

# dimensões do terminal que roda tal.
terminal = get_terminal_size()
(Y,X) = terminal.lines, terminal.columns

# matriz que "pixela" tela com caractéres.
matriz = [Array('u', [' '] * X) for _ in range(Y)]

# variáveis de configuração.
# tempo para descer cada variável num mapa, onde
# quanto maior chave, menor o tempo, consequentemente
# maior a velocidade.
# definições com o programa em execução:
velocidades = {1:200, 2:100, 3:50, 4:10, 5:5, 6:3}
# visualizar barra de status?
MOSTRA_BARRA_STATUS = True 
# fileiras multi-coloridas.
RAINBOW_MODE = True 
# espaços entre fileiras.
FILEIRAS_ESPACOS = 4 


# barra de progresso da velocidade:
def barra_velocidade(velocidade_atual):
   # um pontinho para cada nível.
   barra = '.' * len(velocidades)
   progresso = (
      barra[1:velocidade_atual] 
         + '#' + 
      barra[velocidade_atual:]
   )
   return '- %s +' % progresso
...

# mostra, em tempo real, a barra de status e suas configurações.
def barra_status_visor(janela, nivel, numero):
   cor = A_BOLD
   texto = 'LIN={} COLS={}'
   texto_i = 'ESPAÇOS={}'
   texto_ii = 'FILEIRAS={}'
   janela.addstr(Y-1,0, texto_i.format(FILEIRAS_ESPACOS))
   janela.addstr(Y-1, X-18,texto.format(Y,X))
   janela.addstr(Y-1, 15, barra_velocidade(nivel), cor)
   janela.addstr(Y-1, 30, texto_ii.format(numero), cor)
...

def imprime_matriz(janela):
   # imprimindo a matriz dentro do "curses".
   if RAINBOW_MODE:
      paletas = [ 
         color_pair(i % 7) | A_BOLD 
         for i in range(X-2)
      ]
      for k in range(X-2):
         cor = paletas[k]
         for i in range(Y): 
            char = matriz[i][k]
            janela.addch(i, k, char,cor)
         ...
      ...
   else:
      for i in range(Y):
         for j in range(X-2): 
            cor = color_pair(3) | A_BOLD
            char = matriz[i][j]
            janela.addch(i, j, char, cor) 
         ...
      ...
   ...
...

def main(janela):
   global MOSTRA_BARRA_STATUS, UNICA_DIRECAO
   # execução da janela:
   janela = initscr() # criando uma janela.
   start_color() # inicializando cores do sistema.
   curs_set(False) # desabilitando cursor.
   #curses.use_default_colors()
   noecho() # tirando echo ao digitar.

   # paletas de cores:
   for i in range(0, 8): 
      init_pair(i+1, i, COLOR_BLACK)

   # dados de configuração:
   n = int(floor(X / FILEIRAS_ESPACOS))
   # direção original?
   para_baixo = choice([False, True]) 
   roletas = [
      Roleta(para_baixo, FILEIRAS_ESPACOS*i, matriz) 
      for i in range(1, n)
   ]
   # tecla ativida para algumans configurações.
   janela.nodelay(True) # não interroper loop por causa do input.
   (tecla, v) = (-1, 3) # só "declarando" variável.
   # até for interrompido com o teclado, ficar
   # alternando entre as roletas, dado uma 
   # limite de tempo.
   while tecla != ord('s'):
      # alterando as configurações:
      if tecla == ord('+') and v <= len(velocidades)-1: 
         v += 1 # aumenta velocidade.
      elif tecla == ord('-') and v > 1: 
         v-=1 # diminui velocidade.
      elif tecla == ord('b'): 
         # se estiver desativdo, então ativa.
         if not MOSTRA_BARRA_STATUS: 
            MOSTRA_BARRA_STATUS = True
         else: 
            MOSTRA_BARRA_STATUS = False
      elif tecla == ord('r'):
         # ativa e desativa modo arco-íris.
         if not RAINBOW_MODE: 
            RAINBOW_MODE = True
         else: 
            RAINBOW_MODE = False
      elif tecla == KEY_RESIZE:
         # executa o programa, para se 
         # adequar a nova dimensão.
         napms(600)
         # terminando antigo...
         endwin() 
         # interpletador python.
         programa = "/usr/bin/python3"
         # meu código no diretório.
         codigo = "./matrix.py"
         execv(programa, ("-B", codigo,))

      tecla = janela.getch() # obtendo entrada.
      for obj in roletas: 
         obj.um_deslizamento()
      janela.refresh() # atualizando tela.
      imprime_matriz(janela) # imprime matriz.
      # pausa(definindo velocidade)
      napms(velocidades[v])       
      # atual dimensão do terminal na tela.
      if MOSTRA_BARRA_STATUS: 
         barra_status_visor(janela,v,n)
   endwin() # finalizando...
...


# execução de testes.
if __name__ == '__main__':
   wrapper(main)
   print("programa finalizado.")
...

