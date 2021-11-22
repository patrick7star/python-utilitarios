
# biblioteca para testes.
import time
from biblioteca import Tela
from biblioteca import range_bidimensional, espiral

coords = range_bidimensional((5,12), 4)

T = Tela(0,0)

for (y,x) in coords:
   T.marca(y,x)

#time.sleep(2.5)  # dois segundos e meio.
T.marca(5, 12,simbolo='O')

for (y,x) in espiral((18,45)):
   T.marca(y,x, simbolo='*')
print(T)

for (linha, coluna) in espiral((6,25)):
   T.marca(linha,coluna, simbolo='O')
   time.sleep(0.1)
   print(T)
