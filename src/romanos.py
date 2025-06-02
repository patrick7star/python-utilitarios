'''
    Este programa fará a conversão de números decimais
em números romanos, e vice-versa. Ele terá duas funções
em geral, claro, as com o propósito principal
do programa. A primeira converte um número inteiro positivo
na notação decimal posicional para a notação romana; já
a segunda função faz o oposto, de notação romana para
decimal posicional(mais conhecida como notação indo-árabe).
    Contará como um monte de passos para produzir isto, ou
seja, outras funções, mas estas são unicamente complementares
das funções principais para atingir o objetivo do programa.
    Os dois algoritmos que vão nos auxiliar em tal tarefa são:

CONVERSÃO DE DECIMAIS PARA ROMANOS - O algoritmo
consiste no seguinte, subtrair o valor decimal até atingir zero.
Mas o que será subtraído é, o valor decimal dos algarismos
romanos disponíveis, estes numa variável global. Ele começa
a verificar o "algarismo romano" mais adequado para subtração
da maior ordem, e vai de cima para baixo, até achar um
algarismo(com seu respectivo valor decimal) que seja menor, ou
igual a tal valor. Feito isto, subtrai o valor decimal dele, enquanto
adiciona numa lista de forma paralela o algarismos romano
equivalente ao subtraído. Quando feito isto uma vez, faz novamente
se preciso, até que este algarismo achado seja maior que
o valor restante, se não for mais, busca o próximo algarismo
romano que cumpri a tarefa, que será concerteza menor que o
anterior. E este processo continua até o valor atinja zero. Veja
exemplos abaixo da tarefa:

84 --> 34 --> 24 --> 14 --> 4 --> 0; subtraído 50(L), o maior
algarismo romano, com um "peso" menor que oitenta e quatro.
E, é adicionado um 'L', verifica se 'L' é possível novamente
subtrair, se não for, então vai ao próximo menor ou igual ao
restante do valor, este trinta e quatro. O 50(L) não é possível,
nem seu sucessor, ou antecessor 40(XL)..., más o próximo a
ele, que é o dez(X) sim. Subtraímos dez(X), adicionando o
correspondente romano na lista,  o restante fica vinte e quatro,
verificamos se ainda cumpri o requisito, ser o maior valor "romano"
menor que o atual restante. E sim, cumpri então subtraímos dez novamete,
adicionando também o símbolo romano de forma paralela. O processo
continua, mais um dez(X) é tirado, e o símbolo correspondente romano
adicionado; o restante, agora quatro(IV), não podemos tirar mais dez(X)
buscamos outro, o mais adequado é o 4(IV[sim, tem este algarismo]),
então assim fazemos, e chegamos ao final buscado, o restante igual à
zero. Os símbolos adicionados na lista durante todo procedimento é
L, X, X, X, IV; que combinados dá exatamente o valor romano que
queríamos transformar.

532 --> 32 --> 22 --> 12 --> 2 --> 1 --> 0; Este aqui demonstrado
de forma mais rápida. Buscamos o maior romano menor a respectivo
valor decimal, que é 500(D), então subtraímos; não servindo mais
procuramos outro para o atual valor trinta e dois, o mais adequado
é dez(X), assim fazemos, subtraindo dez(X) e adicionando aos
símbolos na lista; como continua o adequado, fazemos mais duas
vezes; o restante é agora apenas dois, dez(X) não é menor ou igual
a ele, nem nove(IX), quatro(IV) ou cinco(V), más, um(I) é, subtraímos
um(I), e mais uma vez para zerar o restante.  Os símbolos restantes
que foram adicionados a listas são D, X, X, X, I e I. Estes agrupados
nesta ordem mesmo resultam no romano buscado.

2129 --> 0129 --> 029 --> 29 --> 19 --> 9 --> 0; Este aqui, descrevemos
de forma ainda mais simples. Tiramos mil(M), e mais um milhar(M); Agora
tiramos uma centena(C), então resta apenas vinte e nove; subtraía
dez(X), e como ainda pode, mais dez(X); restam miseros nove(IX) que
tem exatamente um correspondente romano equivalendo inteiramente
este resto. O zero foi alcançado, se combinar todos símbolos usados
fica com MMCXXIX.

CONVERSÃO DE ROMANOS PARA DECIMAIS: Este procedimento
é mais simples. Vamos primeiro, fazer uma busca no número buscando
por algarismos romanos compostos, já que estes, se buscado posteriormente
podem destruir a estrutura do número. Feito isso, buscamos pelos
demais. O algoritmo fica em simplesmente, pegar tais algarismos de modo
separado, colocar seus respectivos "pesos" decimais e somar tudo obtendo
o valor decimal. Exemplos:

DXXIX --> IX(9); D(500); X(10) e X(10); vamos primeiro busca algarismos
compostos na string, se houver algum é claro, se não, o procedimento
fica ainda mais simples. Feito isso fatiamos ela em várias partes, estas
reconheciveis, pois "indexar" no dicionário, nos dá seu respectivo valor
decimal. O resto da tarefa consiste em apenas somar: 9 + 500 + 10 + 10
que é igual 529. Os compostos tem que ser buscado primeiro, pois se
nãofizermos, poderíamos acabar obtendo I(1) e X(10) como dois
algarimos distintos, resultando numa resposta errada no final.

MMCDXCIV --> M(1000); M(1000); CD(400); XC(90) e IV(4). Novamente,
primeiros buscamos algarismos compostos, e este número é cheio deles;
depois os demais(apenas dois aqui[e, ainda iguais]). Achamos seus respectivos
valores decimais e somamos, muito simples não?!: 2x1000 + 400 + 90 + 4 = 2494.
'''
#definindo o que será ou não importado.
__all__ = ["decimal_para_romano","romano_para_decimal"]

#ÚNICO DADO DO PROGRAMA.
'''
    Dicionário contendo o número decimal e o seu respectivo romano.
A chave no caso é um número indo-árabe, já o valor associado a ele,
é o equivalente romano.
'''
algs_romanos = {1:'i', 4:'iv',  5:'v', 9:'ix', 10:'x', 40:'xl',
                50:'l', 90:'xc', 100:'c', 400:'cd', 500:'d',
                900:'cm', 1000:'m'}

ALGARISMOS_ROMANOS = {
   1:'i', 4:'iv',  5:'v', 9:'ix', 10:'x', 40:'xl', 50:'l', 90:'xc', 
   100:'c', 400:'cd', 500:'d', 900:'cm', 1000:'m'
}

#PARTE DO PROGRAMA DESIGNADA PARA
#A CONVERSÃO DE NÚMEROS DECIMAIS
#EM ROMANOS.

def decimal_para_romano(n: int) -> str:
    '''
        Converte um valor decimal, com números indo-arábes, para a
    nomeclatura romana. Recebe o valor decimal como argumento.
    '''
    #declarando função local...
    def adequado(x):
        #lista todos valores do dício em ordem inversa
        #buscar o valor anexado aos algarismos, mais adequado.
        for valor in list(algs_romanos. keys())[::-1]:
            if valor <= x: return valor

    #uma cópia do parâmetro para ser excessivamente modificado.
    #aR - algarismos romanos correpondentes.
    #para formar número achado.
    resto, romano, aR = n, '', []
    while resto > 0:
        #retorno da função que acha valor adequado a subtrair.
        x = adequado(resto)
        #adicionando alg. correspondente ao valor subtraido.
        aR.append(algs_romanos[x].upper())
        resto  = resto - x #fazendo subtração a fim de tentar zero 'resto'.
    #cocatenando string(número romano).
    for alg in aR:
        romano += alg
    return romano

# == == == == == == == == == == == === == == == == == == == == == == == === =
#                 Conversão de Número Romano em Decimal 
# == == == == == == == == == == == === == == == == == == == == == == == === =
#PARTE DO PROGRAMA DESIGNADA PARA
#CONVERSÃO DE NÚMEROS ROMANOS EM
#RESPECTIVOS DECIMAIS.

def separa_algs(str0):
    #1ª função local.
    def concatena_str(lista):
        str0 = ''
        for str1 in lista:
            str0 += str1
        return str0

    #2ª função local.
    def removeWC(lista):
        while lista.count('') > 0:
            lista.remove('')

    #cópia da string passada para modificação.
    #lista para colocar os algarismos colhidos.
    #outra lista para se colocar os restos da
    #repartição das strings em partes após
    #dividí-la no "algarismo" procurado.
    str1, algs, resto = str0, [], []
    for alg in ('iv', 'ix', 'xl', 'xc', 'cd', 'cm'):
        #verifica se há o alg. buscado na string formada.
        if alg in str1:
            #se há, então adiciona na lista de algs.
            algs.append(alg)
            #repartimo-las, retirando o alg. achado.
            resto = str1.split(alg)
            #apenas remove o espaço em branco que fica, para o código não "quebrar".
            removeWC(resto)
            #forma uma nova string com os restos, mas sem o alg. compostos retirado.
            str1 = concatena_str(resto)
    #como restou apenas algarismos unitários, adicioná-los
    #ao resto da lista é bem fácil, apenas converter a string
    #em lista e concatenar com a outra.
    return tuple(algs + list(str1))

def romano_para_decimal_velho(strR):
    '''
        Recebe uma string, representando um número romano, então
    retorna-o seu equivalente decimal(como tipo inteiro).
    '''
    if (not isinstance(strR, str)):
       raise TypeError("o número romano tem que ser uma 'str' obviamente")
    #dado o algarismos, que é o valor no dicionário global;
    #a função acha a chave correspondente a este valor
    #e o retorna.
    def valor_chave(c):
        for (chave, valor) in list(algs_romanos.items()):
            if c == valor: return chave
    #convertendo todos os algarismos, e o transformando
    #em decimais.
    valores = [valor_chave(valor) for valor in separa_algs(strR.lower())]
    #somando para obter o decimal.
    return sum(valores)

def separa_algarismos_do_romano(numero: str) -> tuple:
   """
     Pega um número romano(uma string), então divide ela em seus respectivos
   algarismos. Não é uma tarefa trivial, já que tal tipo de número tem uma
   formação que não segue os sistema decimal posicional.

     Parte da presunção que o número romano é uma lowercase string.

     O algoritmo funciona do seguinte modo. Ele aranca primeiro qualquer
   algarismo composto que o número em string tenha. Já os pedaços de strings
   que sobraram, serão apenas compostos de algarismos não-compostos, portanto
   facilmente divisíveis.
   """
   # Duas lista, uma para os algarismos compostos extraídos, e outra para 
   # os trechos de strings que sobraram.
   (algs, resto) = ([], [])
   ALGARISMOS_COMPOSTOS = ('iv', 'ix', 'xl', 'xc', 'cd', 'cm')

   for alg in ALGARISMOS_COMPOSTOS:
      # Verifica se há o alg. buscado na string formada.
      if alg in numero:
         # Repartimo-las, retirando o algarismo achado.
         resto = numero.split(alg)
         # Se há, então adiciona na lista de algs.
         algs.append(alg)
         # Forma uma nova string com os restos, mas sem o alg. compostos 
         # retirado. 
         # Obs.: A concatenção de strings tem efeito nulo no resultado final,
         #       por isso a função de remoção deles foi descartado, um uso
         #       desnecessário no uso de CPU.
         numero = "".join(resto)
   # Concatena a lista de algarismos-compostos, e converte o que sobre da
   # número de algarismos únicos, numa grande lista de algarismos, que 
   # também é convertido em tupla.
   return tuple(algs + list(numero))

#dado o algarismos, que é o valor no dicionário global;
#a função acha a chave correspondente a este valor
#e o retorna.
def converte_algarismo_pra_decimal(alg: str) -> int:
   for (chave, valor) in ALGARISMOS_ROMANOS.items():
      if alg == valor: 
         return chave

def romano_para_decimal(numero: str) -> int:
   """
     Recebe uma string, representando um número romano, então retorna-o 
   seu equivalente decimal(como tipo inteiro).
   """
   if (not isinstance(numero, str)):
      raise TypeError("o número romano tem que ser uma 'str' obviamente")

   # Convertendo todos os algarismos, e o transformando em decimais, então
   # soma-os para obter o decimal.
   numero = numero.lower()
   conversor = lambda alg: converte_algarismo_pra_decimal(alg)
   separador = separa_algarismos_do_romano

   return sum(map(conversor, (x for x in separador(numero))))

# == == == == == == == == == == == === == == == == == == == == == == == === =
#                          Testes Unitários
# == == == == == == == == == == == === == == == == == == == == == == == === =
from unittest import (TestCase)
from random import (randint)
from pprint import (pprint as PPrint)
from timeit import (timeit as time_it, repeat)
import gc

class DecimalPraRomanoUnitarios(TestCase):
   def setUp(self):
      TOTAL = randint(5, 15)
      self.input = [randint(1, 1999) for _ in range(TOTAL)]
      
      PPrint(self.input)

   def executa(self):
      for X in self.input:
         print("\t\b\b%-4d ===> %10s" % (X, decimal_para_romano(X)))

class DesempenhoEntreFuncoesDPR(TestCase):
   def setUp(self):
      self.input = decimal_para_romano(randint(1, 4_999))

   def execucao_com_garbage_collector_ativado(self, QUANTIA: int) -> None:
      medida_do_novo = time_it(
         "motor(INPUT)", "ativar()",
         number = QUANTIA,
         globals = {
            "INPUT": self.input, 
            "motor": romano_para_decimal,
            "ativar": gc.enable
         }
      )
      medida_do_velho = time_it(
         "motor(INPUT)", "garbage_collector_on()",
         number = QUANTIA,
         globals = {
            "INPUT": self.input, 
            "motor": romano_para_decimal_velho,
            "garbage_collector_on": gc.enable
         }
      )

      print("\nPerformance  do algorigmo, 'garbage colector' [ON].")
      print(medida_do_novo, '<', medida_do_velho, '?')

      if medida_do_velho > medida_do_novo:
         diferenca = (medida_do_velho - medida_do_novo)
         percentual = 100.0 * (diferenca / medida_do_velho)
         print(
            "A diferença é de %f seg para %d testes, algo em %0.1f%% mais" 
            " veloz."
           % (diferenca, QUANTIA, percentual)
         )
      else:
         print("O algoritmo não foi otimizado.")
      assert(medida_do_novo < medida_do_velho)

   def execucao_sem_o_garbage_collector(self, QUANTIA: int) -> None:
      medida_do_novo = time_it(
         "motor(INPUT)", number = QUANTIA,
         globals = {
            "INPUT": self.input, 
            "motor": romano_para_decimal,
         }
      )
      medida_do_velho = time_it(
         "motor(INPUT)", number = QUANTIA,
         globals = {
            "INPUT": self.input, 
            "motor": romano_para_decimal_velho,
         }
      )

      a = medida_do_novo; b = medida_do_velho
      print("\nPerformance  do algorigmo, 'garbage colector' [OFF].")
      print("\t{} < {}? {}".format(a, b, a < b))

      if medida_do_velho > medida_do_novo:
         diferenca = (b - a)
         percentual = 100.0 * (diferenca / b)
         print(
            "A diferença é de %f seg para %d testes, algo em %0.1f%% mais" 
            " veloz."
           % (diferenca, QUANTIA, percentual)
         )
      else:
         print("O algoritmo não foi otimizado.")
      assert(medida_do_novo < medida_do_velho)

   def desempenhos(self):
      QUANTIA = 6250

      self.execucao_com_garbage_collector_ativado(QUANTIA)
      self.execucao_sem_o_garbage_collector(QUANTIA)
