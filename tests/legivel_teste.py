
# biblioteca padrão do Python:
import random
import string
import time
# importando módulo a testar...
from biblioteca import tamanho, tempo

#trinta importante testes variando de
#maneira aleatório os parâmetros.

_unidade = ['bit','byte']

#formando número aleatório.
def forma_num_aleatorio():
   i,comprimento = 1,random.randint(2, 29)
   numero = ''
   while i <= comprimento:
      posicao_aleatorio = random.randint(0,9)
      numero += string.digits[posicao_aleatorio]
      i+=1
   return numero

for i in range(30):
   numero = int(forma_num_aleatorio())
   print('{0:>15.3g} ==> {1}'.format(numero,tamanho(numero, unidade=random.choice(('byte','bit')),acronomo=bool(random.randint(0,1)),sistema=random.choice(('metrico', 'binario')))))

# testando a legibilidade de tempo.
print(tempo(0.000000000006))
print(tempo(0.000000283))
print(tempo(0.000012))
print(tempo(0.583))
print(tempo(37)) # testando puro.
print(tempo(2005)) # testando um valor maior que um minuto.
print(tempo(56539)) # maior que uma hora.
print(tempo(832321)) # maior que um dia.
print(tempo(15041932)) # possívelmente maior que um mês
print(tempo(127123821))
print(tempo(669988999))
print(tempo(15798411928))
print(tempo(30589812381))
print(tempo(139581111116))


print('tempo até aqui:',end='')
print(tempo(int(time.time())))
