"""
  Método que carrega símbolos, estes agora mais concatenados do que o modo
anterior, que toma diretórios e subdiretórios, cada um com dezenas de 
arquivos.
"""

# O que será exportado:
__all__ = ["tabela_de_desenhos", "MatrizTexto", "Lados"]

from unittest import (TestCase)
from pathlib import (Path)
from typing import Type
from array import (array as Array)
from src.tela import (Matriz, Lados)
from os import (getenv)

# Apelido da classe:
MT = Type['MatrizTexto']


class MatrizTexto(Matriz):
   def __init__(self, altura, largura):
      # Tenta algo como pontilhado em modo debuggin.
      #grade = __debug__ if False else True
      grade = False
      super().__init__(altura, largura, grade)

   def dimensao(self):
      """
      retorna tupla com a dimensão, onde primeiro valor é a altura, 
      a segunda é a largura.
      """
      qtd_cols = len(self._linhas[0])
      qtd_lins = len(self._linhas)
      return (qtd_lins, qtd_cols)

   @staticmethod
   def concatena_vertical(a: MT, b: MT) -> MT:
      (bH, bL) = b.dimensao()
      (aH, aL) = a.dimensao()
      # nova matriz-texto que embarca ambas.
      resultado = MatrizTexto(aH + bH + 1, max(aL, bL))

      # posicionando cada nos seus devidos lugares.
      for y in range(aH):
         for x in range(aL):
            char = a[y][x]
            resultado[y][x] = char

      for y in range(bH):
         for x in range(bL):
            char = b[y][x]
            resultado[y + aH + 1][x] = char

      return resultado

   @staticmethod
   def concatena_horizontal(mt1: MT, mt2: MT) -> MT: 
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

      for y in range(a2):
         for x in range(l2):
            char = mt2[y][x]
            if a2 < a1:
               y1 = y + diferenca
            else:
               y1 = y
            # resultado.altera(y1, x + l1, char)
            resultado[y1][x + l1] = char

      return resultado

   def __add__(self, obj: MT) -> MT:
      return MatrizTexto.concatena_horizontal(self, obj)

   def __iadd__(self, obj: MT) -> MT:
      return MatrizTexto.concatena_horizontal(self, obj)

   def __ior__(self, obj: MT) -> MT:
      return MatrizTexto.concatena_vertical(self, obj)

   def __or__(a: MT, b: MT) -> MT:
      return MatrizTexto.concatena_vertical(a, b)

   def __str__(self) -> str:
      fitas = []; partes = []
      (Lin, Col) = self.dimensao()

      for i in range(0, Lin):
         for j in range(0, Col):
            partes.append(self[i][j])

         a = "".join(partes)
         a = a.rjust(Col, '\u9639')

         fitas.append(a)
         partes.clear()

      return "\n".join(fitas)
   
   @staticmethod
   def espaco_caractere() -> MT:
      return MatrizTexto(7, 2)
   
   @staticmethod
   def espaco_palavra() -> MT:
      return MatrizTexto(7, 5)

   def sobe_desenho(self):
      """
      Move figura na sua própria grade, na direção vertical, pra cima. Se 
      não for feita cuidadosamente, ou com tal inteção, é possível que tal 
      operação corte a figura.
      """
      (LINS, COLS) = self.dimensao()
      # Linha branca no comprimento da atual figura.
      LINHA_EM_BRANCO = Array('u', COLS * ' ')

      if LINS == 1:
         raise Exception("Não é possível subir a matriz")

      # Coloca a linha vázia no final da matriz, então retira uma do começo.
      # Observe que, se não for feito com medida pode cortar uma parte do
      # desenho.
      self._linhas.append(LINHA_EM_BRANCO) 
      self._linhas.pop(0)

   def desce_desenho(self):
      "Move figura pra baixo, na sua própria grade."
      (LINS, COLS) = self.dimensao()
      LINHA_EM_BRANCO = Array('u', COLS * ' ')

      if LINS == 1:
         raise Exception("não é possível mover figura verticalmente")

      # Operação inversa da 'subida', portanto coloca uma linha no começo, 
      # e retira uma do fim para equilibrar a dimensão. A observação também
      # continua válida, se não for feito com cautela, o desenho será 
      # cortado.
      self._linhas.insert(0, LINHA_EM_BRANCO)
      self._linhas.pop()

def aglomerado_de_linhas_do_arquivo(caminho: Path) -> [str]:
   LINHA_EM_BRANCO = "\n\n"

   with open(caminho, mode="rt") as arquivo:
      conteudo = arquivo.read()
      trechos = conteudo.split(LINHA_EM_BRANCO)
      # Adicionando simples quebra-de-linha na string do final da lista.
      # Isso para manter uma certa simetria, é importante em futuros 
      # algoritmos que processe tal tipo de dado.
      trechos = [s + '\n' for s in trechos]

      return trechos

def extrai_o_alfabeto() -> {str: [str]}:
   try:
      caminho = Path("simbolos/alfabeto.txt")
      lista = aglomerado_de_linhas_do_arquivo(caminho)
   except FileNotFoundError:
      caminho = Path(getenv("SIMBOLOS_DO_TEXTO"))
      caminho = caminho.joinpath("alfabeto.txt")

      assert (caminho.exists())
      assert (caminho.is_file())

      lista = aglomerado_de_linhas_do_arquivo(caminho)
   finally:
      a = ord('A'); z = ord('Z')
      letras = map(lambda code: chr(code), range(a, z))

   return { 
      letra: desenho 
      for (letra, desenho) in zip(letras, lista) 
   }

def extrai_os_digitos() -> {str: [str]}:
   try:
      caminho = Path("simbolos/números.txt")
      lista = aglomerado_de_linhas_do_arquivo(caminho)
   except FileNotFoundError:
      caminho = Path(getenv("SIMBOLOS_DO_TEXTO"))
      caminho = caminho.joinpath("números.txt")

      assert (caminho is not None)
      assert (caminho.exists())

      lista = aglomerado_de_linhas_do_arquivo(caminho)
   finally:
      numeros = range(0, 10)

   return { digito: desenho for (digito, desenho) in zip(numeros, lista) }

def extrai_a_pontuacao() -> {str: [str]}:
   try:
      caminho = Path("simbolos/pontuação.txt")
      lista = aglomerado_de_linhas_do_arquivo(caminho)
   except FileNotFoundError:
      caminho = Path(getenv("SIMBOLOS_DO_TEXTO"))
      caminho = caminho.joinpath("pontuação.txt")

      assert (caminho is not None)
      assert (caminho.exists())

      lista = aglomerado_de_linhas_do_arquivo(caminho)
   finally:
      pontuacao = [
         '{', '[', '(', '@', '*', '\\', '$', '^', ':', '!', '}', ']', ')'
         , '=', '?', '>', '+', '<', '.', ';', '%', '/', '~', '-', '#', ','
      ]

   if __debug__:
      print(zip(pontuacao, lista))

   return { sym: draw for (sym, draw) in zip(pontuacao, lista) }

def string_to_matriz(string: str) -> MatrizTexto:
   fitas    = string.splitlines()
   Lin      = string.count('\n')
   Col      = max(len(s) for s in fitas)
   matriz   = MatrizTexto(Lin, Col)

   for (y, linha) in enumerate(fitas):
      for (x, simbolo) in enumerate(linha):
            matriz[y][x] = simbolo

   return matriz

def tabela_de_desenhos() -> dict[str: MatrizTexto]:
   alfabeto = extrai_o_alfabeto()
   digitos = extrai_os_digitos()
   pontuacao = extrai_a_pontuacao()

   # Corrigindo as chaves dos dígitos, convertendo elas para string.
   digitos = {str(key): value for (key, value) in digitos.items() }

   # Despeja todos num mesmo dicionário.
   output = (alfabeto | digitos | pontuacao)
   # Convertendo seus valores em matrizes ...
   for key in output.keys():
      desenho = output[key]
      matriz_desenho = string_to_matriz(desenho)
      output[key] = matriz_desenho

   return output


class Unitarios(TestCase):
   def setUp(self):
      self.TABLE = tabela_de_desenhos()

   def tearDown(self):
      print("Tabela de desenhos liberada")
      del self.TABLE

   def separacao_do_conteudo_baseado_em_linhas_brancas(self):
      caminho = Path("simbolos/números.txt")
      output = aglomerado_de_linhas_do_arquivo(caminho)

      print("Listagem de cada símbolo:")
      for letra in output:
         print(letra, end="\n\n")

   def organizacao_do_conteudo_extraido(self):
      output_alphabet = extrai_o_alfabeto()
      output_digits = extrai_os_digitos()
      output_spelling = extrai_a_pontuacao()

      print(
         output_alphabet['M'], output_alphabet['B'], output_alphabet['N'],
         output_alphabet['T'], output_alphabet['G'], output_alphabet['I'],
         sep="\n\n"
      )

      print(
         output_digits[5], output_digits[1], output_digits[9],
         output_digits[8], output_digits[0], output_digits[2],
         sep="\n\n"
      )

      print(
         output_spelling[':'], output_spelling['%'], output_spelling['?'],
         output_spelling['='], output_spelling[';'], output_spelling['!'],
         output_spelling['+'], output_spelling['<'], output_spelling['$'],
         sep="\n\n"
      )

   def transformacao_de_um_desenho_numa_matriz(self):
      table = extrai_o_alfabeto()
      divisivel_por_dez = (lambda x: x % 5 == 0)

      for (ordem, key) in enumerate(table.keys()):
         print("\nChave('{}')".format(key))
         In = table[key]

         if divisivel_por_dez(ordem):
            print("Desenho antes: \n{}".format(In))

         Out = string_to_matriz(In)

         if divisivel_por_dez(ordem):
            print("Matriz disso:\n{}\n".format(Out))

   def resultado_final_do_pipeline(self):
      tabela = tabela_de_desenhos()

      print("Iterando todos objetos alocados:")
      for (chave, desenho) in tabela.items():
         print(
            "\nChave utilizada('{}'):\n"
            .format(chave), desenho, end='\n\n', sep=''
         )

   def concatenacoes_e_seus_atalhos(self):
      In_a = self.TABLE['A']
      In_b = self.TABLE['O']
      In_c = self.TABLE['?']
      ESPACO = MatrizTexto.espaco_caractere()

      Out = (In_a + ESPACO + In_b + ESPACO + In_c) 

      Out += ESPACO
      Out += self.TABLE['F']
      Out += ESPACO
      Out += self.TABLE['N']

      Out |= (self.TABLE['@'] + ESPACO + self.TABLE['3'] + self.TABLE['D'])

      print(Out, end= '\n\n\n')
      print(Out | (self.TABLE['G'] + self.TABLE['8']))
      print("\n\nSem alteração:\n", Out, end= '\n\n\n')
      pass

