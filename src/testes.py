"""
 módulo com alguns utilitários para que
 seja realizado uma série de testes.
 No fim, o módulo organiza as saídas.
"""

# biblioteca padrão do Python:
from os import get_terminal_size


def separador():
   "separador de testes"
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

def executa_tal_funcao(funcao):
   "executa teste em tais funções."
   # reparando nome da função.
   nome_funcao = funcao.__name__
   # casos possíveis das funções trabalhadas.
   casos_possiveis = (
      "testa", "teste_da", "teste_de", 
      "testa_funcao", "testa_metodo", 
      "testa_procedimento"
   )
   novo_nome = nome_funcao

   # troca apenas caso específico que caiu.
   for caso in casos_possiveis:
      if nome_funcao.startswith(caso):
         novo_nome = (
            nome_funcao
            .replace(caso, "")
            .strip("_")
         )
      ...
   else:
      # nova mensagem sobre o que está acontecendo...
      print("'{}' testando ...\n".format(novo_nome))
      # chamando tal função...
      funcao()
      # delimitando separador.
      separador()
   ...
...

def executa_teste(*funcoes):
   "rotula as funções passadas e demarca 'outputs'"
   # apelido para facilitar codificação:
   ETF = executa_tal_funcao
   # no caso de várias "p-args".
   # o primeiro caso leva em consideração apenas
   # uma função passada.
   if type(funcoes) == tuple and len(funcoes) == 1:
      funcao = funcoes[0]
      # trata do caso de uma só lista passada.
      if type(funcao) == list:
         executa_teste(*funcao)
      else:
         ETF(funcao)
   # se houver mais que uma função passada:
   else:
      for f in funcoes:
         ETF(f)
   ...
...

# o que será importado ...
__all__ = ["executa_teste"]

# testes unitários:
if __name__ == "__main__":
   # funções para testes:
   def teste_de_funcaoI():
      print("a saída da função é \"funcaoI\"")
   def funcaoII():
      print("a saída da função é \"funcaoII\"")
   def testa_funcaoIII():
      print("a saída da função é \"funcaoIII\"")
   def teste_da_funcaoIV():
      print("a saída da função é \"funcaoIV\"")

   print("modo comum:".title())
   executa_teste(
      teste_de_funcaoI,
      funcaoII,
      testa_funcaoIII,
      teste_da_funcaoIV
   )

   print("apenas uma função passada:".title())
   executa_teste(funcaoII)
   executa_teste(teste_da_funcaoIV)
   print("lista passada como um argumento apenas:".title())
   lista = [
      funcaoII, teste_da_funcaoIV,
      testa_funcaoIII,
      teste_de_funcaoI
   ]
   executa_teste(lista)
...
