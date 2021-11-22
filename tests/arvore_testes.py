#!/usr/bin/python3 -O

# biblioteca padrão do Python:
import os, sys, time
# importando módulos a testar:
from biblioteca import alterna_galho, GalhoTipo, arvore

"""
o teste abaixo funciona apenas em
plataforma linux; e se tiver os
diretórios/sub-diretórios explicitados.
"""

if sys.platform == "linux":
   """
   testando protótipos de funções que funcionam
   apenas no módulo, e não podem ser importados
   para não ficar entulhando tudo que já tem.
   """
   print("esboço em como foi construído o projeto:")
   no_modulo = os.system("python3 -B ../lib/arvore.py")
   # tempo para visualizar o resultado.
   if __debug__:
      time.sleep(5)

   # mudando expessura do galho.
   alterna_galho(GalhoTipo.FINO)

   nucleo = os.getenv("HOME") + "/Documents"
   if __debug__:
      print("\no que saí: \"%s\""%nucleo)

   caminho = nucleo + '/códigos'
   print(arvore(caminho))
   print(arvore(caminho, True))
