
"""
Aqui vamos importar toda a biblioteca para
que possamos utilizar para fazer testes
do nosso código.
"""

from sys import path
# adicionando diretório com 'biblioteca'
# para que módulos possam ser importados...
path.append("../src/")

# o que será importado tudo:
from tela import *
from espiral import *
from romanos import *
from silhueta import *
import numeros_por_extenso as NE
from arvore import *
from aritimetica import *
from barra_de_progresso import *
from legivel import *
# otimizações:
import tela_i as tela_otimizada
import arvore_ii

# removendo desnessários...
del path

# verificando que objetos foram importado...
if __name__ == "__main__":
   print("\ntudo que será importado:")
   for obj in dir():
      # anulando obj defaults da linguagem.
      obj_e_valido = (
         not obj.startswith("__") and
         not obj.endswith("__")
      )
      if obj_e_valido:
         print("  - {}".format(obj))
      ...
   ...
   print("")
