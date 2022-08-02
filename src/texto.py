
"""
O código que trabalha na visualização 
de textos-desenhos ficará aqui mesmo,
na biblioteca utilitários. Só que agora,
com um bom conhecimento de algoritmos
o processo para gera-lô pode ser mais
reduzido.
"""

# biblioteca padrão do Python:
from base64 import encode
from os import listdir
from os.path import join
# própria biblioteca:
from tela_objetos import Matriz

# caminhos dos arquivos contendo os "desenhos".
caminho_alfabeto = r"simbolos\\alfabeto"
caminho_numeros = r"simbolos\\numeros"
caminho_pontuacao = r"simbolos\\pontuacao"

# mapa contendo todo alfabeto, dígitos,
# e pontuações... quase todo símbolos
# na tabela ASCII.
tabela = {}
# verifica os símbolos foram carregados.
carregados = False


class MatrizTexto(Matriz):
   def __init__(self, altura, largura):
      grade = False
      super().__init__(altura, largura, grade)
   ...

   def dimensao(self):
      """
      retorna tupla com a dimensão, onde primeiro 
      valor é a altura, a segunda é a largura.
      """
      qtd_cols = len(self._linhas[0])
      qtd_lins = len(self._linhas)
      return (qtd_lins, qtd_cols)
   ...
...

def file_to_matriz(arquivo):
   linhas = list(arquivo)
   qtd_col = max(len(l) for l in linhas)
   qtd_lin = len(linhas)
   matriz = MatrizTexto(qtd_lin, qtd_col)
   for (y, linha) in enumerate(linhas):
      for (x, char) in enumerate(linha):
         try:
            # burla quebra-de-linhas.
            if char != '\n':
               matriz.altera(y, x, char)
         except IndexError:
            # sem indexação, apenas adiciona
            # espaços brancos para uniformidade.
            matriz.altera(y, x, ' ')
         ...
      ...
   ...
   return matriz
...

def inicializando():
   for arquivo in listdir(caminho_alfabeto):
      caminho = join(caminho_alfabeto, arquivo)
      chave = arquivo[0:-4]
      desenho = file_to_matriz(open(caminho, "rt"))
      tabela[chave] = desenho
   ...

   # carregando números:
   for arquivo in listdir(caminho_numeros):
      caminho = join(caminho_numeros, arquivo)
      chave = nome_to_digito(arquivo[0:-4])
      desenho = file_to_matriz(open(caminho, "rt"))
      tabela[chave] = desenho
   ...

   # carregando pontuação:
   for arquivo in listdir(caminho_pontuacao):
      caminho = join(caminho_pontuacao, arquivo)
      chave = arquivo[0:-4]
      desenho = file_to_matriz(open(caminho, "rt"))
      tabela[chave] = desenho
   ...
   global carregados
   carregados = True
...

# converte nomes de dígitos nos valores 
# em sí.
def nome_to_digito(nome):
   tokens = {
      "zero":0, "um":1, "dois":2, "tres":3, 
      "quatro":4, "cinco":5, "seis":6, "sete":7, 
      "oito":8, "nove":9
   }
   return tokens[nome]
...

# concatena duas matriz-texto.
def concatena(mt1, mt2):
   (a1, l1) = mt1.dimensao()
   (a2, l2) = mt2.dimensao()
   diferenca = abs(a1-a2)
   # computa maior dimensão
   altura = max(a1, a2)
   largura = l1 + l2 + 1
   # matriz-texto resultante.
   resultado = MatrizTexto(altura, largura)
   for y in range(a1):
      for x in range(l1):
         char = mt1[y][x]
         if a1 < a2:
            resultado.altera(y+diferenca, x, char)
         else:
            resultado.altera(y, x, char)
      ...
   ...
   for y in range(a2):
      for x in range(l2):
         char = mt2[y][x]
         x1 = x + (1 + l1)
         if a2 < a1:
            y1 = y + diferenca
         else:
            y1 = y
         resultado.altera(y1, x1, char)
      ...
   ...
   return resultado
...


if __name__ == "__main__":
   from pprint import pprint
   from testes import executa_teste

   def testa_procedimento_inicializando():
      inicializando()
      for chave in tabela.keys():
         if type(chave) == str:
            print("chave: %s" % (chave.upper()))
         else:
            print("chave: %i" % chave)
         print(tabela[chave], end="\n\n")
      ...
      assert carregados
   ...

   def testa_funcao_concatena():
      a = tabela['A']
      dois = tabela[2]
      juncao = concatena(a, dois)
      print(juncao)
      juncao = concatena(dois, a)
      print(juncao)
   ...
   # execução em sí.
   executa_teste(testa_procedimento_inicializando)
   executa_teste(testa_funcao_concatena)
...