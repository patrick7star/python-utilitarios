"""
  O código que trabalha na visualização de textos-desenhos ficará aqui
mesmo, na biblioteca utilitários. Só que agora, com um bom conhecimento
de algoritmos o processo para gera-lô pode ser mais reduzido.
"""

# o que será exportado:
__all__ = ["Texto","tabela", "Palavras", "inicializando"]

# biblioteca padrão do Python:
from os import listdir, get_terminal_size
from os.path import basename,join, dirname, abspath, normpath
from sys import platform
from queue import Queue, SimpleQueue
from pathlib import PosixPath
from io import TextIOBase
from pathlib import PosixPath
import tarfile
from pprint import pprint
from time import sleep
from unittest import main, TestCase
from shutil import rmtree
# própria biblioteca:
from tela.tela_objetos import Matriz

# mapa contendo todo alfabeto, dígitos, e pontuações... quase todo
# símbolos na tabela ASCII.
tabela = {}
# verifica os símbolos foram carregados.
CARREGADOS = False

class MatrizTexto(Matriz):
   def __init__(self, altura, largura):
      grade = False
      super().__init__(altura, largura, grade)
   ...

   def dimensao(self):
      """
      retorna tupla com a dimensão, onde primeiro valor é a altura, 
      a segunda é a largura.
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
            # resultado.altera(y, x, char)
            resultado[y][x] = char
         ...
      ...
      for y in range(a_omt):
         for x in range(l_omt):
            char = outra_mt[y][x]
            # resultado.altera(y + a_mt+1, x, char)
            resultado[y + a_mt + 1][x] = char
         ...
      ...

      return resultado
   ...
...

# computa o caminho dado para o diretório símbolos.
def caminho_simbolos(restante) -> PosixPath:
   # acessa um diretório pai e o diretório "símbolo" contido nele, se
   # e somente se, está executando o arquivo, e no próprio diretório
   # dele.
   if __name__ == "__main__" == __file__ :
      path = PosixPath("../simbolos").joinpath(restante)
      # path = join("../simbolos", restante)
      # return abspath(path)
      return path.resolve()
   else:
      # caminho até o arquivo importado.
      # path = abspath(__file__)
      path =PosixPath(__file__).resolve()
      # strip o arquivo e o diretório localizado.
      '''
      path = dirname(path)
      path = dirname(path)
      '''
      path = path.parent
      path = path.parent
      # chega na raíz da 'lib', onde estão não só este código, mas
      # todos os demais. Então aqui, têm a pasta "símbolos" com todos
      # dados necesários, acessa ele e seus subdirs que são dados
      # como argumento.
      ''' 
      path = join(path, "simbolos", restante)
      return path
      '''
      return path.joinpath("simbolos", restante)
   ...
...

def file_to_matriz(arquivo: TextIOBase) -> MatrizTexto:
   linhas = list(arquivo)
   (C, L) = (max(len(l) for l in linhas), len(linhas))
   matriz = MatrizTexto(L, C)

   for (y, linha) in enumerate(linhas):
      for (x, char) in enumerate(linha):
         if char == '\n':
            continue
         matriz[y][x] = char
      ...
   ...
   return matriz
...

def inicializando() -> None:
   # para o programa se não houver os símbolos necessários para
   # a impressão. Se houver apenas um backup dele, realiza a extração
   # no diretório certo. Retorna um valor lógico se já existe o
   # diretório com tudo certo, ou se foi extraído com sucesso.
   assert simbolos_estao_disponiveis()
   # caminhos dos arquivos contendo os "desenhos".
   caminhos_dos_simbolos = [
      # caminho para o diretório com 'alfabeto'.
      caminho_simbolos("alfabeto"),
      # caminho para o diretório com 'números'.
      caminho_simbolos("numeros"),
      # caminho para o diretório com 'pontuações'.
      caminho_simbolos("pontuacao")
   ]

   if __debug__:
      print("alfabetos =", caminhos_dos_simbolos[0])
      print("números =", caminhos_dos_simbolos[1])
      print("pontuação =", caminhos_dos_simbolos[2])
      print("atual diretório '%s'" % PosixPath('.').cwd())
   ...

   # carrega todos arquivos, de todos subdiretórios...
   for caminho in caminhos_dos_simbolos:
      for arquivo in listdir(caminho):
         caminho_arquivo = caminho.joinpath(arquivo)
         chave = arquivo[0:-4]
         if chave.isalpha():
            chave = chave.lower()
         fd = open(caminho_arquivo, "rt", encoding="latin1")
         desenho = file_to_matriz(fd)
         tabela[chave] = desenho
      ...
   ...
   traduz_chaves_incossistentes()
   global CARREGADOS
   CARREGADOS = True
...

# converte nomes de dígitos nos valores em sí.
def nome_to_digito(nome):
   tokens = {
      "zero":0, "um":1, "dois":2, "tres":3, "quatro":4, "cinco":5, 
      "seis":6, "sete":7, "oito":8, "nove":9
   }
   return tokens[nome]
...

# concatena duas matriz-texto.
def concatena(mt1: MatrizTexto, mt2: MatrizTexto):
   (a1, l1) = mt1.dimensao()
   (a2, l2) = mt2.dimensao()
   diferenca = abs(a1-a2)
   # computa maior dimensão
   (altura, largura) = (max(a1, a2), l1 + l2)
   # matriz-texto resultante.
   resultado = MatrizTexto(altura, largura)
   for y in range(a1):
      for x in range(l1):
         char = mt1[y][x]
         if a1 < a2:
            # resultado.altera(y+diferenca, x, char)
            resultado[y + diferenca][x] = char
         else:
            # resultado.altera(y, x, char)
            resultado[y][x] = char
      ...
   ...
   for y in range(a2):
      for x in range(l2):
         char = mt2[y][x]
         if a2 < a1:
            y1 = y + diferenca
         else:
            y1 = y
         # resultado.altera(y1, x + l1, char)
         resultado[y1][x + l1] = char
      ...
   ...
   return resultado
...

def constroi_str(string):
   # se não for carregado ainda os símbolos, então que seja agora.
   if not CARREGADOS:
      inicializando()

   # se houver apenas um símbolo, então apenas entrega a referência/ou
   # cópia por indexação do mapa..
   if len(string) == 1:
      return tabela[string]
   ...

   # A fila se explica por os caractéres são lidos da esquerda à
   # direita. E têm que ser formados assim também, ou seja, o primeiro
   # a ser lido, será também o primeiro formado(FIFO).
   fila = SimpleQueue()
   for char in string:
      matriz_texto = tabela[char]
      fila.put(matriz_texto)
   ...

   # o algoritmo é o seguinte, remove o primeiro e o usa como base para
   # concatenação do segundo, pegando o resultado o usa como base para
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
   def __init__(self, frase: str) -> None:
      # para futuras indexação do objeto.
      indice = 0
      # lista de palavras.
      self._palavras = []

      # todas chaves na tabela tem apenas letras minúsculas.
      for palavra in frase.lower().split():
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

   def __str__(self) -> str:
      raise Exception("ainda não terminado!")
      indice = self._posicao_atual
      palavras = self._palavras
      return "Palavras({}, '{}')".format(indice, palavras[indice])
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

def simbolos_estao_disponiveis() -> bool:
   diretorio_com_simbolos = PosixPath("../simbolos/")
   arquivo_de_extracao = PosixPath("../simbolos.tar")

   if (
     not diretorio_com_simbolos.exists() and
     not arquivo_de_extracao.exists()
   ):
      print("o diretório 'símbolos' e o arquivo 'tar' com eles inexistem aqui.")
      return False
   elif (
     not diretorio_com_simbolos.exists()
     and arquivo_de_extracao.exists()
   ):
      print("o diretório 'símbolos' inexiste aqui, porém o arquivo 'tar' contendo tais diretórios e subdiretórios existem, extraindo...")
      pacote = tarfile.open(arquivo_de_extracao)
      pacote.extractall("..")
      pacote.close()
      print("'simbolos.tar' removido após extração.")
      return True
   else:
      print("a existência do diretório 'símbolos já é o suficiente.'")
      return diretorio_com_simbolos.exists()
...

def equivalente(nome_do_desenho: str) -> chr:
   match nome_do_desenho:
      # primeira parte os números:
      case "um": return '1'
      case 'dois': return '2'
      case "tres": return '3'
      case "zero": return '0'
      case 'quatro': return '4'
      case "cinco": return '5'
      case 'seis': return '6'
      case "sete": return '7'
      case "oito": return '8'
      case "nove": return '9'
      # limitadores:
      case "abre_colchetes": return '['
      case "fecha_colchetes": return ']'
      case "abre_parenteses": return '('
      case "fecha_parenteses": return ')'
      case "abre_chaves": return '{'
      case "fecha_chaves": return '}'
      # segunda parte a pontuação:
      case "ponto": return '.'
      case "interrogacao": return '?'
      case "exclamacao": return '!'
      case "virgula": return ','
      case "dois_pontos": return ':'
      case "ponto_virgula": return ';'
      # operações matemáticas, ou símbolos referentes:
      case "mais": return '+'
      case "traco": return '-'
      case "asterisco": return '*'
      case "slash": return '*'
      case "igual": return '='
      case "maior_que": return '>'
      case "menor_que": return '<'
      case "porcentagem": return '%'
      case "arroba": return '@'
      # outros que fica difícil de classificar:
      case "cifrao": return '$'
      case _:
         return 'não-trabalhados'
         # raise Exception("caractére com desenho inexistente!")
   ...
...

def traduz_chaves_incossistentes() -> None:
   # traduz chaves inconssistentes...
   lista_de_exclusao = []

   for atual_chave in tabela.keys():
      # casos já formatados normalmente, letras, são passadas, já que 
      # não precisam de qualquer reprocessamento.
      if (len(atual_chave) == 1) and (atual_chave.isalpha()):
         continue
      lista_de_exclusao.append((atual_chave, equivalente(atual_chave)))
   ...

   # trocando nomes das chaves.
   for (velha, nova) in lista_de_exclusao:
      tabela[nova] = tabela[velha]
      del tabela[velha]
   ...
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

class Classes(TestCase):
   def setUp(self):
      print("extraindo o diretório necessário...", end='')
      inicializando()
      print("feito!")

   def tearDown(self):
      print("removendo diretório extraido...", end="")
      rmtree("../simbolos")
      print("feito!")
   ...

   def inicializacao_sucedida(self):
      for chave in tabela.keys():
         if type(chave) == str:
            print("chave: %s" % (chave.upper()))
         else:
            print("chave: %i" % chave)
         print(tabela[chave], end="\n\n")
      ...
      assert CARREGADOS
      self.assertTrue(CARREGADOS)
   ...

   def classe_palavras(self):
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

   def classe_texto(self):
      t = Texto("visual code is a worst than i thought before use it")
      print(t)
      assert True
   ...
...


if __name__ == "__main__":
   main()
