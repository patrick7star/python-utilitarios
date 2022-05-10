'''
 O algoritmo lerá arquivos e diretórios
e arquivará o tamanho de cada, a quantidade
de arquivos neles e etc.
'''
from enum import Enum, auto

# enum's:
class Unidade(Enum):
   BYTE = auto()
   BIT = auto()
...

class Grandeza(Enum):
   METRICO = auto()
   BINARIO = auto()
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


# *** *** *** funções *** *** ***

#[código morto]
def tamanho(valor, *, unidade, acronomo, sistema):
   '''
   Função que retorna um sufixo com a unidade
   de informação traduzida do melhor modo possível
   de acordo com a informação passada.
   '''
   if unidade.lower() == 'byte':
      X = valor
      if sistema.lower() == 'metrico':
         sequencial = (('B','byte'), ('KB','kilobyte'),
                      ('MB','megabyte'),('GB','gigabyte'),
                      ('TB','terabyte'),('PB','petabyte'),
                      ('EB','exabyte'),('ZB','zettabyte'),
                      ('YB','yottabyte'))
         (x1,x2,dx),(y1,y2,dy) = (0,27,3), (3,30,3)
         base = 10 #muda base
      else:
         sequencial = (('Bi','byte'),('KiB','kilobyte'),
                     ('MiB','megabyte'), ('GiB','gigabyte'),
                     ('TiB','terabyte'),('PiB','pebibyte'),
                     ('EiB','exibyte'),('ZiB','zebibyte'),
                     ('YiB','yobibyte'))
         (x1, x2, dx), (y1,y2,dy) = (0,90,10),(10,100,10)
         base = 2 #muda base

   elif unidade.lower() == 'bit':
      X = 8 * valor
      if sistema.lower() == 'metrico':
         sequencial = (('Bit','bit'),('Kbit','kilobit'),
                     ('Mbit','megabit'),('Gbit','gigabit'),
                     ('Tbit','terabit'),('Pbit','petabit'),
                     ('Ebit','exabit'),('Zbit','zettabit'),
                     ('Ybit','yottabit'))
         base = 10 #muda base
         (x1,x2,dx),(y1,y2,dy) = (0,27,3), (3,30,3)
      else:
         sequencial = (('Bit','bit'),('Kibit','kilobit'),
                     ('Mibit','megabit'),('Gibit','gigabit'),
                     ('Tibit','terabit'),('Pibit', 'pebibit'),
                     ('Eibit', 'exbibit'),('Zibit', 'zebibit'),
                     ('Yibit','yobibit'))
         base = 2 #muda base
         (x1,x2,dx),(y1,y2,dy) = (0,90,10),(10,100,10)

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
   for a,b in ordem:
     #escolhe o melhor múltiplo para o valor.
     multiplo = ordem[(a,b)][int(not acronomo)]
     #forma uma string com o valor encolhido
     #a uma escala legível.
     string='{0:0.2f} {1}'.format(X/(base**a),multiplo)
     #se estiver no intervalo existente, então
     #retorna a string combinada com algumas
     #customizações importantes.
     if X >= base**a and X < base**b:
         if X/(base**a) == 1: return string
         else: return string+'\'s'
   else: return string
...

def tempo_auxiliarI(t, arredonda=False, acronomo=False):
   '''
   Representar o tempo de forma legível,
   "legendando" o resultado com os acronimos de
   segundos, minutos e horas e etc...'''

   # múltiplos e sub-múltiplos:
   if t >= picoseg and t < nanoseg:
      if arredonda:
         return '%i picosegundos' % (int(t * 10**12))
      else:
         return '%0.2f picosegundos' % (t * 10**12)
   elif t >= nanoseg and t < microseg:
      if arredonda:
         return '%i nanosegundos' % (int(t * 10**9))
      else:
         return '%0.2f nanosegundos' % (t * 10**9)
   elif t >= microseg and t < miliseg:
      if arredonda:
         return '%i microsegundos' % (int(t * 10**6))
      else:
         return '%0.2f microsegundos' % (t * 10**6)
   elif t >= miliseg and t < 1:
      if arredonda:
         return '%i milisegundos' % (int(t * 10**3))
      else:
         return '%0.2f milisegundos' % (t * 10**3)
   elif t >= 1 and t < 60:
      if acronomo:
         grandeza = 'seg'
      else:
         grandeza = 'segundos'
      if arredonda:
         return '%i %s' % (int(t), grandeza)
      return '%0.2f %s' % (t, grandeza)
   elif t > 60 and t < 3600:
      if arredonda:
         return '%i minutos' % (t // minuto)
      else:
         return '%0.2f minutos' % (t / minuto)
   elif t >= hora and t < dia:
      if arredonda:
         return '%i horas' % (t // hora)
      else:
         return '%0.2f horas' % (t / hora)
   elif t >= dia and t < mes:
      if arredonda:
         return '%i dias'%(t // dia)
      else:
         return '%0.2f dias'%(t / dia)
   elif t >= mes and t < ano:
      if arredonda:
         return '%i meses' % (t // mes)
      else:
         return '%0.2f meses' % (t / mes)
   elif t >= ano and t < decada:
      if arredonda:
         return '%i anos' % (t // ano)
      else:
         return '%0.2f anos' % (t / ano)
   elif t >= decada and t < seculo:
      if arredonda:
         return '%i décadas' % (t // decada)
      else:
         return '%0.2f décadas' % (t / decada)
   elif t >= seculo and t < milenio:
      if arredonda:
         return '%i séculos' % (t // seculo)
      else:
         return '%0.2f séculos' % (t / seculo)
   elif t >= milenio and t < 10 * milenio:
      if arredonda:
         return '%i milênios' %(t // milenio)
      else:
         return '%0.2f milênios' %(t / milenio)
   else:
      raise Exception("não implementado para tal tamanho!")
...

def tempo(segundos, arredonda=False, acronomo=False):
   """
   conserta o plural em alguns casos, a função 
   original é reescrita
   """
   # fazendo a tradução normal.
   tempo_str = tempo_auxiliarI(
      segundos,
      arredonda = arredonda,
      acronomo = acronomo
   )
   # decompondo em partes.
   partes = decompoe(tempo_str)

   # verificando se é o caso que estamos 
   # querendo consertar.
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
      return ( "{} {}" .format(valor, peso))
   else:
      # neste caso, apenas retorna o original
      # obtido.
      return tempo_str
   ...
...

def tamanho(valor, unidade, sistema, acronomo=True):
   '''
   Função que retorna um sufixo com a unidade
   de informação traduzida do melhor modo possível
   de acordo com a informação passada.
   '''
   if unidade == Unidade.BYTE and sistema == Grandeza.METRICO:
      X = valor
      sequencial = (
         ('B','byte'), ('KB','kilobyte'),
         ('MB','megabyte'),('GB','gigabyte'),
         ('TB','terabyte'),('PB','petabyte'),
         ('EB','exabyte'),('ZB','zettabyte'),
         ('YB','yottabyte')
      )
      (x1,x2,dx),(y1,y2,dy) = (0,27,3), (3,30,3)
      base = 10 #muda base
   elif unidade == Unidade.BIT and sistema == Grandeza.METRICO:
      X = 8 * valor
      base = 10 #muda base
      (x1,x2,dx),(y1,y2,dy) = (0,27,3), (3,30,3)
      sequencial = (
         ('Bit','bit'),('Kbit','kilobit'),
         ('Mbit','megabit'),('Gbit','gigabit'),
         ('Tbit','terabit'),('Pbit','petabit'),
         ('Ebit','exabit'),('Zbit','zettabit'),
         ('Ybit','yottabit')
      )
   elif unidade == Unidade.BIT and sistema == Grandeza.BINARIO:
      X = 8 * valor
      base = 2 #muda base
      (x1,x2,dx),(y1,y2,dy) = (0,90,10),(10,100,10)
      sequencial = (
         ('Bit','bit'),('Kibit','kilobit'),
         ('Mibit','megabit'),('Gibit','gigabit'),
         ('Tibit','terabit'),('Pibit', 'pebibit'),
         ('Eibit', 'exbibit'),('Zibit', 'zebibit'),
         ('Yibit','yobibit')
      )
   #elif unidade == Unidade.BYTE and sistema == Grandeza.BINARIO:
   else:
      X = valor
      base = 2 #muda base
      (x1, x2, dx), (y1,y2,dy) = (0,90,10),(10,100,10)
      sequencial = (
         ('Bi','byte'),('KiB','kilobyte'),
         ('MiB','megabyte'), ('GiB','gigabyte'),
         ('TiB','terabyte'),('PiB','pebibyte'),
         ('EiB','exibyte'),('ZiB','zebibyte'),
         ('YiB','yobibyte')
      )
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

def decompoe(tempo_str):
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


__all__ = [
   "Grandeza",
   "Unidade",
   "tamanho",
   "tempo"
]

# testes unitários:
if __name__ == "__main__":
   from testes import executa_teste 

   def testa_tempo_detalhado():
      # valor e peso filtrado:
      string = tempo_detalhado(1_329)
      print(decompoe(string))
      print("1º ==>", string)
      print("2º ==>", tempo_detalhado(592_319))
      print("3º ==>", tempo_detalhado(52_300))

      # testes aleatorios do novo conversor:
      traducao = tempo_detalhado(1166832000)
      print(traducao)
      assert "3 décadas 7 anos" == traducao
      traducao_simples = tempo(1166832000)
      print(traducao_simples, "==>", traducao)
      # outro ...
      traducao = tempo_detalhado(16398720000)
      print(traducao)
      assert "5 séculos 2 décadas" == traducao
      traducao_simples = tempo(16398720000)
      print(traducao_simples, "==>", traducao)

      # testando o arredondamento.
      print(tempo(2_000, arredonda=True))
      # testando o arredondamento para segundos.
      print(tempo(37.3, arredonda=True))
      print(tempo(27.83, arredonda=True))
   ...

   def testa_casos_plurais_e_singulares():
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

   # executa tais funções ...
   executa_teste(
      testa_tempo_detalhado,
      testa_casos_plurais_e_singulares
   )
...
