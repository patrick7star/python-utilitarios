
"""
Implementando a formação de Tabelas para
minha 'biblioteca padrão' Python.
"""

# biblioteca padrão do Python:
from os import get_terminal_size
from copy import deepcopy
from array import array as Array

# módulos auxiliares:
from tabelas_utilitarios import (reveste, TabelaStrMatriz)
from tabelas_variaveis import *

# o que será exportado?
__all__ = [
   "Coluna", "forma_tabela", 
   "forma_tabela_com_multiplas_colunas"
]


class Coluna:
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
   
   # acionando comparações.
   def __lt__(self, coluna):
      assert isinstance(coluna, Coluna)
      return len(self) < len(coluna)

   def __gt__(self, coluna):
      assert isinstance(coluna, Coluna)
      return len(self) > len(coluna)
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

from copy import deepcopy
from sys import exit

# pega todas colunas passadas, ajusta elas lado à lado, com margem
# e um separador visível. Todas linhas processadas e criadas pela
# rotina, serão enfileiras, assim, o retorno será uma fila contendo
# tais linhas para demais processamento, onde a primeira linha da 
# fila é o cabeçalho da futura tabela.
def aglomera_multiplas_colunas(*colunas) -> [str]:
   if not todos_sao_colunas(colunas):
      raise TypeError("todas têm quer do tipo Coluna")
   # achando a Coluna com o maior rol.
   mais_comprida_coluna = max(colunas)
   # lista com todas iterações das respectivas colunas.
   lista_iteracoes_das_colunas = list(iter(c) for c in colunas) 
   # achando a entrada da Coluna, onde sua formatação em texto é a
   # mais longa.
   # primeiro com os nomes do cabeçalho:
   mais_comprida_celula = max(len(c.nome()) for c in colunas)
   # algora com a formatação de string dos dados.
   for c in deepcopy(lista_iteracoes_das_colunas):
      for data in c:
         comprimento = len(str(data))
         if comprimento > mais_comprida_celula:
            mais_comprida_celula = comprimento
      ...
   ...
   # adicionando duas mais espaços vázios, que são as margens para 
   # o separador do nome/dado.
   mais_comprida_celula += (len(MARGEM) + len(BARRA)) 
   # deque de linhas para cocatenação baseado em várias 
   # quebras-de-linhas.
   deque_de_linhas = []
   # para juntar componentes numa só linha.
   celulas = []

   # criando primeira linha da tabela, o cabeçalho com os respectivos
   # nomes(grandezas) da sequência de rols posterior.
   separador_esquerdo = "{0}{1}".format(BARRA, MARGEM)
   celulas.append(separador_esquerdo)

   for coluna in colunas:
      filete = (
         "{:^{length}}{margem}{separador}"
         .format(
            coluna.nome(), margem=MARGEM,
            length=mais_comprida_celula,
            separador=BARRA
         )
      )
      celulas.append(filete)
   ...
   # aglomera todas células numa única linha, então limpa a deque
   # para próximas aglomerações.
   deque_de_linhas.append(''.join(celulas))
   celulas = []

   # agora trabalhando somente com os rols aninhados com suas
   # respectivas grandezas, que foram formatadas acima.
   for _ in range(len(mais_comprida_coluna)):
      separador_esquerdo = "{0}{1}".format(BARRA, MARGEM)
      celulas.append(separador_esquerdo)

      for coluna in lista_iteracoes_das_colunas:
         try:
            dado = next(coluna)
         except StopIteration:
            dado = "---"

         # formatando a célula com o dado, e adicionando na deque
         # de concatenação(para formar uma única linha).
         celulas.append(
            "{:^{length}}{margem}{separador}"
            .format(
               dado, separador=BARRA,
               margem=MARGEM,
               length=mais_comprida_celula
            )
         )
      ...
      # aglomera todas células numa única linha, então limpa a deque
      # para próximas aglomerações.
      deque_de_linhas.append(''.join(celulas))
      celulas = []
   ...

   # retorna deque contendo o cabeçalho e os rols tudo organizado, 
   # do modo que foi processado inicialmente.
   return deque_de_linhas
...

def forma_tabela_com_multiplas_colunas(*colunas, 
estilo_padrao=True) -> str:
   if todos_sao_colunas(colunas):
      tabela = aglomera_multiplas_colunas(*colunas)
      # Por enquanto, há apenas dois estilos a serem secionados.
      if estilo_padrao:
         tampa_tabela(tabela)
      else:
         tampa_tabela_ii(tabela)
      #otimiza_uso_de_tela(tabela)
      # cria string disso.
      tabela_string = "\n".join(tabela)
      matriz_ts = TabelaStrMatriz(tabela_string)
      tabela = reveste(matriz_ts)
      return tabela
   else:
      raise TypeError("todas têm quer do tipo Coluna")
...

def todos_sao_colunas(colunas: list) -> bool:
   " verificando se todos são instância, portanto do tipo, Coluna."
   return all(map(lambda c: isinstance(c, Coluna), colunas))

def tampa_tabela_ii(linhas: [str]) -> None:
   """
   nova modalidade de tampa a tabela, os separadores são apenas 
   colocados parte inferior e superior, para fechar a tabela, e um 
   separador entre o cabeçalho e os demais dados das colunas.
   """
   # largura máxima da tabela.
   comprimento = len(linhas[0])
   # demilitador baseado na largura da tabela.
   barra = BARRA * comprimento
   # bara no topo da tabela.
   linhas.insert(0, barra)
   # separador entre o cabeçalho e os dados.
   linhas.insert(2, barra)
   # separador que fecha parte inferior da tabela.
   linhas.append(barra)
...

from unittest import (TestCase, main)
from sys import exit
from random import (choice, randint)
from testes import bool_to_str

# dados gerais para testes. Dados abaixo variam em tamanho e valores
# já que são gerados, majotariamente, via aleatoriedade:
coluna1 = Coluna(
   "gênero", list(
      choice(['M', 'F']) 
      for _ in range(randint(3, 12))
   )
)
coluna2 = Coluna(
   "idade", list(
      randint(14, 51) 
      for _ in range(randint(6, 10))
   )
)
coluna3 = Coluna(
   "frutas", [
      "maça", "uva", "morango", "abacaxi", "pêssego", 
      "manga", "framboesa", "laranja"
])
coluna4 = Coluna(
   "valor-verdade", [
      bool_to_str(choice([True, False])) 
      for _ in range(randint(3, 8))
   ]
)

class Funcoes(TestCase):
   def aglomeraMultiplasColunas(self):
      aglomera_multiplas_colunas(coluna1, coluna2, coluna3)
   ...
   def formaTabelaComMultiplasColunas(self):
      funcao = forma_tabela_com_multiplas_colunas
      print(funcao(coluna3, coluna2, coluna1))
   ...

   def FTCMC_ComQuatroColunas(self):
      FUNCAO = forma_tabela_com_multiplas_colunas
      ESTILO = choice([True, False])
      print(
         FUNCAO(
            coluna3, coluna2, 
            coluna1, coluna4, 
            estilo_padrao=ESTILO
         )
      )
   ...

   def aglomeradoMinucioso(self):
      saida_i = aglomera_multiplas_colunas(coluna1, coluna2, coluna3)
      saida_ii = aglomera_colunas(coluna3, coluna2)
      print(
         "saídas crúas:",
         saida_i, saida_ii,
         sep = '\n'
      )
      print(
         "resultado formatados:",
         "\n".join(saida_i), 
         "\n".join(saida_ii), 
         sep='\n'
      )
   ...

   def novoEstiloDeTampa(self):
      tabela = aglomera_multiplas_colunas(
         coluna2, coluna1,
         coluna3, coluna4
      )
      tampa_tabela_ii(tabela)
      tabela_string = "\n".join(tabela)
      matriz_ts = TabelaStrMatriz(tabela_string)
      tabela = reveste(matriz_ts)
      print(tabela)
   ...

   def runTest(self):
      self.formaTabelaMultiplasColunas()
...


# testes unitários:
if __name__ == "__main__":
   main()
   exit()
   from testes import executa_teste
   from random import randint, choice


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
