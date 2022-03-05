
# biblioteca padrão do Python:
import random
import string
import time
# importando módulo a testar...
from biblioteca import *

#trinta importante testes variando de
#maneira aleatório os parâmetros.


#formando número aleatório.
def forma_num_aleatorio():
   i,comprimento = 1,random.randint(2, 29)
   numero = ''
   while i <= comprimento:
      posicao_aleatorio = random.randint(0,9)
      numero += string.digits[posicao_aleatorio]
      i+=1
   ...
   return int(numero)
...

print("\nmostrando de várias possibilidades a opção da função:")
for i in range(30):
   n = forma_num_aleatorio()
   u = random.choice(list(Unidade))
   s = random.choice(list(Grandeza))
   valor_legivel = tamanho(n, u, s)
   print('{0:>15.3g} ==> {1}'.format(n,valor_legivel))
...

# mostrando as duas grandezas ...
print("\nambas grandezas visualizadas, lado à lado:")
for i in range(30):
   n = forma_num_aleatorio()
   u = random.choice(list(Unidade))
   v1 = tamanho(n, u, Grandeza.BINARIO)
   v2 = tamanho(n, u, Grandeza.METRICO)
   print('{0:10.3g} ==> {1}\tou\t{2}'.format(n,v1, v2))
...

# rótulos inteiros e acronômos:
print("\nvisualizando sem usar acronômos em ambas gradezas")
# primeiro binário:
print("BINÁRIO:");
for y in map(lambda x: 2**x, range(1, 83)):
   u = random.choice(list(Unidade))
   v2 = tamanho(y, u, Grandeza.BINARIO, acronomo=False)
   v1 = tamanho(y, u, Grandeza.BINARIO)
   print("{:>18}  ou  {}".format(v1, v2))
...
print("MÉTRICO:");
for y in map(lambda x: 10**x, range(1, 30)):
   u = random.choice(list(Unidade))
   v2 = tamanho(y, u, Grandeza.METRICO, acronomo=False)
   v1 = tamanho(y, u, Grandeza.METRICO)
   print("{:>18}  ou  {}".format(v1, v2))
...

# testando a legibilidade de tempo.
print("\ntodos rótulos adequados de tempo:")
recuo = ' '*5
print(recuo,tempo(0.000000000006))
print(recuo,tempo(0.000000283))
print(recuo,tempo(0.000012))
print(recuo,tempo(0.583))
print(recuo,tempo(37)) # testando puro.
print(recuo,tempo(2005)) # testando um valor maior que um minuto.
print(recuo,tempo(56539)) # maior que uma hora.
print(recuo,tempo(832321)) # maior que um dia.
print(recuo,tempo(15041932)) # possívelmente maior que um mês
print(recuo,tempo(127123821))
print(recuo,tempo(669988999))
print(recuo,tempo(30589812381))
print(recuo,tempo(139581111116))

t = tempo(int(time.time()))
print('\ndecorrido desde a criação do UNIX:', t, end='\n')
