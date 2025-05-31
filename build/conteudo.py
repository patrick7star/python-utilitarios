#!/usr/bin/python3 -OB

"""
   Importa todos módulos atualmente importante para aqui, então serão 
 exportados. Os códigos dados como "mortos", pois foram criados otimizações, 
 ou descontinuados não serão exportados novamente. Muitos destes módulos 
 reescritos com otimizações, ganharão o nome original, e como já dito, 
 exportado.
"""

# Re-exportando ...
__all__ = [
   "arvore",
   "progresso",
   "espiral",
   "legivel",
   "romanos",
   "tela",
   "impressao",
   "aritimetica",
   #"tabelas",
   "extenso",
   "texto",
   "tempo"
]

# Acessando diretório com códigos...
from sys import path
from os import getenv, system, remove
from os.path import join, abspath, dirname, exists
import enum, sys
from pathlib import Path

# Tentando importar...
try:
   import progresso 
   import impressao 
   import espiral  
   import legivel 
   from utiltarios import romanos
   # Sendo renomeada com a versão otimizada, pelo menos até o momento.
   import src.tela         as tela
   import src.arvore       as arvore
   import src.extenso      as extenso
   import src.impressao    as impressao
   #import src.tabelas as tabelas
   import src.texto        as texto
   import src.tempo        as tempo
   # Não usado muito, então dado como descontinuado.
   import src.aritimetica  as aritimetica
except ModuleNotFoundError:
   print(
      "Provavelmente o módulo não foi encontrado por que isso é uma "   +
      "biblioteca externa, e pra reduzir a cadeia de árquivos ele foi " +
      "bastante reduzido, ao menos aqueles arquivos(módulos) que não "  + 
      "tem depedencia de cadeia"
   )


# Computa o tipo de dado que é o objeto passado, por exemplo: Classe, 
# Função, Enum, Variável e etc. Retorna uma string informando o tipo.
def qual_o_tipo(objeto):
   tipo = str(type(objeto))

   try:
      nome_do_obj = objeto.__name__
   except AttributeError:
      nome_do_obj = "Nenhum"
   finally: pass

   # proposições.
   e_uma_excecao = (
      "Error" in nome_do_obj or
      issubclass(objeto.__class__, BaseException)
   )

   if "function" in tipo:
      return "Função"
   elif "class" in tipo:
      if "enum" in tipo:
         return "Enumerador"
      elif e_uma_excecao:
         return "Exceção"
      elif ("int" in tipo) or ("float" in tipo) or ("str" in tipo):
         return "Constante"
      else:
         return "Classe"
   else:
      print("objeto desconhecido:[%s]"%str(objeto))
      raise Exception("não implementado para tal objeto")
   ...
...

def listagem_do_modulo(modulo):
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

def todos_modulos_importados_manualmente() -> list:
   """
   Extrai todos módulos manuais importados aqui. Assim não será preciso
   listar as bibliotecas que foram importadas acima.
   """
   # A extração de tais módulos será automática.
   return list(map(
      # Apenas extrai o módulo, o nome pode ser obtido novamente.
      lambda tupla: sys.modules[tupla[1]],
      filter(
        # A filtragem aqui leva em consideração se há um segundo
        # sub-diretório, se houver então descarta. Aqui será apenas 
        # considerado os módulos em 'src'.
        lambda tupla: len(tupla[1].split('.')) == 2,
        filter(
          # Filtra baseado se tem o nome 'src' nele.
          lambda tupla: "src" in tupla[1],
          # Guarda numa tupla o módulo e seu nome em string, respectivamente.
          map(lambda mod: (mod, str(mod)), sys.modules)
   ))))


if __name__ == "__main__":
   MODULOS_EXTRAIDOS = todos_modulos_importados_manualmente()

   if __debug__:
      print("\nO que será visualizado ...")
      for modulo in MODULOS_EXTRAIDOS: 
         print("\t\b\b-", modulo.__name__)

   print("\nImportando módulos ...\n")

   for In in MODULOS_EXTRAIDOS:
      try:
         listagem_do_modulo(In)
      except AttributeError:
         print(
            "__all__ não foi definido para %s. Talvez não sejá uma "
            "biblioteca válida." % In.__name__, end="\n\n"
         )
...
