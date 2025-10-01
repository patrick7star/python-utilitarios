"""
   Extrai os dígitos que formam os números do arquivo compactado dentro do
 diretório raíz do projeto.
   Como o arquivo 'build.py' deixou de ser um código-fonte pra se tornar um
 diretório, ele abrigará todas suas antigas funções em vários arquivos de 
 script que fazem a mesma coisa, porém de modo mais separado.
"""

from tarfile import *
from pathlib import Path


def extracao_do_tarball_se_necessario() -> None:
   caminho = Path("símbolos.tar")

   if caminho.exists():
      arquivo = TarFile.open(caminho, "r")

      print("Extração de '%s' está sendo ..." % arquivo.name, end=' ')
      arquivo.extractall(Path.cwd())
      print("feito.")
      arquivo.close()
      caminho.unlink()
      assert (not caminho.exists())


# Extrai símbolos do 'tarball'.
extracao_do_tarball_se_necessario()
