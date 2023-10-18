
"""
 Ferramentas muitos úteis para vários códigos,
que são um Temporizador e um Cronômetro. Para
quem não conhece nenhuma, a primeira faz uma
contagem regressiva; já a segunda conta por
tempo "indeterminados", porém possível de ter
marcos(registros arbitrários) durante a contagem.
"""
from time import (time, time_ns)
from datetime import timedelta

__all__ = [
   "CronometroParadoError",
   "TempoEsgotadoError",
   "Temporizador",
   "Cronometro"
]

class TempoEsgotadoError(Exception):
   def __str__(self):
      return "O temporizador não pode atualizar mais."
...

class CronometroParadoError(Exception):
   def __init__(self, msg_erro):
      self.mensagem = msg_erro
   def __str__(self):
      if msg_erro != "":
         return "O cronômetro foi parado."
      else:
         return self.mensagem
   ...
...

class Temporizador:
   def __init__(self, tempo):
      "se o tempo não for um 'delta', será considerado como segundos."
      self._registro_inicial = int(time())
      if isinstance(tempo, (int, float)):
         nos_nanos = (tempo <= pow(10, -9))
         if isinstance(tempo, float) and nos_nanos:
            mensagem_erro = (
               "valor na faixa dos 'nanos', ainda não "
               + "se trabalha com valores nesta ordem "
               + "de grandeza."
            )
            raise ValueError(mensagem_erro)
         ...
         # segundos registrado até agora de uma
         # data inicial marcada, convertido a um
         # valor inteiro.
         self._limite = tempo
      elif isinstance(tempo, timedelta):
         self._limite = tempo.total_seconds()
      else:
         mensagem_erro = (
            "só são aceitos valores do tipo 'int', 'float' " +
            "ou 'duration'. O primeiro para casos em segundos " +
            "inteiros; o segundo segundos inteiros ou também" +
            "frações mistas; e o último um construto especial " +
            "para durações de tempo, com precisão de microsegundos."
         )
         raise TypeError(mensagem_erro)
      ...
      # marco inicial.
      self._atual = 0
      # chamadas num temporizador isolado.
      self._ciclos = 0
      # total de reutilizações.
      self._reutilizacoes = 0
   ...
   def __call__(self):
      """
      chamada, atualiza tempo decorrido. Se alcançou
      o tempo delimitado. Retorna True em cada chamada
      validando a existência do Temporizador, False caso
      tenha sido esgotado. Se houver insistência em
      chamar mesmo assim, uma exceção será levantada.
      """
      if self._atual >= self._limite:
         if self._ciclos > 5:
            # chamar um bocado de vezes um Temporizador
            # esgotado, apenas retorna um erro. Se quer
            # reutiliza-lô chame a função específica
            # para isso.
            raise TempoEsgotadoError()
         else:
            self._ciclos += 1
         return False
      ...

      # atualizando atual tempo decorrido.
      self._atual = time() - self._registro_inicial
      return True
   ...
   def percentual(self):
      "verifica o percentual decorrido em segundos"
      # primeiro atualizando dados...
      self()
      if self._atual > self._limite:
         return 1.0
      else:
         return self._atual / self._limite
   ...
   def agendado(self):
      "retorna a duração que você impos ao Temporizador."
      # primeiro atualizando o tempo ...
      self()
      return timedelta(seconds=self._limite)
   ...
   def __lt__(self, tempo) -> bool:
      if isinstance(tempo, (timedelta, int, float)):
         if isinstance(tempo, timedelta):
            tempo = tempo.total_seconds()
      ...
      # primeiro atualizando o tempo ...
      self()
      # contagem atual está em ...
      contagem = self._limite - self._atual
      return contagem <= tempo
   ...
   def __gt__(self, tempo) -> bool:
      if isinstance(tempo, (timedelta, int, float)):
         if isinstance(tempo, timedelta):
            tempo = tempo.total_seconds()
      ...
      # primeiro atualizando o tempo ...
      self()
      # contagem atual está em ...
      contagem = self._limite - self._atual
      return contagem > tempo
   ...
   def __bool__(self) -> bool:
      """
      retorna 'true' enquanto o temporizador
      está ativo(não esgotado), 'false' se
      esgotou-se.
      """
      # também tenta atualiza a contagem.
      try: self()
      except TempoEsgotadoError: pass
      return self._atual < self._limite
   ...
   def __str__(self) -> str:
      try:
         from legivel import tempo as Tempo
      except ImportError:
         raise ImportError("sem a biblioteca necessária.")
      else:
         decorrido = self._limite - self._atual
         return Tempo(decorrido, True)
      ...
   ...
   def reutiliza(self) -> int:
      """
      Reseta todas contagem do Temporizador. Retorna
      a atual quantidade de reutilizações do Temporizador
      até o momento.
      """
      # contagem do número de chamadas permitidas
      # sem erros, também resetada.
      self._ciclos = 0
      self._registro_inicial = int(time())
      # variação zero até aqui.
      self._atual = self._registro_inicial
      # conta o nº de reutilizações.
      self._reutilizacoes += 1
      # retorna a atual contagem.
      return self._reutilizacoes
   ...
...

from legivel import tempo
import statistics

class Cronometro:
   """
   Cronômetro, contador de tempo. Opera na faixa dos nanosegundos.
   Todos retornos aqui são na grandeza de segundos. Computa tanto
   o tempo desde o começo, como também o decorrido desde à última
   marcação; computa também a média de variação das marcações.
   """
   # contabilização das instâncias deste tipo de dado.
   total = 0

   def __init__(self) -> None:
      # marca o ínicio da estrutura.
      self.inicio: int = time_ns()
      # registra marcos durante a contagem, e os salvas. O primeiro
      # valor, será o que acabou de ser marcado.
      self.registros: [int] = [self.inicio]
      # contabilização das instância...
      Cronometro.total += 1
      # muda estado do cronômetro para terminado, equivalente ao
      # 'esgotado' do Temporizador. Também, pega o último registro
      # de tempo antes de parar.
      self.terminado: bool = False
      self.ultimo_registro: int = None
   ...

   def marca(self) -> float:
      if self.terminado:
         msg_error = "não marca mais, já foi 'esgotado'"
         raise CronometroParadoError(msg_error)

      # calculando o tempo decorrido em segundos.
      fim = time_ns()
      decorrido = (fim - self.inicio) * pow(10, -9)
      # adicionando 'marco' na fila.
      self.registros.append(fim)

      # decorrido até o momento, o mesmo que adicionado a fila.
      return decorrido
   ...

   def variacao(self) -> int:
      "retorna variação desde o último 'marco' realizado em nanosegundos"
      t = len(self.registros) - 1
      ultimo = self.registros[t]
      return (ultimo - inicio)
   ...

   def media(self) -> float:
      "computa a média aritmética das variações entre os marcos"
      return statistics.mean(
         abs(a - b) * pow(10, -9)
         for (a, b) in zip (
            self.registros[1:],
            self.registros[:-1]
         )
      )
   ...

   def __str__(self) -> str:
      if self.terminado:
         decorrido_ns = abs(self.inicio - self.ultimo_registro)
      else:
         decorrido_ns = abs(self.inicio - time_ns())

      # converte o tempo para segundos.
      segundos = decorrido_ns * pow(10, -9)

      # retira a parte fracional de valores muitos pequenos, digo,
      # até os minutos.
      if segundos < 60:
         tempo_str = tempo(
            segundos,
            acronomo = True,
            arredonda = True
         )
      else:
         tempo_str = tempo(segundos, acronomo = True)
      if self.terminado:
         return "{}(terminou)".format(tempo_str)
      else:
         return tempo_str

   def __repr__(self) -> str:
      return self.__str__()

   def __del__(self):
      # removendo está instância da contagem.
      Cronometro.total -= 1

   def parar(self):
      """
      para a contagem do tempo de vez, assim não é possível fazer
      mais 'marcações', e a variação é fixa, assim també fica a
      média.
      """
      self.terminado = True
      self.ultimo_registro = time_ns()
   ...

   def listar(self) -> None:
      "funciona na faixa dos nanosegudos até 24 horas"
      if self.registros == []:
         print("sem qualquer 'marco'.")
         return None

      for marco in self.registros:
         decorrido = abs(marco - self.inicio) * pow(10, -9)

         if decorrido == 0:
            continue

         tempo_str = tempo(decorrido, acronomo=True, arredonda=True)
         print("[{:^10}]".format(tempo_str))
      ...
   ...

   def __lt__(self, cronometro) -> bool:
      """
      verifica se este 'cronômetro' tem um tempo decorrido menor que
      o passado.
      """
      # para teste com cronômetros.
      if isinstance(cronometro, Cronometro):
         # o tempo decorrido de ambos cronômetros.
         d = cronometro.marca()
         D = self.marca()

         # removendo os registros deles pelo método 'marca', já que
         # internamente ele adiciona o último registro feito no fim
         # da 'deque' interna.
         self.registros.pop(); cronometro.registros.pop()

         return  D <  d
      # teste com tipos inteiros ou decimais represetando segundos.
      elif isinstance(cronometro, int | float):
         segundos = cronometro
         instancia_seg = self.marca()

         # removendo novamente registro de 'marco' adicionado
         # automaticamente pelo método usado.
         self.registros.pop()

         return instancia_seg < segundos
      else:
         raise ValueError("o valor passado não é um Cronômetro")
   ...

   def __eq__(self, cronometro) -> bool:
      """
      mede a igualdade de tempos decorridos entre este cronômetro, e
      outro, ou um tempo númerico, decimal ou inteiro, dado nas
      de segundos.
      """
      if isinstance(cronometro, Cronometro):
         d = cronometro.marca()
         D = self.marca()
         self.registros.pop(); cronometro.registros.pop()
         # com frações extramentes pequenas, é possível que uma
         # pequeníssima parte faça a diferença, então a representação
         # visual faz a diferença na igualação.
         return  D == d or (str(self) == str(cronometro))
      elif isinstance(cronometro, int | float):
         segundos_instancia = self.marca()
         segundos = cronometro
         self.registros.pop()
         # cinco porcento de error permitido.
         if segundos > segundos_instancia:
            return (segundos_instancia / segundos) < 0.05
         else:
            return (segundos / segundos_instancia) < 0.05
      else:
         raise ValueError("o valor passado não é um Cronômetro")
   ...

   def __gt__(self, cronometro) -> bool:
      """
      verifica se este 'cronômetro' contou um tempo maior,
      que o cronômetro passado.
      """
      # o modo de fazer isso é, verificar se não é menor, ou
      # igual ao tempo percorrido, logo só pode ser maior.
      return not(self < cronometro or self == cronometro)
   ...
...

def stringtime_to_segundos(string):
   caracteres = []
   # remove todos espaços brancos.
   for char in string:
      if not char.isspace():
         caracteres.append(char)
   ...
   # acha divisor entre peso e parte numérica.
   marco = None
   for (i, char) in enumerate(caracteres):
      if char.isalpha():
         marco = i
         break
      ...
   ...
   # transformando em respectivos objetos.
   digitos = float(''.join(caracteres[0:marco]))
   peso = ''.join(caracteres[marco:])

   if marco == None:
      raise Exception("argumento mal formado: %s" % string)

   if peso.startswith("min") or peso == "m":
      return digitos * 60
   elif peso.startswith("seg") or peso == "s":
      return digitos
   elif peso.startswith("hora") or peso == "h":
      return digitos * 3600
   elif peso.startswith("dia") or peso == "d":
      return digitos * 3600 * 24
   else:
      raise Exception("não implementado para tal")
...


from unittest import (main, TestCase)
from time import sleep
from random import (randint, choice)

class TemporizadorTeste(TestCase):
   def verificaEsgotamento(self):
      timer = Temporizador(1.5)
      self.assertTrue(bool(timer))
      sleep(1.6)
      self.assertFalse(bool(timer))
   ...
   def seuPercentual(self):
      timer = Temporizador(1.5)
      for _ in range(1, 15):
         try:
            print(
               "o temporizador está em %0.1f%%"
               % (timer.percentual() * 100.0)
            )
         except TempoEsgotadoError:
            print("já se esgotou.")
         sleep(0.2)
      ...
      self.assertFalse(bool(timer))
   ...
   def metodoReutilizacao(self):
      timer = Temporizador(1.5)
      self.assertTrue(bool(timer))
      sleep(1.6)
      self.assertFalse(bool(timer))
      for _ in range(5):
         try: timer();
         except TempoEsgotadoError:
            print("já foi esgotado!")
      ...
      self.assertFalse(bool(timer))
      total = timer.reutiliza()
      self.assertEqual(total, 1)
      self.assertTrue(bool(timer))
      sleep(1.6)
      self.assertFalse(bool(timer))
   ...
   def agendadoRetorno(self):
      timer = Temporizador(5.2)
      resultado = timer.agendado()
      self.assertTrue(isinstance(resultado, timedelta))
      self.assertEqual(resultado.seconds, 5)
      self.assertEqual(resultado.microseconds, 200_000)
   ...
   def visualDoTemporizadorDebug(self):
      timer = Temporizador(1.5)
      for _ in range(1, 15):
         try:
            print(
               "[%s] o temporizador está em %0.1f%%"
               % (timer, timer.percentual() * 100.0)
            )
         except TempoEsgotadoError:
            print("já se esgotou.")
         sleep(0.2)
      ...
      self.assertFalse(bool(timer))
   ...
...

def pausa_de_miliseg_ou_seg():
   if choice([True, False]):
      tempo_aleatorio = randint(1, 10) / 10
   else:
      tempo_aleatorio = randint(1, 100) / 100
   sleep(tempo_aleatorio)
   return tempo(tempo_aleatorio)
...

class CronometroTeste(TestCase):
   def exemploSimples(self):
      c = Cronometro()
      for _ in range(10):
         print("registro do tempo:", c)
         print("pausa de", pausa_de_miliseg_ou_seg())
      ...

      pausa_de_miliseg_ou_seg()
      print("registro do tempo:", c)
      pausa_de_miliseg_ou_seg()
      print("registro do tempo:", c)

      c.parar()

      print("registro do tempo:", c)
   ...

   def mediaDeRegistros(self):
      c = Cronometro()
      for _ in range(105):
         print("pausa de", pausa_de_miliseg_ou_seg())
         c.marca()
      ...

      M = c.media()
      print("valor:", M)
      print("média: {}".format(tempo(c.media(), arredonda=True)))

      c.parar()
      print("registro do tempo:", c)
   ...

   def listagemDosMarcos(self):
      c = Cronometro()
      for _ in range(50):
         pausa_de_miliseg_ou_seg()
         c.marca()
         print(".", end="")
      ...

      print("\npronto!", end="\n\n")
      c.listar()
   ...

   def comparacaoEntreCronometros(self):
      (c, C) = (Cronometro(), Cronometro())

      self.assertEqual(Cronometro.total, 2)

      for _ in range(7):
         pausa_de_miliseg_ou_seg()
         self.assertEqual(c, C)
         print(".", end="")
      ...
      print("\tpronto!", end="\n\n")

      del C, c
      # verificando contagem de instâncias ...
      self.assertEqual(Cronometro.total, 0)

      # reiniciando, e começando novamente, para testa agora
      # não igualdade entre eles.
      c = Cronometro()
      pausa_de_miliseg_ou_seg()
      C = Cronometro()
      self.assertTrue(c > C)
      self.assertTrue(C < c)
      print("c(%s) > C(%s)" % (c, C))

      # testando inequality com outros tipos de dados.
      print("c(%s) < 3 seg" % c)
      self.assertTrue(c < 3)
      pausa_de_miliseg_ou_seg()
      print("c(%s) < 16.8 seg" % c)
      self.assertTrue(c < 16.8)
   ...
...


''' testes obsoletos.
if __name__ == "__main__":
   import utilitarios.src.testes as UT
   from time import sleep

   def strtime_to_seg():
      argumentos = (
         "15min", "38 segundos", "3.5 horas",
         "15.0 min", "38 seg", "3h", "4.53 h",
         "5.8 min    ", "   89     segundos",
         "3      hfak",  " 12   dios",
      )
      for arg in argumentos:
         try:
            conversao = stringtime_to_segundos(arg)
            print("%s ==> %iseg" % (arg, conversao))
         except:
            print("[%s] mal formado!!" % arg)
         ...
      ...
   ...

   def usa_temporizador():
      t = Temporizador(stringtime_to_segundos("13seg"))
      while t():
         porcentagem = t.percentual() * 100
         print("\r%0.1f%%" % porcentagem, end = '')
      else:
         print("esgotado!".upper())
      ...

      # induzindo ao erro.
      for _ in range(15):
         try:
            print("resultado: ", t())
         except TempoEsgotadoError():
            print("induzido com sucesso!")
            break
         ...
      ...
   ...

   def comparaTemporizador():
      tempo = stringtime_to_segundos("1.3min")
      a = Temporizador(tempo)
      sleep(20)
      # está em 58seg
      print("agora têm que ser menor que 59.")
      assert a < 59
      print("agora têm que ser menor que 51.")
      sleep(7)
      assert a < 51
   ...
...
'''

if __name__ == "__main__":
   main(verbosity=2)
