'''
 O algoritmo lerá arquivos e diretórios
e arquivará o tamanho de cada, a quantidade
de arquivos neles e etc.
'''
from enum import Enum, auto

# o que será importado:
__all__ = (
   # enumeradores:
   "Grandeza",
   "Unidade",
   # funções:
   "tamanho",
   "tempo"
)


# enum's:
class Unidade(Enum):
   BYTE = auto()
   BIT = auto()
...

class Grandeza(Enum):
   METRICO = auto()
   BINARIO = auto()
...

# dicionários dentre de dicionários.
# o primeiro é uma string ligada a um
# mapa, este por sua, vez, outras strings
# ligadas a tupla, que tem vários pares
# de tuplas dentro da mesma. Estas, represetam 
# os pesos usado da função 'tamanho'.
# Está aqui, simplesmente, porque o aninhamento
# dentro da função está uma confusão, ou seja,
# por legibilidade.
PESOS = {
   "byte": {
      "metrico": (
         ('B','byte'), ('KB','kilobyte'),
         ('MB','megabyte'),('GB','gigabyte'),
         ('TB','terabyte'),('PB','petabyte'),
         ('EB','exabyte'),('ZB','zettabyte'),
         ('YB','yottabyte')
      ),
      "binario": (
         ('Bi','byte'),('KiB','kilobyte'),
         ('MiB','megabyte'), ('GiB','gigabyte'),
         ('TiB','terabyte'),('PiB','pebibyte'),
         ('EiB','exibyte'),('ZiB','zebibyte'),
         ('YiB','yobibyte')
      )
   },
   "bit": {
      "metrico": (
         ('Bit','bit'),('Kbit','kilobit'),
         ('Mbit','megabit'),('Gbit','gigabit'),
         ('Tbit','terabit'),('Pbit','petabit'),
         ('Ebit','exabit'),('Zbit','zettabit'),
         ('Ybit','yottabit')
      ),
      "binario": (
         ('Bit','bit'),('Kibit','kilobit'),
         ('Mibit','megabit'),('Gibit','gigabit'),
         ('Tibit','terabit'),('Pibit', 'pebibit'),
         ('Eibit', 'exbibit'),('Zibit', 'zebibit'),
         ('Yibit','yobibit')
      )
   }
}

def tamanho(valor, unidade: Unidade, sistema: Grandeza, 
acronomo=True) -> str:
   '''
   Função que retorna um sufixo com a unidade
   de informação traduzida do melhor modo possível
   de acordo com a informação passada.
   '''
   if unidade == Unidade.BYTE and sistema == Grandeza.METRICO:
      X = valor
      sequencial = PESOS["byte"]["metrico"]
      (x1,x2,dx),(y1,y2,dy) = (0,27,3), (3,30,3)
      base = 10 #muda base
   elif unidade == Unidade.BIT and sistema == Grandeza.METRICO:
      X = 8 * valor
      base = 10 #muda base
      (x1,x2,dx),(y1,y2,dy) = (0,27,3), (3,30,3)
      sequencial = PESOS["bit"]["metrico"]
   elif unidade == Unidade.BIT and sistema == Grandeza.BINARIO:
      X = 8 * valor
      base = 2 #muda base
      (x1,x2,dx),(y1,y2,dy) = (0,90,10),(10,100,10)
      sequencial = PESOS["bit"]["binario"]
   # este último é 'byte' e 'binário'.
   else:
      X = valor
      base = 2 #muda base
      (x1, x2, dx), (y1,y2,dy) = (0,90,10),(10,100,10)
      sequencial = PESOS["byte"]["binario"]
   ...

   #dicionário  contendo todos intervalos de variação
   #e seus respectivos múltiplos para deixar
   #mais legível tal número.
   ordem = {
      (a,b):U for(a,b,U) in zip(
         range(x1,x2,dx),
         range(y1,y2,dy),
         sequencial
      )
   }

   #a - inicio de um valor; b - final do valor; definindo
   #assim o intervalo. Percorrendo o dicionário sendo a
   #chave uma tupla, com valor inicial e final.
   for (a,b) in ordem:
     #escolhe o melhor múltiplo para o valor.
     multiplo = ordem[(a,b)][int(not acronomo)]
     #forma uma string com o valor encolhido
     #a uma escala legível.
     string='{0:0.2f} {1}'.format(X/(base**a),multiplo)
     #se estiver no intervalo existente, então
     #retorna a string combinada com algumas
     #customizações importantes.
     if X >= base**a and X < base**b:
         if X/(base**a) == 1:
            return string
         else:
            return string+'\'s'
     ...
   else:
      return string
   ...
...

# constantes com escalas de tempo, com suas
# equivalências em segundos.
# A coisa dos múltiplos de submúltiplos são
# bem confusos, não seguem o sistema
#métrico... inicialmente!
miliseg = 1 / 1_000
microseg = 1 / 10**6
nanoseg = 1 / 10**9
picoseg = 1 / 10**12
minuto = 60
hora = 60 * minuto
dia =  24 * hora
mes = 30 * dia
ano = 365 * dia
# bem aqui começa o sistema métrico...
decada = 10 * ano
seculo = 10 * decada
milenio = 10 * seculo

# Representar o tempo de forma legível,
# onde converte todos valores passados na
# ordem de segundos para  minutos, horas
# décadas, meses, milisegundos, nanosegundos
# e etc...
def converte(t: int) -> str:
   # múltiplos e sub-múltiplos:
   if t >= picoseg and t < nanoseg:
      grandeza = "picosegundos"
      return '%0.2f %s' % (t * 10**12, grandeza)
   elif t >= nanoseg and t < microseg:
      grandeza = 'nanosegundos'
      return '%0.2f %s' % (t * 10**9, grandeza)
   elif t >= microseg and t < miliseg:
      grandeza = 'microsegundos'
      return '%0.2f %s' % (t * 10**6, grandeza)
   elif t >= miliseg and t < 1:
      grandeza = 'milisegundos'
      return '%0.2f %s' % (t * 1000, grandeza)
   elif t >= 1 and t < 60:
      grandeza = 'segundos'
      return '%0.2f %s' % (t, grandeza)
   elif t > 60 and t < 3600:
      grandeza = 'minutos'
      return '%0.2f %s' % (t / minuto, grandeza)
   elif t >= hora and t < dia:
      grandeza = 'horas'
      return '%0.2f %s' % (t / hora, grandeza)
   elif t >= dia and t < mes:
      return '%0.2f dias'%(t / dia)
   elif t >= mes and t < ano:
      return '%0.2f meses' % (t / mes)
   elif t >= ano and t < decada:
      return '%0.2f anos' % (t / ano)
   elif t >= decada and t < seculo:
      grandeza = 'décadas'
      return '%0.2f %s' % (t / decada, grandeza)
   elif t >= seculo and t < milenio:
      grandeza = 'séculos'
      return '%0.2f %s' % (t / seculo, grandeza)
   elif t >= milenio and t < 10 * milenio:
      grandeza = 'milênios'
      return '%0.2f %s' % (t / milenio, grandeza)
   else:
      raise Exception("não implementado para tal tamanho!")
...

def tempo(segundos, arredonda=False, acronomo=False) -> str:
   """
   conserta o plural em alguns casos, a função
   original é reescrita
   """
   # fazendo a tradução normal.
   tempo_str = converte(segundos)
   # deixa no singular se possível.
   tempo_str = transforma_no_singular(tempo_str)

   if acronomo and (not arredonda):
      return aplica_acronomo(tempo_str, False)
   elif (not acronomo) and arredonda:
      return arredonda_tempostr(tempo_str)
   elif  acronomo and arredonda:
      arredondado = arredonda_tempostr(tempo_str)
      return aplica_acronomo(arredondado, True)
   else:
      return tempo_str
...


# mostra o tempo de forma mais detalhada:
def tempo_detalhado(t):
   string = tempo(t)
   partes = decompoe(string)
   # apelido para simplificar codificação:
   peso = partes["peso"]

   if "minuto" in peso:
      tempo_seg = minuto * partes["fracao"]
      fracao_legivel = tempo(tempo_seg)
   elif "hora" in peso:
      tempo_seg = hora * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "dia" in peso:
      tempo_seg = dia * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "meses" in peso or "mês" in peso:
      tempo_seg = mes * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "ano" in peso:
      tempo_seg = ano * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "década" in peso:
      tempo_seg = decada * partes['fracao']
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "século" in peso:
      tempo_seg = seculo * partes['fracao']
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "milênio" in peso:
      tempo_seg = milenio * partes['fracao']
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   else:
      raise Exception("não implementado para tal ainda!!")
   ...

   # retorno do tempo melhor detelhado.
   return (
      "{} {} {}"
      .format(
         partes["inteiro"],
         partes["peso"],
         fracao_legivel
      )
   )
...

Decomposicao = {str: float, str:int, str:str}
# decompõe em partes a "string de tempo".
def decompoe(tempo_str: str) -> Decomposicao:
   if __debug__:
      # caractére por caractére da string.
      print(tuple(tempo_str.split()))

   partes = tempo_str.split()
   peso = partes.pop()
   valor = partes.pop()
   # objeto desnecessário, acabando com sua vida
   # neste momento, sem qualquer chance para o
   # GB fazer-lô automaticamente.
   del partes

   if __debug__:
      print("valor:\"%s\"" % valor)

   try:
      (inteiro, fracao) = valor.split('.')
      fracao = float('0.' + fracao)
      inteiro = int(inteiro)
   except ValueError:
      fracao = 0
      inteiro = int(valor)
   finally:
      if __debug__:
         # visualizando o que foi obtido.
         print("\nvalor:\"%s\"" % valor)
         print(
            "fração:\"%s\" e inteiro:\"%s\""
            % (fracao, inteiro),
            end = '\n\n'
         )
      ...

   if __debug__:
      print(inteiro, fracao, peso)

   return {
      'fracao': fracao,
      'inteiro': inteiro,
      'peso': peso
   }
...

# pega uma 'conversão' e arredonda sua parte inteira
def arredonda_tempostr(tempo_str):
   partes = decompoe(tempo_str)
   inteiro = partes['inteiro']
   fracao = partes['fracao']
   peso = partes['peso']

   if fracao > 0.5:
      inteiro += 1

   return "{} {}".format(inteiro, peso)
...

# pega uma string já em forma legível
# e encurta seu acrônomo.
def aplica_acronomo(tempo_str, arredonda):
   partes = decompoe(tempo_str)
   (i, f, peso) = (
      partes['inteiro'],
      partes['fracao'],
      partes['peso']
   )
   encostado = False

   if "picosegundo" in peso:
      peso = "ps"
      encostado = True
   elif 'nanosegundo' in peso:
      peso = 'ns'
      encostado = True
   elif "microsegundo" in peso:
      peso = "μs"
      encostado = True
   elif "milisegundo" in peso:
      peso = "ms"
      encostado = True
   elif "segundo" in peso:
      peso = "seg"
   elif "minuto" in peso:
      peso = "min"
   elif "hora" in peso:
      peso = "h"
      encostado = True
   elif "década" in peso:
      peso = 'dec'
   elif "milênio" in peso:
      peso = 'mil'
   ...

   valor = i + f
   espaco = ' '
   if encostado:
      espaco = ''
   if arredonda and f == 0.0:
      return "%i%s%s" % (int(valor), espaco, peso)
   else:
      return "%0.2f%s%s" % (valor, espaco, peso)
...

# transforma 'tempo_str' na forma
# singular, se este for o caso.
def transforma_no_singular(tempo_str):
   # verificando se é o caso que estamos
   # querendo consertar.
   partes = decompoe(tempo_str)
   e_caso_procurado = (
      partes['inteiro'] == 1 and
      partes['fracao'] == 0.0
   )

   if e_caso_procurado:
      # transforma no valor novamente ...
      valor = partes['inteiro'] + partes['fracao']
      # remove o plural.
      tamanho = len(partes['peso'])
      peso = partes['peso'][0:tamanho-1]
      # retornando o valor dirigido no singular.
      return "{} {}" .format(valor, peso)
   else:
      # não é o caso, apenas devolve dado.
      return tempo_str
   ...
...


#from testes import executa_teste
from random import randint
from unittest import (TestCase, main)

# testes unitários:
class Funcoes(TestCase):
   def tempoDetalhado(self):
      # valor e peso filtrado:
      string = tempo_detalhado(1_329)
      print(decompoe(string))
      print("1º ==>", string)
      print("2º ==>", tempo_detalhado(592_319))
      print("3º ==>", tempo_detalhado(52_300))

      # testes aleatorios do novo conversor:
      traducao = tempo_detalhado(1166832000)
      print(traducao)
      self.assertEqual("3 décadas 7 anos", traducao)
      traducao_simples = tempo(1166832000)
      print(traducao_simples, "==>", traducao)
      # outro ...
      traducao = tempo_detalhado(16398720000)
      print(traducao)
      self.assertEqual("5 séculos 2 décadas", traducao)
      traducao_simples = tempo(16398720000)
      print(traducao_simples, "==>", traducao)

      # testando o arredondamento.
      print(tempo(2_000, arredonda=True))
      # testando o arredondamento para segundos.
      print(tempo(37.3, arredonda=True))
      print(tempo(27.83, arredonda=True))
   ...
   def arredondaTempostr(self):
      exemplos = [
         "15.3 horas", "3.7 min", "18 segundos",
         "57.8 dias", "7.8 meses", "14.2 minutos",
         "6.45 horas"
      ]
      for ts in exemplos:
         print(ts, arredonda_tempostr(ts), sep=" ==> ")
   ...
   def tempoComAcronomos(self):
      amostras = [
         31_899, 192, 1_938, 419_203,
         41_283, 3_912_822, 47,
         580_098_523, 92_378_223,
         1_101_283_283, 5_823, 223/1000,
         3/10**6, 28/10**9, 84/10**12
      ]
      for t in amostras:
         normal = tempo(t)
         transforma = tempo(t, acronomo = True)
         print("{} ==> {}".format(normal, transforma))
      ...
   ...
   def runTest(self):
      self.tempoDetalhado()
...
def valor_grande_legivel(numero: int) -> str:
   if numero >= 1_000 and numero < 1_000_000:
      return "{:0.1f} mil".format(numero / 1_000)
   elif  pow(10, 6) <= numero < pow(10, 9):
      return "{:0.1f} mi".format(numero / pow(10, 6))
   elif pow(10, 9) <= numero < pow(10, 12):
      return "{:0.1f} bi".format(numero / pow(10, 9))
   elif pow(10, 12) <= numero < pow(10, 15):
      return "{:0.1f} ti".format(numero / pow(10, 9))
   else:
      return str(numero)
...

def valor_grande_bem_formatado(numero: int) -> str:
   if numero < 1000:
      return str(numero)
   else:
      forma_inicial = str(numero)
      resto = len(forma_inicial) % 3
      forma_inicial = ''.join(['0'*(3 - resto), forma_inicial])
      # fila para armazenar caractéres temporiamente,
      # e string para concatenação.
      fila = []; numero_str = ""
      
      for c in list(forma_inicial):
         fila.append(c)
         # deseja numa classe a formação dos três algs.
         if len(fila) == 3:
            numero_str += ' '
            while len(fila) > 0:
               numero_str += fila.pop(0)
         ...
      ...
      numero_str += ' '
      while len(fila) > 0:
         numero_str += fila.pop(0)
      return numero_str.lstrip('0 ')
   ...
...

if __name__ == "__main__":
   main()
...
