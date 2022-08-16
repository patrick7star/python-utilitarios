
"""
O código que trabalha na visualização 
de textos-desenhos ficará aqui mesmo,
na biblioteca utilitários. Só que agora,
com um bom conhecimento de algoritmos
o processo para gera-lô pode ser mais
reduzido.
"""

# biblioteca padrão do Python:
from os import listdir, get_terminal_size
from os.path import basename,join, dirname, abspath, normpath
from sys import platform
from queue import Queue, SimpleQueue
# própria biblioteca:
from tela_objetos import Matriz


# mapa contendo todo alfabeto, dígitos,
# e pontuações... quase todo símbolos
# na tabela ASCII.
tabela = {}
# verifica os símbolos foram carregados.
CARREGADOS = False
# caractéres equivalente aos seguintes
# nomes de arquivos.
EQUIVALENTE = (
   ('(', "abre_aspas_duplas"),
   (':', "dois_pontos"),
   ('-', "traco"),
   ('=', "traco"),
   ('/', "slash")
)

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

   def concatena_vertical(self, outra_mt):
      (a_omt, l_omt) = outra_mt.dimensao()
      (a_mt, l_mt) = self.dimensao()
      altura = a_omt + a_mt
      largura = max(l_mt, l_omt)
      # nova matriz-texto que embarca ambas.
      resultado = MatrizTexto(altura + 1, largura)

      # posicionando cada nos seus devidos lugares.
      for y in range(a_mt):
         for x in range(l_mt):
            char = self[y][x]
            resultado.altera(y, x, char)
         ...
      ...
      for y in range(a_omt):
         for x in range(l_omt):
            char = outra_mt[y][x]
            resultado.altera(y + a_mt+1, x, char)
         ...
      ... 

      return resultado
   ...
...

# computa o caminho dado para o
# diretório símbolos.
def caminho_simbolos(restante):
   # acessa um diretório pai e o diretório
   # "símbolo" contido nele, se e somente se,
   # está executando o arquivo, e no próprio
   # diretório dele.
   if __name__ == "__main__" == __file__ :
      path = join("../simbolos", restante)
      return abspath(path)
   else:
      # caminho até o arquivo importado.
      path = abspath(__file__)
      # strip o arquivo e o diretório localizado.
      path = dirname(path)
      path = dirname(path)
      # chega na raíz da 'lib', onde estão não 
      # só este código, mas todos os demais.
      # Então aqui, têm a pasta "símbolos" com
      # todos dados necesários, acessa ele e
      # seus subdirs que são dados como argumento.
      path = join(path, "simbolos", restante)
      return path
   ...
...

def file_to_matriz(arquivo):
   linhas = list(arquivo)
   qtd_col = max(len(l) for l in linhas)
   qtd_lin = len(linhas)
   matriz = MatrizTexto(qtd_lin, qtd_col)
   for (y, linha) in enumerate(linhas):
      for (x, char) in enumerate(linha):
         if char == '\n':
            continue
         matriz.altera(y, x, char)
      ...
   ...
   return matriz
...

def inicializando():
   # caminhos dos arquivos contendo os "desenhos".
   caminho_alfabeto = caminho_simbolos("alfabeto")
   caminho_numeros = caminho_simbolos("numeros")
   caminho_pontuacao = caminho_simbolos("pontuacao")

   for arquivo in listdir(caminho_alfabeto):
      caminho = join(caminho_alfabeto, arquivo)
      chave = arquivo[0:-4].lower()
      desenho = file_to_matriz(open(caminho, "rt"))
      tabela[chave] = desenho
   ...

   # carregando números:
   for arquivo in listdir(caminho_numeros):
      caminho = join(caminho_numeros, arquivo)
      chave = str(nome_to_digito(arquivo[0:-4]))
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
   global CARREGADOS
   CARREGADOS = True
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
   largura = l1 + l2
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
         if a2 < a1:
            y1 = y + diferenca
         else:
            y1 = y
         resultado.altera(y1, x + l1, char)
      ...
   ...
   return resultado
...


def traduz_chave(char):
   for tupla in EQUIVALENTE:
      if tupla[0] == char:
         return tupla[1]
   ...
   return char
...

def constroi_str(string):
   # se não for carregado ainda os símbolos,
   # então que seja agora.
   if not CARREGADOS:
      inicializando()

   # se houver apenas um símbolo, então
   # apenas entrega a referência/ou cópia
   # por indexação do mapa..
   if len(string) == 1:
      chave = traduz_chave(string)
      return tabela[chave]
   ...

   # A fila se explica por os caractéres
   # são lidos da esquerda à direita. E
   # têm que ser formados assim também,
   # ou seja, o primeiro a ser lido, será
   # também o primeiro formado(FIFO).
   fila = SimpleQueue()
   for char in string:
      matriz_texto = tabela[traduz_chave(char)]
      fila.put(matriz_texto)
   ...

   # o algoritmo é o seguinte, remove o primeiro
   # e o usa como base para concatenação do segundo,
   # pegando o resultado o usa como base para 
   # demais concatenações até a fila acabar.
   remocao = fila.get()
   resultado = remocao
   while not fila.empty():
      nova_remocao = fila.get()
      resultado = concatena(resultado, nova_remocao)
   ...
   return resultado
...

class Palavras:
   "iterador de palavras e demais dados ao formar a frase"
   def __init__(self, frase):
      # para futuras indexação do objeto.
      indice = 0
      # lista de palavras.
      self._palavras = []
      

      for palavra in frase.split():
         texto_desenho = constroi_str(palavra)
         info = (texto_desenho, palavra, indice)
         indice += 1
         self._palavras.append(info)
      ...
   ...

   def __iter__(self):
      # atributo para a iteração da lista.
      self._posicao_atual = 0
      # retorna própria referência do objeto.
      return self
   ...

   def __next__(self):
      indice = self._posicao_atual
      ultimo = len(self._palavras) - 1

      if indice <= ultimo:
         info = self._palavras[indice]
         self._posicao_atual += 1
         return info
      else:
         raise StopIteration()
   ...

   def __contains__(self, string):
      for (_, palavra, _) in self._palavras:
         if string == palavra:
            return True
      ...
      return False
   ...

   def __len__(self):
      return len(self._palavras)
   
   def __getitem__(self, indice):
      for (mt, s, i) in self._palavras:
         if indice == i:
            return (mt, s)
      ...
      # não existe tal índice.
      raise IndexError()
   ...
...

def clona_fila(fila):
   fila_clone = Queue()
   qtd = fila.qsize()
   while qtd > 0:
      remocao = fila.get()
      fila_clone.put(remocao)
      fila.put(remocao)
      qtd -= 1
   ...
   return fila_clone
...

def concatena_vertical(mt1, mt2):
   largura = max(l_mt1, l_mt2)
   altura = a_mt1 + a_mt2 + 1
...

class Texto:
   def __init__(self, texto, align=None):
      self._palavras = Palavras(texto)
      self._linhas = Queue()
      self._limite_tela = (get_terminal_size().columns - 1)
      # alinhamento inicial do texto.
      self._alinhamento = align
      # texto uma vez formado é para ser
      # colocado neste atributo. Para que 
      # evite consumo de CPU futuramente para
      # se computar o mesmo texto. Tal atributo
      # será apenas modificado se 'alinhamento'
      # ou 'largura da tela' mudarem.
      self._texto = None
      # divide a palavras de acordo com
      # o limite do terminal.
      self._separa_em_linhas()
   ...

   # separa as palavras iteradas em linhas.
   def _separa_em_linhas(self):
      (acumulado, linha) = (0, [])
      terminal_largura = get_terminal_size().columns
      for (mt, _, i) in self._palavras:
         (_, largura) = mt.dimensao()
         acumulado += (largura + 3)

         if acumulado > self._limite_tela:
            self._linhas.put(tuple(linha))
            linha.clear()
            acumulado = largura
         ...
         # adicionará apenas o cabível.
         linha.append(i)
      ...
      if len(linha) > 0:
         self._linhas.put(tuple(linha))
   ...

   def __str__(self):
      if self._texto is not None:
         return str(self._texto)
      
      # começa todo processo de concatenação ...
      espaco = MatrizTexto(4, 3)
      linhas = SimpleQueue()
      # processo de concatenação horizontal.
      (n, base) = (1, None)
      while not self._linhas.empty():
         item = self._linhas.get()
         for indice in item:
            palavra = self._palavras[indice][0]
            if base is None:
               base = concatena(palavra, espaco)
            else:
               base = concatena(base, palavra)
               # adiciona espaço no fim, se e somente
               # se, não é a última palavra da 
               # iteração de 'linha'.
               if base != item[-1]:
                  base = concatena(base, espaco)
            ...
         ...
         linhas.put(base)
         base = None
      ...
      # agora o processo de concatenação vertical.
      self._texto = linhas.get()
      while not linhas.empty():
         item = linhas.get()
         self._texto = self._texto.concatena_vertical(item)
      ...

      # matrix-texto para string.
      return str(self._texto)
   ...
...

# o que será importado.
__all__ = ["constroi_str"]


if __name__ == "__main__":
   from pprint import pprint
   from testes import executa_teste
   from time import sleep

   def testa_procedimento_inicializando():
      inicializando()
      for chave in tabela.keys():
         if type(chave) == str:
            print("chave: %s" % (chave.upper()))
         else:
            print("chave: %i" % chave)
         print(tabela[chave], end="\n\n")
      ...
      assert CARREGADOS
   ...

   def testa_funcao_concatena():
      a = tabela['a']
      dois = tabela['2']
      juncao = concatena(a, dois)
      print(juncao)
      juncao = concatena(dois, a)
      print(juncao)
   ...

   def teste_de_constroi_str():
      texto_desenho = constroi_str("bigorna")
      print(texto_desenho)
      texto_desenho = constroi_str("pe")
      print(texto_desenho)
      texto_desenho = constroi_str("k")
      print(texto_desenho)
      texto_desenho = constroi_str("casa-de-queijo")
      print(texto_desenho)
      texto_desenho = constroi_str("13/04")
      print(texto_desenho)
      texto_desenho = constroi_str("08:38:52")
      print(texto_desenho)
   ...

   def testa_classe_palavras():
      objeto = Palavras(
         "there she goes there she goes " +
         "again and for you my friend " +
         "refrain you know"
      )
      for palavra in objeto:
         print(palavra)
         print(palavra[0])
         sleep(1.5)
      ...
      assert "there" in objeto
      assert "my" in objeto
      assert not("out" in objeto)
      assert len(objeto) == 15
      assert objeto[5][1] == "goes"
      assert objeto[11][1] == "friend"
   ...

   def teste_classe_texto():
      t = Texto("visual code is a worst than i thought before use it")
      print(t)
   ...

   # execução em sí.
   executa_teste(
      testa_procedimento_inicializando,
      testa_funcao_concatena,
      teste_de_constroi_str,
      testa_classe_palavras,
      teste_classe_texto
   )
...
