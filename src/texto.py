"""
  O código que trabalha na visualização de textos-desenhos ficará aqui
mesmo, na biblioteca utilitários. Só que agora, com um bom conhecimento
de algoritmos o processo para gera-lô pode ser mais reduzido.
"""

# O que será exportado:
__all__ = [
   "constroi_str", "Texto", "tabela", "Palavras", "inicializando",
   "MatrizTexto", "Lados"
]

# Biblioteca padrão do Python:
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
from shutil import rmtree
# Própria biblioteca:
from text.inicializacao import (tabela_de_desenhos, MatrizTexto, Lados)

# Mapa contendo todo alfabeto, dígitos, e pontuações... quase todo
# símbolos na tabela ASCII.
tabela = {}
# Verifica os símbolos foram carregados.
CARREGADOS = False


def inicializando() -> None:
   global tabela, CARREGADOS

   tabela = tabela_de_desenhos()
   CARREGADOS = True

def constroi_str(string: str) -> MatrizTexto:
   """
   Constrói um desenho da string pura, portanto o retorno será uma 'matriz
   texto', algo que não é muito manipulável ou interativo.
   """
   # se não for carregado ainda os símbolos, então que seja agora.
   if not CARREGADOS:
      inicializando()

   # se houver apenas um símbolo, então apenas entrega a referência/ou
   # cópia por indexação do mapa..
   if len(string) == 1:
      return tabela[string]

   # A fila se explica por os caractéres são lidos da esquerda à
   # direita. E têm que ser formados assim também, ou seja, o primeiro
   # a ser lido, será também o primeiro formado(FIFO).
   fila = SimpleQueue()

   for char in string:
      matriz_texto = tabela[char]
      fila.put(matriz_texto)

   # o algoritmo é o seguinte, remove o primeiro e o usa como base para
   # concatenação do segundo, pegando o resultado o usa como base para
   # demais concatenações até a fila acabar.
   remocao = fila.get()
   resultado = remocao
   ESPACO = MatrizTexto.espaco_caractere()

   while not fila.empty():
      nova_remocao = fila.get()
      # resultado = concatena(resultado, nova_remocao)
      resultado = resultado + ESPACO + nova_remocao

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
         texto_desenho = constroi_str(palavra.upper())
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

   def __str__(self):
      if self._texto is not None:
         return str(self._texto)

      # começa todo processo de concatenação ...
      #espaco = MatrizTexto(4, 3)
      ESPACO = MatrizTexto.espaco_palavra()
      linhas = SimpleQueue()
      # processo de concatenação horizontal.
      (n, base) = (1, None)

      while not self._linhas.empty():
         item = self._linhas.get()
         for indice in item:
            palavra = self._palavras[indice][0]

            if base is None:
               #base = concatena(palavra, espaco)
               base = palavra + ESPACO
            else:
               # base = concatena(base, palavra)
               base = base + palavra
               # Adiciona espaço no fim, se e somente se, não é a última 
               # palavra da iteração de 'linha'.
               if base != item[-1]:
                  #base = concatena(base, espaco)
                  base = base +  ESPACO

         linhas.put(base)
         base = None

      # agora o processo de concatenação vertical.
      self._texto = linhas.get()
      while not linhas.empty():
         item = linhas.get()
         #self._texto = self._texto.concatena_vertical(item)
         self._texto = self._texto | item

      # matrix-texto para string.
      return str(self._texto)
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

# == == == == == == == == == == == === == == == == == == == == == == == ===
#                          Testes Unitários 
# == == == == == == == == == == == === == == == == == == == == == == == ===
from unittest import main, TestCase

class Unitarios(TestCase):
   def setUp(self):
      print("extraindo o diretório necessário...", end='')
      inicializando()
      print("feito!")

   def tearDown(self):
      print("removendo diretório extraido...", end="")
      #rmtree("../simbolos")
      print("feito!")


   def inicializacao_sucedida(self):
      for chave in tabela.keys():
         if type(chave) == str:
            print("chave: %s" % (chave.upper()))
         else:
            print("chave: %i" % chave)
         print(tabela[chave], end="\n\n")

      assert CARREGADOS
      self.assertTrue(CARREGADOS)

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

   def classe_texto(self):
      t = Texto(
         "visual code is worster than i thought before use it." +
         " You dont think either?!"
      )
      print(t)
      assert True

class InicializacaoSucedida(TestCase):
   def setUp(self):
      print("extraindo o diretório necessário...", end='')
      inicializando()
      print("feito!")

   def tearDown(self):
      print("removendo diretório extraido...", end="")
      #rmtree("../simbolos")
      print("feito!")

   def runTest(self):
      for chave in tabela.keys():
         if type(chave) == str:
            print("chave: %s" % (chave.upper()))
         else:
            print("chave: %i" % chave)
         print(tabela[chave], end="\n\n")

      assert CARREGADOS
      self.assertTrue(CARREGADOS)

class ClassePalavras(TestCase):
   def setUp(self):
      print("extraindo o diretório necessário...", end='')
      inicializando()
      print("feito!")

   def tearDown(self):
      print("removendo diretório extraido...", end="")
      #rmtree("../simbolos")
      print("feito!")

   def runTest(self):
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

class ClasseTexto(ClassePalavras):
   def runTest(self):
      t = Texto(
         "visual code is worster than i thought before use it." +
         " You dont think either?!"
      )
      print(t)
      assert True

class FuncaoConstroiStr(TestCase):
   """
   Todo o processo de construção de um relógio. Portanto, um exemplo simples
   de como usar a função 'constroi_str'.
   """
   def construcao_de_strings(self):
      sample = ["bigorna", "pe", "k", "casa-do-queijo", "13/04", "08:38:52"]

      for In in sample:
         Out = constroi_str(In.upper())
         print(Out)

   def formato_do_horario(self):
      sep = FuncaoConstroiStr.dois_pontos_centralizado()
      obj = constroi_str("19") + sep + constroi_str("39")
      print(obj)

   def formatacao_de_todos_digitos(self):
      print(constroi_str("0987654321"))

   def dois_pontos_centralizado() -> MatrizTexto:
      BRANCO = MatrizTexto.espaco_caractere()
      sep = constroi_str(":")

      sep.margem(2, Lados.INFERIOR)
      sep.margem(2, Lados.DIREITO)

      return BRANCO + sep 

   def subida_de_dois_pontos(self):
      horas = constroi_str("48")
      minutos = constroi_str("10")
      segundos = constroi_str("27")
      separador = FuncaoConstroiStr.dois_pontos_centralizado()

      print(horas + separador + minutos + separador + segundos)

   def runTest(self):
      self.subida_de_dois_pontos()

if __name__ == "__main__":
   main()
