
# biblioteca padrão do Python:
import random
import string
import time
from unittest import TestCase, main
# importando módulo a testar...
from sys import path
path.append("../../src/")
from legivel import *

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

class Tamanho(TestCase):
   def AmostraAleatoria(self):
      print("\nmostrando de várias possibilidades a opção da função:")
      for i in range(30):
         n = forma_num_aleatorio()
         u = random.choice(list(Unidade))
         s = random.choice(list(Grandeza))
         valor_legivel = tamanho(n, u, s)
         print('{0:>15.3g} ==> {1}'.format(n,valor_legivel))
      ...
   ...
   # mostrando as duas grandezas ...
   def ComparacaoDosModos(self):
      print("\nambas grandezas visualizadas, lado à lado:")
      for i in range(30):
         n = forma_num_aleatorio()
         u = random.choice(list(Unidade))
         v1 = tamanho(n, u, Grandeza.BINARIO)
         v2 = tamanho(n, u, Grandeza.METRICO)
         print('{0:10.3g} ==> {1}\tou\t{2}'.format(n,v1, v2))
      ...
   ...
   # rótulos inteiros e acronômos:
   def SemEncurtamento(self):
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
   ...
...

class Tempo(TestCase):
   def variasEntradas(self):
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
      self.assertTrue(True)
   ...

   def tempoDoUnix(self):
      print(
         '\ndecorrido desde a criação do UNIX:',
         tempo(int(time.time())), end='\n'
      )
      self.assertTrue(True)
   ...
...

if __name__ == "__main__":
   main(verbosity=2)
