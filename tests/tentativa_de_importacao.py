"""
   Verificando como fica a importação deste 'import package'. Apesar de tal
 diretório está dentro dele, está totalmente fora do escopo de importação,
 então funciona do mesmo modo se estiver em qualquer outro diretório do home.
"""

from utilitarios.legivel import (tempo, tamanho, Unidade, Grandeza)
from random import randint

for _ in range(randint(10, 15)):
   X = randint(81_851, 4_318_822)
   print(
      '\t\b\b', X, " ===> ", tempo(X), '|', 
      tamanho(X, Unidade.BIT, Grandeza.METRICO)
   )


import utilitarios.romanos

for _ in range(randint(3, 9)):
   In = randint(1, 999)
   Out = utilitarios.romanos.decimal_para_romano(X)
   
   print(In, "===>", Out)
