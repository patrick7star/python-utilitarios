
"""
Vamos fazer um novo código para o módulo
'tela', porém mais otmizado em questão
de memória. Aqui vamos testar ele com
o antigo.
Muito do código do "módulo tela" original
será reutilizado nesta nova criação.
"""
#from biblioteca import Tela, Ponto, tamanho, Unidade, Grandeza
#from biblioteca import TelaOptimizada
from sys import getsizeof, path
path.append("..")
# Deste módulo...
from src.legivel import (tamanho, Unidade, Grandeza)
from src.tela import Tela as TelaOptimizada, Ponto
from src.screen.tela_antigo import Tela
from src.espiral import (range_bidimensional, espiral)
#from biblioteca import range_bidimensional, espiral

# métrica padrão para impressão
METRICA_PADRAO = (Unidade.BYTE, Grandeza.METRICO)

ALTURA = 100; LARGURA = 80
tela_old = TelaOptimizada(ALTURA, LARGURA,borda=True, grade=False)
tela_new = Tela(ALTURA, LARGURA, borda=True,grade=False)

print(tela_old)
print(tela_new)

tO = getsizeof(tela_old)
tN = getsizeof(tela_new)
assert tO > tN
print(
   "tamanho do tela_old: %s\ntamanho do tela_new: %s" 
   % (tamanho(tO, *METRICA_PADRAO), tamanho(tN, *METRICA_PADRAO))
)

coords = range_bidimensional((5,12), 4)

for (y,x) in espiral((18,45)):
   pA = Ponto(y, x)
   tela_old.marca(pA, '*')
   tela_new.marca(y,x, simbolo='*')
...

for (y,x) in coords:
   tela_old.marca(Ponto(y, x))
   tela_new.marca(y, x)
...

print(tela_old)
print(tela_new)

tO = getsizeof(tela_old)
tN = getsizeof(tela_new)
assert tO > tN
print(
   "tamanho do tela_old: %s\ntamanho do tela_new: %s" 
   % (tamanho(tO, *METRICA_PADRAO), tamanho(tN, *METRICA_PADRAO))
)

