"""
   Vou tentar o máximo minimizar o uso de 'makefile' aqui, ao invés, tentarei
 criar um script para cada função que ele iria ter. Como nos makefiles faço
 um comando em tais makefiles para arquivar tal modificação numa nova versão,
 que é algo bem simples lá, este aqui é o arquivo pra isso.

    Primeiro farei usando uma interface de comandos, posteriormente, irei
 usar realmente a biblioteca e interface interna da linguagem.
"""

from os import (system as SystemCmd, getenv as GetEnv)
from glob import glob
from os.path import (basename, abspath)

PYTHON_INTERPLETADOR = "/usr/bin/python3"
NOVA_VERSAO          = "v3.0.1"
NOME_DO_ARQUIVO      = "utilitarios"
REPOSITORIO          = GetEnv("PYTHON_CODES")
DESTINO              = "{}/versões".format(REPOSITORIO)


def listagem_de_todos_backups_deste_programa() -> None:
   ANTIGOS_BACKUPS = glob("{}/{}*.tar".format(DESTINO, NOME_DO_ARQUIVO))

   print("\nTodas versões de '%s' já realizadas:" % NOME_DO_ARQUIVO)
   for entrada in ANTIGOS_BACKUPS:
      print('\t\b\b-', basename(entrada))
   print("")

def impressao_dos_simbolos_arquivados(programa: str, nome: str) -> None:
   print("\nTudo que foi arquivado:")
   SystemCmd("%s -m tarfile -l %s.tar" % (programa, nome))
   print("", end='\n\n')

def salva_pacotes_de_simbolos() -> None:
   NOME_DO_ARQUIVO = "símbolos"
   FONTE = "./simbolos"
   processo = SystemCmd(
      # A saída é dispensada, uma própria será criada.
      "{} -m tarfile -v -c {}.tar {} > /dev/null"
      .format(PYTHON_INTERPLETADOR, NOME_DO_ARQUIVO, FONTE)
   )

   print("Atual diretório: '%s'" % abspath("."))
   if processo == 0:
      impressao_dos_simbolos_arquivados(PYTHON_INTERPLETADOR, NOME_DO_ARQUIVO)
      print("'%s' foi arquivado com sucesso." % NOME_DO_ARQUIVO)
   else:
      print("Falhar ao arquivar '%s'!" % NOME_DO_ARQUIVO)

def arquiva_toda_biblioteca() -> None:
   # Impresssão antes da execução para comparação posteriormente.
   listagem_de_todos_backups_deste_programa()
   # Executa a arquivação, então pega o resultado(status) dela.
   result = SystemCmd(
      "{} -m tarfile -v -c {}/{}.{}.tar * > /dev/null"
      .format(PYTHON_INTERPLETADOR, DESTINO, NOME_DO_ARQUIVO, NOVA_VERSAO)
   )

   if result == 0:
      print("Arquivação da biblioteca feita com sucesso.")
      listagem_de_todos_backups_deste_programa()
   else:
      print("Houve algum erro ao tentar-lá arquivar!")
   print("", end='\n\n')

if REPOSITORIO is None:
   raise OSError("não foi achado a variável que indica o repositório")

# Forma comando, então executa-o.
if REPOSITORIO is None:
   var = 'REPOSITORIO'
   raise OsError("O ambiente não tem tal variável '%s' definida. Defina!" % var)

arquiva_toda_biblioteca()
salva_pacotes_de_simbolos()
