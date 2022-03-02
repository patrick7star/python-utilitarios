
"""
Vamos fazer um novo código para o módulo
'tela', porém mais otmizado em questão
de memória. Aqui vamos testar ele com
o antigo.
Muito do código do "módulo tela" original
será reutilizado nesta nova criação.
"""
from biblioteca import Tela, Ponto, tamanho, Unidade, Grandeza
from biblioteca import TelaOptimizada
from sys import getsizeof
from biblioteca import range_bidimensional, espiral

# métrica padrão para impressão
METRICA_PADRAO = (Unidade.BYTE, Grandeza.METRICO)

tela_i = TelaOptimizada.Tela(10_000, 10_000,borda=True, grade=False)
tela_ii = Tela(10_000, 10_000, borda=True,grade=False)

print(tela_i)
print(tela_ii)

t1 = getsizeof(tela_i)
t2 = getsizeof(tela_ii)
assert t1 < t2
print("tamanho do tela_i: %s" % tamanho(t1, *METRICA_PADRAO))
print("tamanho do tela_ii: %s" % tamanho(t2, *METRICA_PADRAO))

coords = range_bidimensional((5,12), 4)

for (y,x) in espiral((18,45)):
   tela_i.marca(y,x, simbolo='*')
   tela_ii.marca(y,x, simbolo='*')
...

for (y,x) in coords:
   tela_i.marca(y,x)
   tela_ii.marca(y,x)
...

print(tela_i)
print(tela_ii)

t1 = getsizeof(tela_i)
t2 = getsizeof(tela_ii)
assert t1 < t2
print("tamanho do tela_i: %s" % tamanho(t1, *METRICA_PADRAO))
print("tamanho do tela_ii: %s" % tamanho(t2, *METRICA_PADRAO))

