
# biblioteca padrão do terminal.
from os import get_terminal_size
# própria biblioteca ...
from biblioteca import NE
escreva_por_extenso = NE.escreva_por_extenso

# para simular o macro 'assert_eq' do Rust.
def assert_eq(a, b):
   print("direito:\"{}\"\nesquerdo:\"{}\"\n".format(b, a))
   assert a == b

# separador de testes:
def separador():
   # obtendo largura da tela.
   largura = get_terminal_size().columns
   qtd = largura // 4
   # espaço vertical de uma linha.
   print("")
   for i in range(qtd):
      print("~~~",end=" ")
   # espaço vertical de duas linhas.
   print("\n\n")
...

# executa teste em tais funções.
def executa_tal_funcao(funcao):
   # reparando nome da função.
   novo_nome = (
      funcao
      .__name__
      .replace("testa", "")
      .strip("_")
   )
   # nova mensagem sobre o que está acontecendo...
   print("'{}' testando ...\n".format(novo_nome))
   # chamando tal função...
   funcao()
   # delimitando separador.
   separador()
...

# executa teste em tais funções.
def executa_tal_funcao(funcao):
   # reparando nome da função.
   novo_nome = (
      funcao
      .__name__
      .replace("testa", "")
      .strip("_")
   )
   # nova mensagem sobre o que está acontecendo...
   print("'{}' testando ...\n".format(novo_nome))
   # chamando tal função...
   funcao()
   # delimitando separador.
   separador()
...

def testa_escreva_por_extenso() :
   assert_eq("cinco", escreva_por_extenso(5))
   assert_eq("onze", escreva_por_extenso(11))
   assert_eq("cinquenta e dois", escreva_por_extenso(52))
   assert_eq("quatrocentos e vinte e oito", escreva_por_extenso(428))
   assert_eq(
      "nove mil seiscentos e dezenove", 
      escreva_por_extenso(9_619)
   )
   assert_eq(
      "noventa e um mil duzentos e quarenta e três", 
      escreva_por_extenso(91_243)
   )
   assert_eq(
      "quatrocentos e setenta e oito mil cento e onze",
      escreva_por_extenso(478_111)
   )
   assert_eq(
   "sete milhões quinhentos e vinte e sete mil setecentos e oitenta e quatro",
   escreva_por_extenso(7_527_784)
   )
   assert_eq(
   "trinta e sete milhões cento e cinco mil duzentos e quartoze",
   escreva_por_extenso(37_105_214)
   )
   assert_eq(
   "oitocentos e oitenta e um milhões novecentos e doze mil e dezenove",
   escreva_por_extenso(881_912_019)
   )
   assert_eq(
   "um bilhão um milhão novecentos e noventa e seis mil setecentos e quarenta",
   escreva_por_extenso(1_001_996740)
   )
   assert_eq(
   "vinte e nove bilhões seiscentos milhões quinhentos mil e duzentos",
   escreva_por_extenso(29_600_500_200)
   )
   assert_eq(
   "cento e vinte e nove bilhões seiscentos milhões cento e treze mil e duzentos",
   escreva_por_extenso(129_600_113_200)
   )
   assert_eq(
   "oito trilhões quatrocentos e treze bilhões cento e noventa e nove milhões duzentos e sessenta e três mil duzentos e quarenta e nove",
   escreva_por_extenso(8_413_199_263_249)
   )
   assert_eq(
   "setenta e dois trilhões quinhentos e vinte e um bilhões oitocentos milhões cento e noventa e quatro mil trezentos e quarenta e sete",
   escreva_por_extenso(72_521_800_194_347)
   )
   assert_eq(
   "novecentos e noventa e nove trilhões novecentos e noventa e nove bilhões novecentos e noventa e nove milhões novecentos e noventa e nove mil novecentos e noventa e nove",
   escreva_por_extenso(999_999_999_999_999)
   )
...

def testa_escreva_por_extenso_parte_ii() :
   assert_eq(
   "quarenta e um mil e seiscentos",
   escreva_por_extenso(41_600)
   )
   assert_eq(
   "onze milhões quartoze mil e cem",
   escreva_por_extenso(11014100)
   )
   assert_eq(
   "trinta e nove bilhões cento e cinquenta milhões trezentos e oitenta e oito mil e seiscentos",
   escreva_por_extenso(39_150_388_600)
   )
   assert_eq(
   "novecentos e noventa e nove trilhões novecentos e noventa e nove bilhões novecentos e noventa e nove milhões novecentos e noventa e nove mil e quinhentos",
   escreva_por_extenso(999_999_999_999_500)
   )
...

def testa_escreva_por_extenso_parte_iii():
   assert_eq(
   "quarenta e sete bilhões e oitenta e um",
   escreva_por_extenso(47_000_000_081)
   )
   assert_eq(
   "cem bilhões cinco milhões novecentos e noventa e dois",
   escreva_por_extenso(100_005_000_992)
   )
   assert_eq(
   "setenta e sete milhões",
   escreva_por_extenso(77_000_000)
   )
   assert_eq("zero", escreva_por_extenso(0))
   assert_eq("dezoito", escreva_por_extenso(18))
   assert_eq(
      "duzentos e quarenta e um",
      escreva_por_extenso(241)
   )
   assert_eq("um", escreva_por_extenso(1))
   assert_eq("dez", escreva_por_extenso(10))
   assert_eq("cem", escreva_por_extenso(100))
   assert_eq("mil", escreva_por_extenso(1_000))
   assert_eq("um milhão", escreva_por_extenso(10**6))
   assert_eq("um bilhão", escreva_por_extenso(10**9))
   assert_eq("um trilhão", escreva_por_extenso(10**12))
...


# executa todas funções dadas acima.
executa_tal_funcao(testa_escreva_por_extenso_parte_iii)
executa_tal_funcao(testa_escreva_por_extenso_parte_ii)
executa_tal_funcao(testa_escreva_por_extenso)
