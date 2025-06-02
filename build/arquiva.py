"""
   Vou tentar o máximo minimizar o uso de 'makefile' aqui, ao invés, tentarei
 criar um script para cada função que ele iria ter. Como nos makefiles faço
 um comando em tais makefiles para arquivar tal modificação numa nova versão,
 que é algo bem simples lá, este aqui é o arquivo pra isso. 

    Primeiro farei usando uma interface de comandos, posteriormente, irei
 usar realmente a biblioteca e interface interna da linguagem.
"""

from os import (system as SystemCmd, getenv)
from glob import glob
from os.path import (basename)

PYTHON_INTERPLETADOR = "/usr/bin/python3"
NOVA_VERSAO          = "v3.0.1"
NOME_DO_ARQUIVO      = "utilitarios"
REPOSITORIO          = getenv("PYTHON_CODES")
DESTINO              = "{}/versões".format(REPOSITORIO)


def listagem_de_todos_backups_deste_programa() -> None:
   ANTIGOS_BACKUPS = glob("{}/{}*.tar".format(DESTINO, NOME_DO_ARQUIVO))

   print("\nTodas versões de '%s' já realizadas:" % NOME_DO_ARQUIVO)
   for entrada in ANTIGOS_BACKUPS:
      print('\t\b\b-', basename(entrada))
   print("")
   

if REPOSITORIO is None:
   raise OSError("não foi achado a variável que indica o repositório")

listagem_de_todos_backups_deste_programa()
# Forma comando, então executa-o.
SystemCmd(
   "{} -m tarfile -v -c {}/{}.{}.tar *"
   .format(PYTHON_INTERPLETADOR, DESTINO, NOME_DO_ARQUIVO, NOVA_VERSAO)
)
listagem_de_todos_backups_deste_programa()
