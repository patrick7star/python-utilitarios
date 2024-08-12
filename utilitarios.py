#!/usr/bin/python3 -OB

"""
   Importa todos módulos atualmente importante para aqui, então serão 
exportados. Os códigos dados como "mortos", pois foram criados otimizações, ou descontinuados não serão exportados novamente. Muitos destes módulos 
reescritos com otimizações, ganharão o nome original, e como já dito, 
exportado.
"""

# re-exportando ...
__all__ = [
   "arvore",
   "barra_de_progresso",
   "espiral",
   "legivel",
   "romanos",
   "tela",
   "impressao",
   "aritimetica",
   "tabelas",
   "numeros_por_extenso",
   "texto",
   "tempo"
]

# acessando diretório com códigos...
from sys import path
from os import getenv, system, remove
from os.path import join, abspath, dirname, exists
import tarfile
import enum
from shutil import move, rmtree
from os import rename
from pathlib import Path


# computa o caminho dado para o
# diretório 'source-codes'.
def computa_caminho(restante):
   # Acessa um diretório pai e o diretório "símbolo" contido nele, se e 
   # somente se, está executando o arquivo, e no próprio diretório dele.
   if __name__ == "__main__" == __file__ :
      path = join("../src", restante)
      return abspath(path)
   else:
      # caminho até o arquivo importado.
      raiz = abspath(__file__)
      # strip o arquivo e o diretório localizado.
      raiz = dirname(raiz)
      #path = dirname(path)
      # chega na raíz da 'lib', onde estão não 
      # só este código, mas todos os demais.
      # Então aqui, têm a pasta "símbolos" com
      # todos dados necesários, acessa ele e
      # seus subdirs que são dados como argumento.
      if restante is None:
         return raiz
      else:
         path = join(raiz, restante)
         return path
      ...
   ...
...

if __name__ == "__main__":
   path.append("src/")
else:
   caminho = computa_caminho("src/") 
   print("formado =", caminho)
   path.append(caminho)
...


def compila_todos_projetos() -> None:
   diretorio_lib = Path("lib/")

   if diretorio_lib.exists():
      print("Já está tudo compilado.")
      return None

   print("Compilando todos libs ...")
   system("python3 -m compileall -o 2 src/")
   print("realizado com sucesso.")

   print("Transferindo para o diretório lib/ ...")
   move("src/__pycache__", ".")
   rename ("__pycache__", "lib")
   print("realizada com sucesso.")

   print("Renomeando tais para algo mais legivel ...")
   TRECHO = ".cpython"
   for file in diretorio_lib.iterdir():
      nome_str = str(file.name)
      indice = nome_str.index(TRECHO)
      atual_nome = nome_str[0:indice:1]
      print(file, "====>", atual_nome)

      novo_nome_str = atual_nome + ".pyc"
      novo_nome_path = Path(file.parent, novo_nome_str)
      file.rename(novo_nome_path)
   ...
   
   print("\n\tVeririficando após renomeação ...")
   for file in diretorio_lib.iterdir():
      print("\t\t", '-', file)
...

# Importando...
#import barra_de_progresso(descontinuado)
import src.progresso as progresso
import src.impressao as impressao
import src.espiral as espiral
import src.legivel as legivel
import src.romanos as romanos
# Sendo renomeada com a versão otimizada, pelo menos até o momento.
#import tela_i as tela(descontinuado)
import src.tela as tela
#import arvore_ii as arvore(descontinuado)
import src.arvore as arvore
# import numeros_por_extenso(descontinuado)
import src.extenso as extenso
import src.impressao as impressao
import src.tabelas as tabelas
import src.texto as texto
import src.tempo as tempo
# Não usado muito, então dado como descontinuado.
import src.aritimetica as aritimetica

# verificando diretório com símbolos ...
caminho = computa_caminho("simbolos")
if exists(caminho):
   print("\ndiretório 'símbolos' está ok!")
   # fazendo árvore apenas para ilustração.
   tg = arvore.GalhoTipo.FINO
   print(arvore.arvore(caminho, tipo_de_galho=tg), end='')
else:
   print(
      "não existe diretório 'simbolos', então "
      + "extraindo do arquivo 'simbolos.tar'..."
   )
   caminho_arquivo_tar = computa_caminho("simbolos.tar")

   if exists(caminho_arquivo_tar):
      destino = computa_caminho(None)
      print(arvore.ramifica_caminho(destino))
      """
      if platform == "linux":
         comando = (
            "tar -vx --one-top-level={} -f {}"
            .format(destino, caminho_arquivo_tar)
         )
         system(comando)
      elif platform == "win32":
      """
      archive = tarfile.open(caminho_arquivo_tar)
      archive.extractall(path=computa_caminho(None))
      archive.close()

      print("removendo \"%s\" ..." % caminho_arquivo_tar)
      remove(caminho_arquivo_tar)
   ...
...

# Computa o tipo de dado que é o objeto passado, por exemplo: Classe, 
# Função, Enum, Variável e etc. Retorna uma string informando o tipo.
def qual_o_tipo(objeto):
   tipo = str(type(objeto))
   # proposições.
   e_uma_excecao = (
      "Error" in objeto.__name__ or
      issubclass(objeto.__class__, BaseException)
   )

   if "function" in tipo:
      return "Função"
   elif "class" in tipo:
      if "enum" in tipo:
         return "Enumerador"
      elif e_uma_excecao:
         return "Exceção"
      else:
         return "Classe"
   else:
      print("objeto desconhecido:[%s]"%str(objeto))
      raise Exception("não implementado para tal objeto")
   ...
...

def le_modulo(modulo):
   nome_modulo = modulo.__name__.replace("src.", "")
   print(" Módulo '{}':".format(nome_modulo))

   if __debug__:
      print(modulo.__all__)
      for atributo in modulo.__all__:
         print(getattr(modulo, atributo))

   for item in modulo.__all__:
      tipo = qual_o_tipo(modulo)
      recuo = " " * 4
      seu_tipo = qual_o_tipo(getattr(modulo, item))
      print("{1}{0:.<30}[{2}]".format(item, recuo, seu_tipo))
   # mais uma linha.
   print("")
...

if __name__ == "__main__":
   compila_todos_projetos()

   print("\nImportando módulos ...\n")
   todos_modulos = [
      progresso, legivel, espiral, arvore, romanos, impressao,
      extenso, aritimetica, tempo
   ]
   for modulo in todos_modulos:
      le_modulo(modulo)
...
