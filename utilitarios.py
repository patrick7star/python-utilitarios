
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
path.append("src/")

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
#import aritmetica

# re-exportando ...
__all__ = [
   "arvore",
   "barra_de_progresso",
   "espiral",
   "legivel",
   "romanos",
   "tela",
   "impressao"
]

def le_modulo(modulo):
   print("módulo \"{}\":".format(modulo.__name__))
   for item in modulo.__all__:
      print("{1}{0}".format(item, " " * 4))
   ...
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
      numeros_por_extenso
   ]
   for modulo in todos_modulos:
      le_modulo(modulo)
...