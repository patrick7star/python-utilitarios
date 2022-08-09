
"""
Implementando a formação de Tabelas para
minha 'biblioteca padrão' Python.
"""

# biblioteca padrão do Python:
from os import get_terminal_size
from copy import deepcopy
from array import array as Array

# módulos auxiliares:
from tabelas_utilitarios import reveste, TabelaStrMatriz
from tabelas_variaveis import *

class Coluna():
   def __init__(self, rotulo, array):
      self._rol = array
      self._nome = rotulo
   ...

   def __iter__(self):
      "iteração embutida na própria lista."
      return iter(self._rol)
   
   def nome(self):
      "encapsulamento, retorna o rótulo da coluna"
      return self._nome
   
   def __len__(self):
      "quantia de dados no rol"
      return len(self._rol)
...


# ajusta baseado no comprimento passado
# "adicionando margens" a string.
def equilibra_str(string, comprimento):
   str_comprimento = len(string)
   if str_comprimento % 2 != 0:
      consertada = string + ESPACO
      return equilibra_str(consertada, comprimento)
      
   if len(string) <= comprimento:
      diferenca = abs(len(string) - comprimento)
      while len(string) < comprimento:
         string = (
            "{espaco}{}{espaco}"
            .format(string, espaco=ESPACO)
         )
      ...
   ...
   return string
...

def aglomera_colunas(coluna1, coluna2):
   linhas = []
   maior_qtd = max(len(coluna1), len(coluna2))
   
   i1 = iter(coluna1)
   i2 = iter(coluna2)
   
   # computando o valor com mais dígitos do rols, ou
   # o rótulo com mais letras.
   mc1 = max(len(str(v)) for v in coluna1)
   mc1 = max(len(coluna1.nome()), mc1)
   mc2 = max(len(str(v)) for v in coluna2)
   mc2 = max(len(coluna2.nome()), mc2)

   rotulo1 = coluna1.nome()
   rotulo1 = equilibra_str(rotulo1, mc1)
   rotulo2 = coluna2.nome()
   rotulo2 = equilibra_str(rotulo2, mc2)

   linhas.append(
      "{barra}{margem}{0}{margem}{barra}{margem}{1}{margem}{barra}"
      .format(
         rotulo2, 
         rotulo1, 
         barra = BARRA,
         margem = MARGEM
      )
   )
   # adição da margem do valor à borda
   # da tabela.
   adicao = len(MARGEM)
   while maior_qtd != 0:
      linha = BARRA
      try:
         celula = str(next(i2))
         linha += (
            MARGEM + 
            equilibra_str(celula, mc2) + 
            MARGEM + BARRA
         )
      except StopIteration:
         linha += (
            MARGEM + equilibra_str(TRACOS, mc2) 
            + MARGEM + BARRA
         )
      ...
      try:
         celula = str(next(i1))
         linha += (
            MARGEM + equilibra_str(celula, mc1) 
            + MARGEM + BARRA
         )
      except StopIteration:
         linha += (
            MARGEM + equilibra_str(TRACOS, mc1) 
            + MARGEM + BARRA
         )
      ...
      linhas.append(linha)
      maior_qtd -= 1
      del linha
   ...

   return linhas
...

# cria barras superiores, inferiores e centrais.
def tampa_tabela(linhas):
   # largura máxima da tabela.
   comprimento = len(linhas[0])
   # demilitador baseado na largura da tabela.
   barra = BARRA * comprimento
   # para computar a próxima inclusão
   # na próxima linha de cédulas.
   qtd = 0

   for indice in range(len(linhas) + 1):
      linhas.insert(indice + qtd, barra)
      qtd += 1
   ...
...

def otimiza_uso_de_tela(linhas):
   altura = get_terminal_size().lines
   largura = get_terminal_size().columns
   # largura da tabela.
   lT = len(linhas[0])
   # espaço entre as tabelas concatenadas.
   afastamento = ESPACO * 3
   # quantas tabelas cabem dado a largura
   # do terminal. Uma divisão simples entre
   # a "largura do terminal" divido pela
   # da tabela mais o espaçamento entre 
   # elas.
   n = largura // (lT + len(afastamento))
   # altura das tabelas. Pode ser qualquer
   # valor, já que não seria fixo na impressão.
   aT= len(linhas) // n
   # fila para reter fatias e concatena-las
   # baseado na primeira retida.
   fila_de_fatias = []
   # uma lista, onde as strings que formam
   # a tabela(chamadas linhas aqui) são
   # adicionandas após removidas das demais.
   fatia = []

   # fatia igualmente as linhas passadas e
   # guarda tais fatias para anexação posteriore.
   for k in range(1, len(linhas)+1):
      if k % aT == 0:
         tampa_tabela(fatia)
         fila_de_fatias.append(fatia[:])
         fatia.clear()
      else:
         fatia.append(linhas.pop(0))
      ...
   ...

   # limpa para reutilização da referência.
   linhas.clear()
   # a primeira "fatia" é que junta tudo.
   remocao = fila_de_fatias.pop(0)
   linhas.extend(remocao)
   while len(fila_de_fatias) > 0:
      fatia_removida = fila_de_fatias.pop(0)
      indice = 0
      while len(fatia_removida) > 0:
         linha = fatia_removida.pop(0)
         linhas[indice] = (
            linhas[indice] +
            afastamento
            + linha
         )
         indice += 1
      ...
   ...
...

def forma_tabela(C1, C2):
   if type(C1) == type(C2) == Coluna:
      tabela = aglomera_colunas(C1, C2)
      tampa_tabela(tabela)
      #otimiza_uso_de_tela(tabela)
      # cria string disso.
      tabela_string = "\n".join(tabela)
      matriz_ts = TabelaStrMatriz(tabela_string)
      tabela = reveste(matriz_ts)
      return tabela
   else:
      raise TypeError()
   ...
...

__all__ = ["Coluna", "forma_tabela"]

# testes unitários:
if __name__ == "__main__":
   from testes import executa_teste
   from random import randint, choice

   # dados comuns:
   coluna1 = Coluna("gênero", ['M', 'F', 'F', 'F', 'M'])
   coluna2 = Coluna("idade", [14, 27, 38, 13, 51, 24])

   def imprime(array):
      print("\n".join(array), end="\n\n")

   def testa_funcao_cria_tabela():
      esboco = aglomera_colunas(coluna1, coluna2)
      imprime(esboco)
   ...

   def teste_de_funcao_tampa_tabela():
      linhas_esboco = aglomera_colunas(coluna2, coluna1)
      tampa_tabela(linhas_esboco)
      imprime(linhas_esboco)
   ...

   def testa_funcao_ct_dobradura():
      rol = list(choice(['F', 'M']) for _ in range(132))
      coluna1 = Coluna("gênero", rol)
      rol = list(randint(5, 100) for _ in range(129))
      coluna2 = Coluna("idade", rol)
      esboco_inicial = aglomera_colunas(coluna1, coluna2)
      otimiza_uso_de_tela(esboco_inicial)
      imprime(esboco_inicial)
   ...

   def testa_funcao_reveste():
      rol = list(choice(['F', 'M']) for _ in range(132))
      coluna1 = Coluna("gênero", rol)
      rol = list(randint(5, 100) for _ in range(129))
      coluna2 = Coluna("idade", rol)
      esboco_inicial = aglomera_colunas(coluna1, coluna2)
      otimiza_uso_de_tela(esboco_inicial)
      esboco = "\n".join(esboco_inicial)
      resultado = reveste(TabelaStrMatriz(esboco))
      print(resultado)
   ...

   def testa_funcao_forma_tabela():
      def gera_codigo():
         simbolos = ['@']
         for _ in range(12):
            x = chr(randint(41, 97))
            simbolos.append(x)
         ...
         return "".join(simbolos)
      ...

      coluna_i = Coluna(
         "candidatos", 
         ["João Almeida", "Juana Barbados",
         "Lucas Otaviano", "Carol Bastos",
         "Felipe Joaquino", "Adélio Portas",
         "Constantino Pereira", "Victor Peres",
         "Juna Albrês", "Rita Cadilaque", 
         "Mônica Fernandes", "Joana Drumon",
         "Sebastian Ferreira"]
      )

      coluna_ii = Coluna(
         "códigos",
         [gera_codigo() for _ in range(7)]
      )

      print(forma_tabela(coluna_ii, coluna_i))

   executa_teste(testa_funcao_cria_tabela)
   executa_teste(teste_de_funcao_tampa_tabela)
   executa_teste(testa_funcao_ct_dobradura)
   executa_teste(testa_funcao_reveste)
   executa_teste(testa_funcao_forma_tabela)
...
