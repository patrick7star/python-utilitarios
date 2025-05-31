#!/usr/bin/env python3
"""
   Compila todos bibliotecas, separadamente ou conjunta, e repõe elas no diretório
 correto(o 'lib' no caso aqui).
"""

from os import (mkdir)
from compileall import (compile_dir)
from pathlib import (Path)
from shutil import (rmtree, move)
from glob import (glob)


def recria_diretorios_necessarios() -> None:
    try:
        mkdir("lib")
    except FileExistsError:
        print("Tal diretório 'lib'já existe.")
    finally:
        pass

def compila_todas_bibliotecas() -> None:
    compile_dir(Path("src"), maxlevels=0, optimize=1)

def corrige_nome_e_move_artefatos_pra_lib() -> None:
    todos_artefatos = map(lambda s: Path(s), glob("src/*/*.pyc"))
    PADRAO = ".cpython-312.opt-1"
    temporario = Path("src/__pycache__")

    for caminho in todos_artefatos:
        antigo_nome = str(caminho.name)
        novo_nome = str(antigo_nome).replace(PADRAO, "")
        caminho.rename(Path("lib",novo_nome))

        if __debug__:
            print("'{}' ==> '{}'".format(antigo_nome, novo_nome))
    print("Todos bytes-codes foram devidamente movidos para 'lib'.")
    assert(temporario.exists())
    Path("src/__pycache__").rmdir()
    assert(not temporario.exists())
    print("Removido diretório temporário vázio.")

def extracao_do_tarball_se_necessario() -> None:
   caminho = Path("simbolos.tar")

   if caminho.exists():
      arquivo = TarFile.open(caminho, "r")

      print("Extração de '%s' está sendo ..." % arquivo.name, end=' ')
      arquivo.extractall(Path.cwd())
      print("feito.")
      arquivo.close()
      caminho.unlink()
      assert (not caminho.exists())

# Processo de compilação de vários módulos que compõem a biblioteca. Primeiro,
# cria o diretório de destino, depois compila eles -- pra ser sincero, a 
# ordem destes dois não importa muito, porém será escrito deste modo. O 
# último passo consiste em renomear ambos os bytes-codes no diretório, 
# posteriormente mover-lo para o diretório adequado, que no caso aqui é o 
# 'lib'.
recria_diretorios_necessarios()
compila_todas_bibliotecas()
corrige_nome_e_move_artefatos_pra_lib()
