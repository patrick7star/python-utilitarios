'''
 O algoritmo lerá arquivos e diretórios
e arquivará o tamanho de cada, a quantidade
de arquivos neles e etc.
'''

# *** *** *** funções *** *** ***

def lendo_arquivo(nome):
   acumulador = 0
   arq = open(nome, mode='rb')
   for parte in arq:
      acumulador += len(parte)
      del parte #deleta da memória.
   arq.close()
   return tamanho(
      acumulador,
      acronomo = True,
      unidade='byte',
      sistema='binario'
   )
...

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

def tempo(t):
   '''
   Representar o tempo de forma legível,
   "legendando" o resultado com os acronimos de
   segundos, minutos e horas e etc...'''

   # constantes com escalas de tempo, com suas 
   # equivalências em segundos.
   # A coisa dos múltiplos de submúltiplos são 
   # bem confusos, não seguem o sistema 
   #métrico... inicialmente!
   miliseg = 1 / 1000
   microseg = 1 / 10**6
   nanoseg = 1 / 10**9
   picoseg = 1 / 10**12
   minuto = 60
   hora = 60 * minuto
   dia =  24 * hora
   mes = 30 * dia
   ano = 12 * mes
   # bem aqui começa o sistema métrico...
   decada = 10 * ano 
   seculo = 10 * decada 
   milenio = 10 * seculo
   # múltiplos e sub-múltiplos:
   if t >= picoseg and t < nanoseg:
      return '%0.2f picosegundos' % (t * 10**12)
   elif t >= nanoseg and t < microseg:
      return '%0.2f nanosegundos' % (t * 10**9)
   elif t >= microseg and t < miliseg:
      return '%0.2f microsegundos' % (t * 10**6)
   elif t >= miliseg and t < 1:
      return '%0.2f milisegundos' % (t * 10**3)
   elif t >= 1 and t < 60:
      return '%0.2f segundos' % t
   elif t > 60 and t < 3600: 
      return '%0.2f min'%(t / minuto)
   elif t >= hora and t < dia: 
      return '%0.2f horas'%(t / hora)
   elif t >= dia and t < mes: 
      return '%0.2f dias'%(t / dia)
   elif t >= mes and t < ano: 
      return '%0.2f meses' % (t / mes)
   elif t >= ano and t < decada: 
      return '%0.2f anos' % (t / ano)
   elif t >= decada and t < seculo: 
      return '%0.2f decadas' % (t / decada)
   elif t >= seculo and t < milenio: 
      return '%0.2f séculos' % (t / seculo)
   elif t >= milenio and t < 10 * milenio: 
      return '%0.2f milênios' %(t / milenio)
   else: return str(t)
...
