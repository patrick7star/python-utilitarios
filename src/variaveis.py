

"""
   Cria variáveis booleanas que tem obviamente um valor lógico, porém,
 tais não somem quando o programa é encerrado, pois são gravas na
 'memória de massa' de tempos em tempos.
   Tal não é case-sensitive, portanto só armazena um tipo de variável
 por vez. Elas também tem a data de criação, e a última alteração feita.
 Por que criar isso, e não um variável de ambiente? Porque esta o
 armazenamento é "permanente" não só quando está em execução.
"""

from time import time
from tempo import Temporizador
from testes import bool_to_str

# o que será importado?
__all__ = ("TabelaBooleana")


def minimiza_espacos(texto: str) -> iter:
   """
   pega um texto, e se ele tem vários espaços seguidos, apenas minimiza
   para um só espaço tal.
   """
   # informa que a 'string' já foi preenchida com um espaço.
   ja_tem_espaco = False

   for char in texto:
      if char.isspace():
         # se espaços seguidos já está ativado, não usar tal caractére.
         if ja_tem_espaco:
            continue
         else:
            # gerar e tentar marca como um espaço já colocado.
            ja_tem_espaco = True
            yield(char)
      else:
         yield(char)
         # acaba com a tag de espaço seguid.
         ja_tem_espaco = False
      ...
   ...
...

def troca_acentuacao(char: str) -> str:
   "troca todas vogais acentuadas por simples vogais"
   match char.lower():
      case 'é' | 'ê' | 'ë' | 'ẽ':
         return 'e'
      case 'á' | 'â' | 'ã' | 'à':
         return 'a'
      case 'í' |  'ì':
         return 'i'
      case 'ô' | 'ó' | 'ö' | 'õ':
         return 'o'
      case 'ú' | 'ù' | 'ü':
         return 'u'
      case _:
         return char
   ...
...

def ajusta_variavel(nome: str) -> str:
   return (
      # retira possível vogais acentuadas.
      ''.join(
         map(
            lambda ch: troca_acentuacao(ch),
            # retira espaços desnecessários...
            minimiza_espacos(nome.lower())
         )
      ).replace(' ', '_')
      # retira possíveis 'underscores' das pontas de tais variáveis.
      .strip('_').rstrip('_').upper()
   )
...

from datetime import (datetime as DT, timedelta)
from pathlib import (PurePosixPath, Path)
from os import getenv

# nome do arquivo para os registros das entradas.
NOME_ARQUIVO = ".variaveis_registro.dat"
# como é desejado que, todas variáveis sejam armazenadas num mesmo
# lugar, e, não dependendo onde tal biblioteca está instalada, vamos
# fazer deste arquivo oculto, e colocado na pasta $HOME do usuário que
# o chama, ou seja, seu referêncial será o usuário que o chama.
RAIZ = PurePosixPath(getenv("HOME"))
CAMINHO_BD = PurePosixPath.joinpath(RAIZ, NOME_ARQUIVO)
SEPARADOR = ":::"
# apelido para dicionário com chave string e valor tupla.
Variaveis = dict[str: (bool, DT)]

def grava_em_disco(variaveis: Variaveis):
   # só faz algo se houver valores no dicionário.
   if len(variaveis) == 0:
      print("nenhuma variável à gravar em disco!")
      return None

   with open(CAMINHO_BD, "wt") as arquivo:
      # itera dicionário com nome das variaveis e seus valores, além
      # de outras informações secundárias.
      for (nome, vls) in variaveis.items():
         arquivo.write(
            "{0}{sep}{1}{sep}{2}\n"
            .format(
               nome, bool_to_str(vls[0]),
               vls[1].timestamp(),
               sep = SEPARADOR
            )
         )
      ...
   ...
...

def str_para_bool(valor: str) -> bool:
   # neste caso, caem mais casos sensitivos.
   valor = valor.lower()

   if valor == "verdadeiro" or valor == "true" or valor == 'v':
      return True
   elif valor == "falso" or valor == "false" or valor == 'f':
      return False
   else:
      raise ValueError("este '{}' não é um válido!".format(valor))
...

def le_do_disco() -> Variaveis:
   agrupador: {str: (bool, DT)} = {}

   # abrindo arquivo para lê e processar dados, se um erro acontecer
   # no caminho, o dicionário só ficará inalterado.
   try:
      with open(CAMINHO_BD, "rt") as arquivo:
         for linha in arquivo.readlines():
            # divide a string baseado no separador, assim podemos
            # trabalhar com os devidos componentes salvos.
            (nome, valor_logico, tempo) = (
               linha.rstrip('\n')
               .split(sep=SEPARADOR, maxsplit=2)
            )
            # convertendo e inserido na tabela.
            agrupador[nome] = (
               str_para_bool(valor_logico),
               DT.fromtimestamp(float(tempo))
            )
         ...
      ...
   except FileNotFoundError:
      arquivo = open(CAMINHO_BD, "wt")
      arquivo.close()
      print(
         "como '{}' não existe, então foi criado."
         .format(NOME_ARQUIVO[1:])
      )
   ...

   return agrupador
...

from legivel import tempo
from tabelas import (
   Coluna, forma_tabela,
   forma_tabela_com_multiplas_colunas 
)

class TabelaBooleana:
   """
   Cria uma tabela que armazena apenas variáveis booleanas, que podem
   ser acessada depois de o programa ter sido encerrado, já que ela
   grava todas alterações feitas nela em disco de tempos em tempos.
   """
   # contagem de instâncias criadas.
   total = 0

   def __init__(self) -> None:
      # mapa que guarda o nome da variável, e uma tupla cotendo o valor
      # lógico dela, e última vez que ela foi alterada.
      self.variaveis: {str:(bool, DT)} = le_do_disco()

      # se não estiver vázia, e o arquivo binário deste não existir,
      # então clonar este para o binário.
      caminho = Path(CAMINHO_BINARIO_BD)
      if len(self.variaveis) > 0 and (not caminho.exists()):
         clona_para_bd_binario()

      # a cada 10seg atualiza o banco de variáveis, escrevendo novas
      # registros em disco.
      self.houve_atualizacao: bool = False
      limite = timedelta(seconds=10)
      self.contagem: Temporizador = Temporizador(limite)

      # contabilizando as instâncias deste tipo.
      TabelaBooleana.total += 1
   ...

   def __len__(self) -> int:
      return len(self.variaveis)

   def __setitem__(self, chave: str, valor: bool):
      novo_nome = ajusta_variavel(chave)

      if novo_nome in self.variaveis:
         vL = self.variaveis[novo_nome][0]
         print("trocando valor de '{}' para '{}'".format(novo_nome, vL))
      else:
         print("nova variável '{}' adicionada.".format(novo_nome))
         self.variaveis[novo_nome] = [valor, DT.today()]

      # informa de mudanças.
      self.houve_atualizacao = True

      # acionando atualização automática, por enquanto na mesma thread.
      if (not self.contagem):
         grava_em_disco(self.variaveis)
         # contagem reiniciada para atualizar novamente.
         self.contagem.reutiliza()
   ...

   def __getitem__(self, chave: str) -> bool:
      # no inicio verifica se é preciso gravar dados da tabela, caso
      # seja, então faz. Isso pode parecer uma operação de busca
      # ficar extramente custosa, porém poucos dados estarão na tabela,
      # e no futuro tal operação de escrita será feita paralalemente
      # quando chegar pontos de verificação, assim não interrompendo
      # a consulta pelo valor.
      if (not bool(self.contagem)) and self.houve_atualizacao:
         grava_em_disco(self.variaveis)
         self.houve_atualizacao = False
      ...
      nome = ajusta_variavel(chave)

      if nome in self.variaveis:
         return self.variaveis[nome][0]
      else:
         raise ValueError("tal '{}' não existe.".format(nome))
   ...

   def salva(self) -> None:
      "faz operação de gravação automaticamente, na verdade força uma"
      # grava todas variáveis criadas ou atualizadas em disco.
      grava_em_disco(self.variaveis)
      # em seguida grava a versão binária.
      clona_para_bd_binario()
      # marcando para nova futura atualiza no futuro.
      self.houve_atualizacao = False
      # refazendo a contagem.
      self.contagem.reutiliza()
   ...

   def __del__(self):
      """
      quando liberado, manualmente ou via GB, ele grava última vez em
      disco se for necessário
      """
      if self.houve_atualizacao:
         grava_em_disco(self.variaveis)
         # também escrevendo versão em binário.
         clona_para_bd_binario()
         if __debug__:
            print("última modificação foi realizada nela.")
      else:
         if __debug__:
            print("nenhum alteração consta nela para regravar dados.")
      ...
      # descontabilizando instâncias destruída.
      TabelaBooleana.total -= 1
   ...

   def __str__(self) -> str:
      "impressão do tipo mostra ela numa tabela"
      nomes_variaveis = []
      valores_logicos = []
      tempo_decorrido = []

      for (nome, (valor, t)) in self.variaveis.items():
         diferenca = DT.today() - t
         tempo_str = tempo(diferenca.total_seconds())
         # criando o rol de dados de cada grandeza.
         nomes_variaveis.append(nome)
         valores_logicos.append(bool_to_str(valor))
         tempo_decorrido.append(tempo_str)
      ...

      return forma_tabela_com_multiplas_colunas(
         Coluna("variável", nomes_variaveis), 
         Coluna("valor-verdade",valores_logicos), 
         Coluna("última alteração",tempo_decorrido)
      )
   ...

   def __iter__(self) -> iter:
      iterador = self.variaveis.items()
      # uma tupla contendo um nome e outra tupla, esta segunda sendo
      # um par com o valor, e timestamp, neste caso, só iteressa o 
      # valor.
      return map(lambda t: (t[0], t[1][0]), iterador)
   ...
...

NOME_ARQUIVO_BINARIO = ".variaveis_registro_binario.dat"
CAMINHO_BINARIO_BD = PurePosixPath.joinpath(RAIZ, NOME_ARQUIVO_BINARIO)

def serializacao_da_variavel(nome: str, valor: bool, 
  tempo: DT) -> bytearray:
   # a array de bytes começa com o tamanho da string, esta que é
   # a primeira.
   bytes_str = bytes(nome, encoding="latin1")
   size_str = len(bytes_str)
   todos_bytes = bytearray(size_str.to_bytes(1, "little"))
   # colocando a string, de tamanho variável.
   # tamano da string terá um valor entre 1 à 255 caractéres no máximo.
   todos_bytes += bytes_str

   # anexando o valor-lógico.
   bytes_bool = int(valor).to_bytes(1, "little")
   todos_bytes += bytes_bool

   segundos = tempo.timestamp()
   # adicionando por último o valor flutuante.
   inteiro = int(segundos)
   # extraindo parte decimal.
   decimal = abs((inteiro - segundos) * pow(10, 6))
   bytes_int = inteiro.to_bytes(8, "little")
   bytes_float = int(decimal).to_bytes(4, "little")
   todos_bytes += bytes_int
   todos_bytes += bytes_float

   return todos_bytes
...

from array import array as Array
from os import (
   open as Open, O_RDONLY, O_CREAT,
   O_WRONLY, close as Close, fdopen
)

def deserializando_variavel(fila: Array) -> (str, bool, DT):
   # deque com toda quantias de bytes a serem consumida.
   # primeiro byte é o nome da string.
   tamanho_str = fila.pop(0)
   print("tamanho da string: %d" % tamanho_str)
   # então lê ela, baseado na sua quantia de bytes já lida.
   nome = b"".join(
      bytes(chr(b), encoding="ascii")
      for b in drena(fila, tamanho_str)
   )
   # Agora lê-se 1 byte do valor-lógico.
   valor_logico = bool(fila.pop(0))

   # Lendo os bytes do ponto flutuante, primeiro 8 bytes da
   # parte inteira, posteriormente 4 bytes da parte decimal.
   bytes_int = (fila.pop(0) for _ in range(8))
   inteiro = float(int.from_bytes(bytes_int, "little"))
   bytes_float = (fila.pop(0) for _ in range(4))
   # colocando ele novamente para um valor menor que um.
   decimal = int.from_bytes(bytes_float, "little") * pow(10, -6)
   # transformando num datetime novamente.
   tempo = DT.fromtimestamp(inteiro + decimal)

   # se não chegou aqui vázia, um erro aconteceu.
   assert len(fila) == 0
   return (nome, valor_logico, tempo)
...

def grava_em_disco_binario(variaveis: Variaveis) -> bool:
   """o mesmo que anterior, porém a gravação é em binário"""
   tipo = Open(CAMINHO_BINARIO_BD, O_WRONLY | O_CREAT)
   arquivo = fdopen(tipo, "wb")

   # convertendo todos os tipos de dados numa 'bytearray', assim,
   # podemos escrever no 'file descriptor'. Eles seguem a ordem
   # dos argumentos passados na função de serialização.
   for (nome, (vL, t)) in variaveis.items():
      _bytes = serializacao_da_variavel(nome, vL, t)
      # são escritos um ao lado do outro sem qualquer separador.
      # Portanto fica a cargo de quem escreveu ele, na ordem dada,
      # interpleta-lá.
      arquivo.write(_bytes)
   ...
   arquivo.close()
   # se chegou até aqui, então é porque  a escrita foi concluída
   # com total sucesso.
   return True
...

def drena(a: Array, t:int) -> Array:
   assert isinstance(a, Array)
   assert isinstance(t, int)
   return Array('B',(a.pop(0) for _ in range(t)))
...

def le_em_disco_binario() -> Variaveis:
   """o mesmo que anterior, porém a gravação é em binário"""
   variaveis: {str: (bool, DT)} = dict()
   tipo = Open(CAMINHO_BINARIO_BD, O_RDONLY)
   arquivo = fdopen(tipo, mode="r+b")
   # pegando todos bytes nele.
   _bytes = Array('B',arquivo.read())
   arquivo.close()

   # processando tal informação...
   while len(_bytes) > 0:
      # lendo o tamanho da string.
      tamanho_str = _bytes[0]
      # agora o total de bytes fica previsível. A regra é a seguinte,
      # o primeiro byte representa o total de bytes da string seguinte,
      # isso que deixa as fatias de bytes variante, no momento que
      # leio interpleto ela, o total dos bytes restantes são fixos,
      # 1 byte para o valor lógico, e 12 para o valor decimal, nesta
      # ordem. Por isso da soma abaixo.
      total = 1 + int(tamanho_str) + 1 + 12
      slice_array = drena(_bytes, total)
      (chave, vL, tempo) = deserializando_variavel(slice_array)
      variaveis[chave] = (vL, tempo) 
   ...
   
   return variaveis
...

def copia_bd_texto_para_bd_binario() -> None:
   if __debug__:
      print(
         "não existe um 'banco de dados' "+
         "com dados serializados em binário."
      )
      print("lendo BD existente...", end='')
   ...
   variaveis = le_do_disco()
   if __debug__:
      print("feito.")
      print("criando sua versão binária.")
   ...
   assert(grava_em_disco_binario(variaveis))
...

def clona_para_bd_binario() -> bool:
   caminho = Path(CAMINHO_BD)
   if caminho.exists():
      copia_bd_texto_para_bd_binario()
      print("BD de texto clonado para binário.")
   else:
      print("tal BD binário já existe, não é preciso clonagem.")
...


# itens para testes:
import unittest, random
from os.path import exists
from time import sleep
from os import remove

class Funcoes(unittest.TestCase):
   def correcaoDeNomes(self):
      entradas_e_saidas = (
         ("um_dia_atras", "UM_DIA_ATRAS"),
         ("como vai você", "COMO_VAI_VOCE"),
         ("_valor_do_inteiro", "VALOR_DO_INTEIRO"),
         ("um dia   será mais bonito que vocẽ",
         "UM_DIA_SERA_MAIS_BONITO_QUE_VOCE"),
         ("um  tipo   de     variável esquesita",
         "UM_TIPO_DE_VARIAVEL_ESQUESITA")
      )

      for (e, s) in entradas_e_saidas:
         print(e, "===>", ajusta_variavel(e))
         self.assertEqual(ajusta_variavel(e), s)
   ...

   def minimizacaoDeEspacos(self):
      entradas_e_saidas = [
         ("hoje é um novo dia","hoje é um novo dia"),
         ("tem várias   coisas", "tem várias coisas"),
         ("vamos tentar  com   vários    espaços",
         "vamos tentar com vários espaços"),
         ("   isso é      uma   aberração  !",
         " isso é uma aberração !")
      ]
      funcao = minimiza_espacos
      for (e, s) in entradas_e_saidas:
         saida = "".join(funcao(e))
         print("'{}' >>> '{}'".format(e, saida))
         self.assertEqual(saida, s)
      ...
   ...

   def gravacaoELeituraEmDisco(self):
      def selo_de_tempo_randomico() -> DT:
         return DT.datetime(
            random.randint(1978, 2005),
            random.randint(1, 9),
            random.randint(5, 27),
            hour=random.randint(7, 16),
            minute=random.randint(16, 52),
            seconds=random.randint(1, 30)
         )
      ...
      entrada = {
         "MAL_DE_SUBITO": [False, selo_de_tempo_randomico()],
         "NAO_FOI_HOJE": [True, selo_de_tempo_randomico()],
         "DIA_DO_BANHO_DE_SOL":[False, selo_de_tempo_randomico()],
         "JA_ANOITECIDO": [False, selo_de_tempo_randomico()]
      }
      # registra em discos.
      grava_em_disco(entrada)

      def datas_quase_iguais(d1: DT, d2: DT) -> bool:
         return (
            d1.hour == d2.hour and
            d1.minute == d2.minute and
            d1.second == d2.second
         )
      ...
      # lê o que está registrado.
      saida = le_do_disco()
      for (e, s) in zip(entrada.items(), saida.items()):
         self.assertEqual(e[0], s[0])
         self.assertEqual(e[1][0], s[1][0])
         self.assertTrue(datas_quase_iguais(s[1][1], e[1][1]))
      ...
   ...

   def copiaBDTextoParaBDBinario(self):
      self.assertFalse(Path(CAMINHO_BINARIO_BD).exists())
      copia_bd_texto_para_bd_binario()
      self.assertTrue(Path(CAMINHO_BINARIO_BD).exists())
      remove(CAMINHO_BINARIO_BD)
   ...

   def lendoBDBinario(self):
      self.assertFalse(Path(CAMINHO_BINARIO_BD).exists())
      clona_para_bd_binario()
      variaveis = le_em_disco_binario()
      for (n, (vl, t)) in variaveis.items():
         T = DT.today()
         decorrido = (T - t).total_seconds()
         print(n, vl, tempo(decorrido), sep="::==::")
      ...
      remove(CAMINHO_BINARIO_BD)
      self.assertFalse(Path(CAMINHO_BINARIO_BD).exists())
   ...

   def runTest(self):
      self.correcaoDeNomes()
...

class Classes(unittest.TestCase):
   def runTest(self):
      self.instanciaBasicaSemBD()

   def instanciaBasicaComBD(self):
      print("caminho =", CAMINHO_BD)
      self.assertTrue(exists(CAMINHO_BD))
      table = TabelaBooleana()
      print("total de variáveis: {}".format(len(table)))
   ...

   def instanciaBasicaSemBD(self):
      table = TabelaBooleana()
      self.assertEqual(table.variaveis, {})
   ...

   def escreveAlgumasVariaveis(self):
      table = TabelaBooleana()
      table["está de dia"] = True
      table["está chovendo"] = False
      del table

      # pausa de meio-segundo.
      #sleep(0.200)

      new_table = TabelaBooleana()
      self.assertTrue(new_table["ESTA_DE_DIA"])
      self.assertFalse(new_table["ESTA_CHOVENDO"])
   ...

   def impressaoDaTabela(self):
      table = TabelaBooleana()
      print(table)

   def iteracaoDaTabela(self):
      tabela = TabelaBooleana()
      for (nome, valor_logico) in tabela:
         print("nome: {} \t valor: {}".format(nome, valor_logico))
   ...

   def colocandoNovaVariavel(self):
      print("ambos BDs já tem que existir.")
      self.assertTrue(exists(CAMINHO_BD))
      table = TabelaBooleana()
      total_vars = len(table)
      print("total de variáveis: {}".format(total_vars))
      table["tempo nublAdo"] = True
      table.salva()
   ...
...


if __name__ == "__main__":
   unittest.main(defaultTest=Classes)
...

