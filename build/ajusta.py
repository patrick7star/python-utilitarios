"""
   Algoritmo ajusta o código pra ser um package-import in Python. Assim, 
 poderia importar os programas, apenas acessando o nome do projeto, no caso
 aqui é 'utilitarios', então o módulo, então o conteúdo dentro dele. No
 geral, este algoritmo apenas tirar os códigos da pasta 'src', e adiciona
 um '__init__.py' prá torna-lo package-import.
"""
from pathlib import (Path)
from os import (chdir as ChangeDir)
from collections.abc import (Iterator)
from glob import (glob)


def conta_iteracao(I: Iterator) -> int:
   contagem = 0

   while True:
      try:
         next(I)
         contagem += 1
      except StopIteration:
         break
      else: pass
      finally: pass

   return contagem

def ha_conteudo_dentro_de_source() -> bool:
   "Diz se o diretório existe, e se há conteúdo dentro dele."
   fonte = Path("./src")
   quantia = conta_iteracao(fonte.iterdir())

   return (fonte.exists() and quantia > 0)

def cria_arquivo_init() -> None:
   with open("__init__.py", "w"):
      print("Arquivo 'init.py' criado na base.")

def realiza_operacoes_de_mover() -> None:
   diretorio_base = Path.cwd()
   NOME_PROJETO = "python-utilitarios"

   if diretorio_base.name != NOME_PROJETO:
      mensagem = (
         "Só é possível executar tal script no diretório "
         + "'python-utilitarios'"
      )
      raise NotADirectoryError(mensagem)

   if __debug__:
      print("Atual diretório: %s" % diretorio_base)
   print ("Realizando o movimento de conteúdo ...")

   for caminho in glob("./src/*"):
      caminho = Path(caminho)
      destino = diretorio_base
      fonte = caminho

      shutil.move(fonte, destino)

      if caminho.is_dir():
         print("\t\b\b\b- %s/ movido." % (caminho.name))
      else:
         print("\t\b\b\b- %s movido." % (caminho.name))

   diretorio_base.joinpath("src").rmdir()
   cria_arquivo_init()

#+========================================================================+
#                          Testes Unitários
#+========================================================================+
from unittest import (TestCase, expectedFailure)
import shutil
from os import (rename)

class HaConteudoDentroDeSource(TestCase):
   def runTest(self):
      print("Há uma pasta 'src'? %s" % ha_conteudo_dentro_de_source())

class RealizaOperacoesDeMover(TestCase):
   def setUp(self):
      """
        Realiza um backup do diretório a ser mexido, assim é possível mudar
      apenas está cópia, e no final, restaurar o inicial.
      """
      # Coloca um novo nome no original.
      self.antigo = Path("./src/")
      self.novo = Path("./src-backup/")

      rename(self.antigo, self.novo)
      # Faz uma cópia deste backup, com o nome original. Tudo no mesmo
      # diretório.  Observe que como não há mais 'src', porque acabou de
      # de ser renomeada para 'src-backup'; então posso simplesmente 
      # fazer um novo backup usando o nome antigo('src').
      shutil.copytree(self.novo, self.antigo)

   def tearDown(self):
      """
        Restaura o backup. Neste estágio, a versão 'src' já foi removida
      pelo o algoritmo, restando apenas 'src-backup', então transformo
      novamente ele em apenas 'src'.
      """
      self.assertFalse(self.antigo.exists())
      # Aplica o reverso. Portanto, troca pro antigo nome. Claro, é preciso
      # que a outra diretório, à cópia, não exista mais.
      rename(self.novo, self.antigo)

   def runTest(self):
      realiza_operacoes_de_mover()

@expectedFailure
class NaoPossivelExecutarAqui(TestCase):
   def runTest(self):
      nova_base = Path("build")
      print("Diretório atual: %s" % Path.cwd())
      ChangeDir(nova_base)
      print("Diretório atual: %s" % Path.cwd())
      realiza_operacoes_de_mover()

#+========================================================================+
#                          Execução do Script
#+========================================================================+
if __name__ == "__main__":
   ha_conteudo_dentro_de_source()
   realiza_operacoes_de_mover()
