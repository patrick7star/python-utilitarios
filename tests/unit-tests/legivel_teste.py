
# biblioteca padrão do Python:
import random
import string
import time
from unittest import (TestCase, main, skip)
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
   @skip("teste ainda não finalizado")
   def casosPluraisESingulares(self):
      # testando valores no plural e singular:
      print(tempo(1_300))
      print(tempo(1))
      print(tempo(3_600))
      print(tempo(3_631))
      # testando com arredondamento.
      print(tempo(1_300, arredonda=True))
      print(tempo(1, arredonda=True))
      print(tempo(3_600, arredonda=True))
      print(tempo(3_631, arredonda=True))
   ...
   @skip("teste ainda não finalizado")
   def tempoAcronomosEArredondamentos(self):
      from random import randint
      entradas = [
         31_899, 192,
         1_938, 419_203,
         41_283, 3_912_822, 47,
         580_098_523, 92_378_223,
         1_101_283_283, 5_823, 223/1000,
      ]
      # seguinte esquema: tupla, onde o primeiro
      # é o resultado normal; o segundo é arrendodado
      # sem encurtadomento; e o último ambas variações
      # acima
      saidas = [
         ("8.86 horas", "8.86 horas", "9.0 h"),
         ("3.2 minutos", "3.0 minutos", "3.0 min")
      ]
      for (s, t) in zip(saidas, entradas):
         randomico = bool(randint(0, 1))
         normal = tempo(t)
         arredondado_sem_acronomo = tempo(t, arredonda=randomico)
         encurtado = tempo(t, arredonda=randomico,acronomo=True)
         self.assertEqual(normal, s[0])
         self.assertEqual(arredondado_sem_acronomo, s[1])
         self.assertEqual(encurtado, s[2])
         print(
            normal,
            arredondado_sem_acronomo,
            encurtado,
            sep = " ==> "
         )
      ...
      amostras = [ 3/10**6, 28/10**9, 84/10**12 ]
      for t in amostras:
         randomico = bool(randint(0, 1))
         normal = tempo(t)
         arredondado_sem_acronomo = tempo(t, arredonda=randomico)
         encurtado = tempo(t, arredonda=randomico,acronomo=True)
         print(
            normal,
            arredondado_sem_acronomo,
            encurtado,
            sep = " ==> "
         )
      ...
   ...
...

if __name__ == "__main__":
   main(verbosity=2)
