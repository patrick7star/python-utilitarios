
"""
importa todos módulos atualmente importante
para aqui, então serão exportados. Os códigos
dados como "mortos", pois foram criados
otimizações, ou descontinuados não serão
exportados novamente. Muitos destes módulos
reescritos com otimizações, ganharão o nome
original, e como já dito, exportado.
"""


# acessando diretório com códigos...
from sys import path
from os import getenv
from os.path import join
if __name__ == "__main__":
   path.append("src/")
else:
   caminho = join(
      getenv("HOME"),
      "Documents",
      "python-utilitarios",
      "src"
   )
...

# importando...
import barra_de_progresso
import impressao
import espiral
import legivel
import romanos
# sendo renomeada com a versão otimizada,
# pelo menos até o momento.
import tela_i as tela
import arvore_ii as arvore
import numeros_por_extenso
import testes
import impressao
# não usado muito, então dado como
# descontinuado.
import aritimetica
import tabelas

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
   "testes",
   "tabelas",
   "numeros_por_extenso"
]

# computa o tipo de dado que é 
# o objeto passado, por exemplo:
# Classe, Função, Enum, Variável
# e etc. Retorna uma string 
# informando o tipo.
import enum
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
   nome_modulo = modulo.__name__
   print("módulo \"{}\":".format(nome_modulo))

   if __debug__:
      print(modulo.__all__)
      for atributo in modulo.__all__:
         print(getattr(modulo, atributo))

   for item in modulo.__all__:
      tipo = qual_o_tipo(modulo)
      recuo = " " * 4
      seu_tipo = qual_o_tipo(getattr(modulo, item))
      print("{1}{0}[{2}]".format(item, recuo, seu_tipo))
   # mais uma linha.
   print("")
...

if __name__ == "__main__":
   print("\nimportando módulos ...\n")
   todos_modulos = [
      barra_de_progresso,
      legivel, espiral,
      arvore, romanos,
      tela, impressao, testes,
      numeros_por_extenso,
      tabelas, aritimetica
   ]
   for modulo in todos_modulos:
      le_modulo(modulo)
...
