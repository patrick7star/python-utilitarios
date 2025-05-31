"""
  As vezes a extração de tal biblioteca é feita com um nome diferente do seu
 suposto: 'utilitarios'. Então, este script tem como proposito criar um 
 linque simbólico com seu nome para este 'package import' ao seu lado, no 
 diretório que esteja; isso é claro, se não tiver o nome correto. Ele também
 tem uma função para renomear-lo se for preciso para este nome, qualquer 
 opção é válida, e estará disponível.
"""

from pathlib import (Path, )
from os import (chdir as ChangeDir)

CAMINHO_SCRIPT = Path(__file__)
DIR_PROJETO    = CAMINHO_SCRIPT.parent.parent
PACKAGE_IMPORT = DIR_PROJETO.name

if __debug__:
   print("Caminho: '%s'" % str(CAMINHO_SCRIPT))
   print("Diretório do projeto:", DIR_PROJETO)
   print("Nome do projeto:", PACKAGE_IMPORT)


nome_corresponde = (
   PACKAGE_IMPORT == "utilitarios" or
   PACKAGE_IMPORT == "utils"
)
print("Nome do pacote bate, 'utilitarios'?", nome_corresponde)
ChangeDir(CAMINHO_SCRIPT.parent)
DIR_VIZINHO = DIR_PROJETO.parent
print("Estou no diretório '%s' agora." % (str(DIR_VIZINHO.name)))
FONTE_DO_LINK = DIR_VIZINHO.joinpath("utilitarios")
FONTE_DO_LINK.symlink_to(DIR_PROJETO)
