
"""
 Ferramentas muitos úteis para vários códigos,
que são um Temporizador e um Cronômetro. Para
quem não conhece nenhuma, a primeira faz uma 
contagem regressiva; já a segunda conta por
tempo "indeterminados", porém possível de ter
marcos(registros arbitrários) durante a contagem.
"""
from time import time
from datetime import timedelta

__all__ = ["TempoEsgotadoError", "Temporizador", "Cronometro"]

class TempoEsgotadoError(Exception):
   def __str__(self):
      return "O temporizador não pode atualizar mais."
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

class Cronometro: pass

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
   main()
