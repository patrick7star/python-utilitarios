'''
  O programa terá como finalidade escrever
números inteiros positivos por extenso.
    Como fazer algo do tipo, você pergunta? Bem,
vamos tentar achar um padrão. Quando falamos
1583 por extenso, fica algo mais ou menos deste
tipo aqui: mil quinhentos e oitenta e três. Observe
que, há duas classes neste número, por aí já é um
começo, as classes das unidades e as classes de
milhar. O "um" não aparece ali, é um caso mais
específico desta classe ao ditar. Se fosse 139232,
ou seja, um milhão trezenos e noventa e dois mil
duzentos e trinta e dois; neste caso, o "um" aparece,
e este parece o caso par demais classes como bilhão,
trilhão, e etc... más, não para milhar é claro.
Outra coisa que se nota é, em cada classe no número,
você têm algo como um conector "e" ligando as
unidades, dezenas e centenas, sejam elas das de
milhar, milhão, bilhão o quer que for. Outro ponto
é, tirando a classe das unidades, todas as outras
possuem um tipo de sufixo, acompanhando a classe
na fim da ditação, veja: 32819(trezentos e vinte
e oite MIL [...]), 12527111(cento e vinte e cinco
MILHÕES [...]), 8000000000(oito BILHÕES), e assim
em diante.

    Vamos dizer que há apenas uma classe, cada uma
com três casas decimais. As demais, seguem a mesma
lógica, apenas acrescentando o sufixo(tipo milhar,
milhão, bilhão, quatrilhão,...). Sendo assim,
precisamos... primeiro, dividir o números em todas
classes disponiveis; segundo um tradutor que traduza
apenas as primeiras três casas decimais, as demais
no número apenas são estás adicionadas ao um sufixo,
como já dito.
'''
#o que pode, ou não importar.
__all__ = {'escrevaPorExtenso'}
#trasnforma a string numa com o comprimento
#igual ao um múltiplo de três. Para isso, ela
#adiciona zeros à esquerda dele.
def preencheNum(Str):
    #variável auxiliar para mexer o objeto.
    s = Str
    c = len(Str) #seu atual comprimento.
    while c % 3 != 0:
        s = s.zfill(c + 1)
        c = len(s)
    return s

def separaClasses(num):
    '''
        Retorna um dicionário contendo o "número separado por classes",
    de três em três algarismos. E o valor do dicionário é, uma potência
    de dez que "eleva" a classe.

    51.892 - {51:1.000, 892:1}
    9.302.711 - {9:1.000.000, 302:1.000, 711:1}
    '''
    #preenche os zeros necessários para que
    #a quantia de dígitos no número sejá um
    #múltiplo de três.
    aux = preencheNum(num)
    t = len(aux) #comprimento da "str" agora.
    #string para cocatenar, e dicionário para
    #armazenar tal string, e seu correspondente
    #númerico.
    classe, classes = '', {}
    for (k, d) in enumerate(aux):
        classe += d
        #adiciona se o contador for múltiplo de três.
        if (k+1) % 3 == 0:
            #potência; qual múltiplo de três vamos
            #elevar a base dez. O três,... para ser
            #múltiplo de três, já a subtração, está
            #na busca de qual ordem de "classe" tal
            #tal pertence.
            pot = 3 * (int(t/3) - int((k+1)/3))
            classes[int(classe)] = 10 ** pot
            classe = '' #limpando "str" para o próximo.
    #o retorno é um dicionário representando a expansão
    #de um número decimal, só que, pela a classe e não
    #a ordem do número. Ou seja, seu respectivo peso(
    #potência de dez[más, da classe, não do algarismo])
    return classes

def porExtenso1000(num):
    '''
        Retorna recebe um número e retorna uma "str"
    com tal valor escrito por extenso.
    '''
    if num < 1000:
        #têm todos "significados" quando os pesos forem passados.
        tradutor = {0:'', 1:'um', 2:'dois', 3:'três', 4:'quatro', 5:'cinco',
        6:'seis', 7:'sete', 8:'oito', 9:'nove',

        11:'onze', 12:'doze', 13:'treze', 14:'quatorze', 15:'quinze',
        16:'dezesseis', 17:'dezesete', 18:'dezoito', 19:'dezenove',

        10:'dez', 20:'vinte', 30:'trinta', 40:'quarenta', 50:'cinquenta',
        60:'sesenta', 70:'setenta', 80:'oitenta', 90:'noventa',

        100:'cento', 200:'duzentos', 300:'trezentos', 400:'quatrocentos',
        500:'quinhentos', 600:'seiscentos', 700:'setecentos',
        800:'oitocentos', 900:'novecentos'}

        numStr = preencheNum(str(num))
        ordens = tuple([int(alg) * 10**(len(numStr) - i - 1) for (i, alg) in enumerate(str(numStr))])

        #para uma legibilidade melhor, vamos nomear
        #com seus respectivos nomes.
        centenas, dezenas, unidades = ordens

        #soma das unidades e dezena resultar em 11, 12, 13, ..., 19.
        x = dezenas + unidades
        if (x in tradutor) and (x >= 11 and x <=19):
            if unidades != 0 and dezenas != 0 and centenas == 0:
                return tradutor[dezenas + unidades]

            else:
                return tradutor[centenas] + ' e ' + tradutor[dezenas + unidades]

        else:
            if unidades == 0 and dezenas != 0 and centenas != 0:
                return tradutor[centenas] + ' e ' + tradutor[dezenas]

            elif unidades == 0 and dezenas == 0 and centenas != 0:
                    if centenas == 100: return 'cem'
                    return tradutor[centenas]

            elif unidades != 0 and dezenas == 0 and centenas != 0:
                return tradutor[centenas] + ' e ' + tradutor[unidades]

            elif unidades != 0 and dezenas == 0 and centenas == 0:
                return tradutor[unidades]

            elif unidades == 0 and dezenas == 0 and centenas == 0:
                return 'zero'

            elif unidades != 0 and dezenas != 0 and centenas == 0:
                return tradutor[dezenas] + ' e ' + tradutor[unidades]

            elif unidades == 0 and dezenas != 0 and centenas == 0:
                return tradutor[dezenas]

            else:
                return (tradutor[centenas] + ' e ' +
                tradutor[dezenas] + ' e ' + tradutor[unidades])

def escrevaPorExtenso(num):
   '''
     Recebe um número tanto em forma de string como inteiro,
   e retorna uma "str" com tal valor escrito por extenso.
   '''
   if type(num) == int: return escrevaPorExtenso(str(num))

   #nomes das classes numéricas "mais abastadas" do
   #que as usuais.
   sufixos = {1:'', 1000:'mil', 10**6:'milhão',10**9:'bilhão',
   10**12:'trilhão', 10**15:'quatrilhão', 10**18:'quintilhão',
   10**21:'sextilhão', 10**24:'septilhão', 10**27:'octilhão',
   10**30:'donilhão', 10**33:'decilhão', 10**36:'undecilhão',
   10**39:'duodecilhão', 10**42:'tredecilhão',
   10**45:'quatordecilhão', 10**48:'quindecilhão ',
   10**51:'sexdecilhão', 10**54:'setedecilhão',
   10**57:'octodecilhão',10**60:'novedecilhão',
   10**63:'vigesilhão'}
   numero = ''
   #a chave aqui é o número, e a potência é uma potência
   #de dez equivalente a sua classe.
   for (chave, potencia) in separaClasses(num).items():
     #Ele concatenará se, e somente se, e for "maior que mil",
     #portanto na casa dos milhões.
     if potencia in sufixos:
         #caso as classe não seja um, então colocar
         #o texto no plural.
         if potencia >= 10**6 and int(chave) > 1:
             numero += (porExtenso1000(chave) + ' '
                         + sufixos[potencia][0:-2] + 'ões ')
         else:
             #do caso contrário, formata-lô deste modo.
             numero += (porExtenso1000(chave) + ' '
                         + sufixos[potencia] + ' ')
   # pequenos ajustes ajustes
   if int(num) != 0 and numero.find('zero') != -1: 
      return numero.replace('zero', '')
   else: return numero

# *** *** *** EXECUÇÃO *** *** ***
if __name__ == '__main__':

   # buscando pequenos erros na "semântica"...
   print(105,escrevaPorExtenso(105), sep=' - ') # cento e cinco.

   print(1352,escrevaPorExtenso(1352), sep=' - ') # mil trezentos e ciquenta e dois
   print(1052,escrevaPorExtenso(1052),sep=' - ') # mil e cinquenta.

   print(8012012,escrevaPorExtenso(8012012), sep = ' - ') # oitio milhões doze mil e doze
   print(8012812,escrevaPorExtenso(8012812), sep = ' - ') # oitio milhões doze mil e oitocentos e doze
   print(8412012, escrevaPorExtenso(8412012), sep=' - ') # oito milhões quatrocentos e doze mil e doze

   print(1000, escrevaPorExtenso(1000), sep= ' - ') # mil
   print(10**6, escrevaPorExtenso(10**6), sep=' - ') # um milhão
   print(10**9, escrevaPorExtenso(10**9), sep = ' - ') # um bilhão
   print(10**12, escrevaPorExtenso(10**12), sep = ' - ') # um trilhão
   print(10 ** 15, escrevaPorExtenso(10**15), sep = ' - ') # um quatrilhão
   print(10**18, escrevaPorExtenso(10**18), sep = ' - ') # um bilhão
   print(10**21, escrevaPorExtenso(10**21), sep = ' - ') # um trilhão
   print(10 ** 24, escrevaPorExtenso(10** 24), sep = ' - ') # um quatrilhão

   print(10 ** 9 + 1050, escrevaPorExtenso(10**9 + 1050), sep=' - ')
   print(189324712911322, escrevaPorExtenso(189324712911322), sep=' - ')