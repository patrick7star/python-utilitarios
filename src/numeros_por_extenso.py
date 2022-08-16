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
__all__ = {'escreva_por_extenso'}

tradutor = {
   0:'', 1:'um', 2:'dois', 3:'três', 4:'quatro', 
   5:'cinco', 6:'seis', 7:'sete', 8:'oito', 9:'nove',
   10:'dez', 20:'vinte', 30:'trinta', 40:'quarenta', 
   50:'cinquenta', 60:'sessenta', 70:'setenta', 
   80:'oitenta', 90:'noventa',
   100:'cento', 200:'duzentos', 300:'trezentos', 
   400:'quatrocentos', 500:'quinhentos', 
   600:'seiscentos', 700:'setecentos', 
   800:'oitocentos', 900:'novecentos'
}

PESOS = (
   "mil", "milhões", "bilhões",
   "trilhões", "quatrilhões",
   "quintilhões", "sextilhões",
   "septilhões", "octilhões",
   "donilhões", "decilhões", "undecilhões",
   "duodecilhões", "tredecilhões",
   "quatordecilhões", "quindecilhões",
   "sexdecilhões", "setedecilhões",
   "octodecilhões","novedecilhões",
   "vigesilhões"
)

PESOS_UNITARIOS = (
   "mil", "milhão", "bilhão",
   "trilhão", "quatrilhão",
   "quintilhão", "sextilhão",
   "septilhão", "octilhão",
   "donilhão", "decilhão", "undecilhão",
   "duodecilhão", "tredecilhão",
   "quatordecilhão", "quindecilhão",
   "sexdecilhão", "setedecilhão",
   "octodecilhão","novedecilhão",
   "vigesilhão"
)

# decompõe um número em algarismos, onde 
# a parte mais a esquerda têm uma potência
# maior que o mais a esquerda, mesmo como
# é escrito a mão. 
def decompoe(numero):
   # pilha contendo algarismos.
   pilha_algs = []

   # empilhando algarismos ...
   for alg in str(numero):
      pilha_algs.append(int(alg))

   # faz sempre a quantia de algs. um 
   # múltiplo de três.
   qtd = len(pilha_algs)
   if qtd % 3 == 1:
      pilha_algs.insert(0, 0)
      pilha_algs.insert(0, 0)
   elif qtd % 3 == 2:
      pilha_algs.insert(0, 0)

   return pilha_algs
...

def zero_a_mil(algarismos):
   '''
   Retorna recebe um número e retorna uma "str"
   com tal valor escrito por extenso.
   '''
   if len(algarismos) != 3:
      raise Exception("só aceita um número com três algarismos!")

   # ordens da classe:
   unidades = tradutor[algarismos[2]]
   dezenas = tradutor[algarismos[1] * 10]
   centenas = tradutor[algarismos[0] * 100]

   # casos possíveis de escrita:
   algs = algarismos
   if algs[0] == 0 and algs[1] == 0 and algs[2] == 0:
      return "zero"
   elif algs[0] != 0 and algs[1] == 0 and algs[2] == 0:
      # tipo de casos trabalhados neste bloco:
      # 100, 200, 300, 400,... ,800, 900 
      if algs[0] == 1:
         return "cem"
      else:
         return centenas
   elif algs[0] == 0 and algs[1] != 0 and algs[2] == 0:
      # tipo de casos trabalhados neste bloco:
      # 10, 20, 30, 40,... ,80, 90 
      return dezenas
   elif algs[0] == 0 and algs[1] == 0 and algs[2] != 0:
      # tipo de casos trabalhados neste bloco:
      # 1, 2, 3, 4,... 8, 9. 
      return unidades
   elif algs[0] == 0 and algs[1] != 0 and algs[2] != 0:
      # tipo de casos trabalhados neste bloco:
      # 85, 39, 24, 15 e etc.
      return dezenas + " e " + unidades
   elif algs[0] != 0 and algs[1] == 0 and algs[2] != 0:
      # tipo de casos trabalhados neste bloco:
      # 805, 309, 204, 105 e etc. 
      return centenas + " e " + unidades
   elif algs[0] != 0 and algs[1] != 0 and algs[2] == 0:
      # tipo de casos trabalhados neste bloco:
      # 850, 390, 240, 150 e etc. 
      return centenas + " e " + dezenas
   else:
      # todos os demais, onde não há algarismos nulos
      # serão tratados aqui. Por exemplo: 312, 582,
      # 958, 642, 231, 253 e etc...
      return centenas + " e " + dezenas + " e " + unidades
   ...
...

# verifica por causa do algoritmo de construção
# da escrita por extenso, se a última classe 
# é uma ou mais centenas "certas", o que quero
# dizer é: tanto suas dezenas com unidades de tal
# classe estão zeradas, só a cetena que conta.
def centenas_valida(numero):
   # obtendo algarismos do número.
   algs = decompoe(numero);
   # total de algarismos para indexer direito a array.
   q = len(algs)
   # obten as ordens da última classe.
   unidade = algs[q-1];
   dezena = algs[q-2];
   centena = algs[q-3];

   # verificando se só a centena tem alguma coisa ...
   if centena != 0 and dezena == 0 and unidade == 0:
      return True
   elif centena == 0 and (dezena != 0 or unidade != 0):
      return True
   else:
      return False
...

# peguando casos especiais e reescrevendo string.
def consertando_casa_dos_dez(ne):
   # onze.
   if "dez e um" in ne:
      ne = ne.replace("dez e um", "onze")
   # doze.
   if "dez e dois" in ne:
      ne = ne.replace("dez e dois", "doze")
   # treze.
   if "dez e três" in ne:
      ne = ne.replace("dez e três", "treze")
   # quartoze.
   if "dez e quatro" in ne:
      ne = ne.replace("dez e quatro", "quartoze")
   # quinze.
   if "dez e cinco" in ne:
      ne = ne.replace("dez e cinco", "quinze")
   # dezesseis.
   if "dez e seis" in ne:
      ne = ne.replace("dez e seis", "dezesseis")
   # dezesete.
   if "dez e sete" in ne:
      ne = ne.replace("dez e sete", "dezesete")
   # dezoito.
   if "dez e oito" in ne:
      ne = ne.replace("dez e oito", "dezoito")
   # dezenove.
   if "dez e nove" in ne:
      ne = ne.replace("dez e nove", "dezenove")

   # re-retornando a string passada, talvez consertada.
   return ne;
...

def escreva_por_extenso(numero):
   """
   retorna uma string com o valor escrito
   por extenso. O maior valor permitido é um
   inteiro de 64-bits, porém não é o limite
   total que está implementado.
   Então o código retorna um `Err` com limites
   possíveis ainda não implementados.
   """
   # no caso de um valor de 0 à 1000, um função 
   # cuida perfeitamente disso, precisando apenas 
   # que aplique uma correção, como os demais casos. 
   if numero < 1000:
      numero_str = zero_a_mil(decompoe(numero))
      pos_conserto = consertando_casa_dos_dez(numero_str)
      return pos_conserto
   elif numero == 1_000:
      # tratando de caso muito específico ...
      return "mil"
   else:
      escrita = ""
      algarismos = decompoe(numero)
      qtd = len(algarismos)

      pesos = [ ' ' + s + ' ' for s in PESOS]
      pesos_unitario = [ ' ' + s + ' ' for s in PESOS_UNITARIOS]

      if qtd >= 6:
         # total de ciclos, tirando o das centenas.
         ciclos = (qtd // 3) - 1
         # ínicio e fim do intervalo.
         (i, f) = (0, 3)
         # total de pesos inicialmente, para indexar o último.
         indice = (qtd - 6 + 3)//3 -1

         # realizando concatenação "ciclo vezes".
         while ciclos > 0:
            fatia = algarismos[i:f]
            forma_numero = zero_a_mil(fatia)
            no_plural = (
               forma_numero != "zero" and
               forma_numero != "um"
            )
            no_singular = (
               forma_numero != "zero" and
               forma_numero == "um"
            )
            if no_plural :
               escrita += forma_numero
               # tira de ambos, pois o próximo pode ser do outro.
               escrita += pesos.pop(indice)
               # (DESABILITADO)drop(pesos_unitario.remove(indice));
               # nova quantia de pesos atualizada.
               if indice > 0 :
                  indice -= 1
            elif no_singular :
               escrita += forma_numero
               # tira de ambos, pois o próximo pode ser do outro.
               escrita += pesos_unitario.pop(indice)
               #[DESABILITADO]drop(pesos.remove(indice))
               # nova quantia de pesos atualizada.
               if indice > 0:
                  indice -= 1
            ...
            # avançando no intervalo ...
            i += 3; f += 3;
            # cotabilizando ciclos realizados.
            ciclos -= 1
         ...
         # adicionando centenas separadamente ...
         fatia = algarismos[i:f]
         # debugando caso especial ...
         if __debug__:
            if numero == 1052:
               print("fatia:", fatia)
               print("número por extenso:", zero_a_mil(fatia))
            ...
         ...
         forma_numero = zero_a_mil(fatia)
         if centenas_valida(numero):
            escrita += "e "
            escrita += forma_numero
         elif forma_numero != "zero":
            escrita += forma_numero
      else:
         # se for uma ordem ainda não trabalhada ...
         raise Exception("quatrilhão, quintilhão e etc; não implementada!")
      ...

      # concertando dezenas que por meio automático foram
      # traduzidas como por exemplo:
      #    'dez e cinco' ao invés de 'quize'
      #    'trezentos e dez e um' ao invés de 'trezentos
      #    e onze' 
      escrita = consertando_casa_dos_dez(escrita)
      def termina_com_espaco_em_branco(s):
         caracteres = tuple(s)
         indice = len(caracteres) - 1
         if caracteres[indice].isspace():
            return True
         else:
            return False
      ...
      # retirar espaço em branco no final, se houver algum.
      if termina_com_espaco_em_branco(escrita):
         escrita = escrita.rstrip()
      # nova triagem de reparos:
      return conserta_unidade_de_milhar(escrita, numero)
   ...
...

# conserta um caso especial de número por extenso.
# O caso em que é "um mil", porém não é escrito 
# desta maneira por muitas vezes.
def conserta_unidade_de_milhar(ne_str, numero):
   if ne_str.startswith("um mil") and numero < 10**6:
      return ne_str.replace("um mil", "mil")
   else:
      # se não for o caso, apenas retorna o que 
      # foi passado.
      return ne_str
   ...
...

__all__ = ["escreva_por_extenso"]

# *** *** *** EXECUÇÃO *** *** ***
if __name__ == '__main__':
   # buscando pequenos erros na "semântica"...
   extenso = escreva_por_extenso(105)
   print(105, extenso, sep=' - ') # cento e cinco.
   assert "cento e cinco" == extenso

   extenso = escreva_por_extenso(7352)
   print(7352, extenso, sep=' - ') 
   assert "sete mil trezentos e cinquenta e dois" == extenso

   extenso = escreva_por_extenso(1052)
   print(1052, extenso, sep=' - ')
   assert "mil e cinquenta e dois" == extenso

   # pegando algumas sutilezas ...
   extenso = escreva_por_extenso(8_012_012)
   print(8012012, extenso, sep = ' - ') 
   assert "oito milhões doze mil e doze" == extenso

   numero = 8_012_812
   extenso = escreva_por_extenso(numero)
   print(numero, extenso, sep = ' - ') 
   assert "oito milhões doze mil oitocentos e doze" == extenso

   numero = 8_412_012
   extenso = escreva_por_extenso(numero)
   print(numero, extenso, sep = ' - ') 
   assert "oito milhões quatrocentos e doze mil e doze" == extenso

   # teste com potências de 10, as implementadas...
   numero = 10**3
   extenso = escreva_por_extenso(numero)
   print(numero, extenso, sep = ' - ') 
   assert "mil" == extenso

   numero = 10**6
   extenso = escreva_por_extenso(numero)
   print(numero, extenso, sep = ' - ') 
   assert "um milhão" == extenso

   numero = 10**9
   extenso = escreva_por_extenso(numero)
   print(numero, extenso, sep = ' - ') 
   assert "um bilhão" == extenso

   numero = 10**12
   extenso = escreva_por_extenso(numero)
   print(numero, extenso, sep = ' - ') 
   assert "um trilhão" == extenso

   print(10 ** 15, escreva_por_extenso(10**15), sep = ' - ') # um quatrilhão
   print(10**18, escreva_por_extenso(10**18), sep = ' - ') # um bilhão
   print(10**21, escreva_por_extenso(10**21), sep = ' - ') # um trilhão
   print(10 ** 24, escreva_por_extenso(10** 24), sep = ' - ') # um quatrilhão

   print(10 ** 9 + 1050, escreva_por_extenso(10**9 + 1050), sep=' - ')
   print(189324712911322, escreva_por_extenso(189324712911322), sep=' - ')
...
