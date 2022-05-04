# biblioteca padrão do terminal.
from os import get_terminal_size
# importando 'lib' especifica a testar.
from biblioteca import tela_otimizada
Ponto = tela_otimizada.Ponto

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

# primeira tela, sem borda vísivel e
# contendo grade.
def testa_tela_com_grade_e_sem_borda():
   t = tela_otimizada.Tela(None, None,True)
   t.risca(Ponto(5, 20), 5, horizontal=False)

   t.circula(Ponto(5, 40), Ponto(10, 60))
   t.circula(Ponto(0, 0), Ponto(3, 15))
   t.circula(
      Ponto(t.linhas-5, t.colunas-10),
      Ponto(t.linhas, t.colunas)
   )
   # imprimindo...
   print(t)
...

def testa_metodo_risca():
   t = tela_otimizada.Tela(None, None,borda=True, grade=False)

   t.risca(Ponto(3,10), 20, simbolo='X')
   t.risca(Ponto(3, 10), 20, horizontal=False)

   # imprimindo modificação...
   print(t)
...

# testando circunscrição em todos lados e cantos.
def testa_metodo_circula():
   t = tela_otimizada.Tela(None, None, borda=True, grade=False)
   compr = 7
   (P, Q) = Ponto(0, 0), Ponto(compr, compr)
   t.circula(P, Q)

   (P, Q) = Ponto(t.linhas-compr, 0), Ponto(t.linhas, compr)
   t.circula(P, Q)

   (P, Q) = (
      Ponto(0, t.colunas-compr),
      Ponto(compr, t.colunas)
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(t.linhas-compr, t.colunas-compr),
      Ponto(t.linhas, t.colunas)
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(0, int(t.colunas/2)-compr),
      Ponto(compr, int(t.colunas/2))
   )
   t.circula(P, Q)

   (P, Q) = (
      Ponto(t.linhas-compr, int(t.colunas/2)-compr),
      Ponto(t.linhas, int(t.colunas/2))
   )
   t.circula(P, Q)

   (P, Q) = Ponto(compr+3, 0), Ponto(2*compr, 17)
   t.circula(P, Q)

   (P, Q) = (
      Ponto(int(t.linhas/2), t.colunas-17),
      Ponto(int(t.linhas/2)+compr, t.colunas)
   )
   t.circula(P, Q)

   # imprimindo...
   print(t)
...

# testando o método de enquadradamento.
def testa_metodo_enquadra():
   t = tela_otimizada.Tela(10, None)
   string = "um teste apenas!"
   t.escreve(Ponto(5,30), string)
   t.enquadra(
      Ponto(3, 28),
      altura=4,
      largura=len(string) + 3
   )
   # imprimindo...
   print(t)
...

# --- ~~~ --- ~~~ executando testes --- ~~~ --- ~~~ 
executa_tal_funcao(testa_tela_com_grade_e_sem_borda)
executa_tal_funcao(testa_metodo_risca)
executa_tal_funcao(testa_metodo_circula)
executa_tal_funcao(testa_metodo_enquadra)
