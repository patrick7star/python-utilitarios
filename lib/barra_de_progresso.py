'''
    Uma barra de progresso para visualizar
o quanto foi feito da tarefa, dado os valores:
a ser atingindo, e o quanto está no momento.
'''
#bibliotecas:
import os, sys, decimal, threading
from time import sleep, time
# meus módulos:
import legivel


# dados:
texto_molde = '{0:>{espaco}} de {1}: [{2}]{3:>5.1f}%'
texto_molde_i = '{0}/{1}: [{2}]{3:>5.1f}%'

# minhas próprias classe-exeções:
class PorcentagemError(ValueError): pass

class FimDoProgressoError(ValueError):
   def __init__(self, progresso):
      # armazena a barra de progresso cheia.
      self.progresso = progresso

class NaoCabeNaTelaError(Exception):
   def __init__(self, largura):
      self.largura = largura
   def __str__(self):
      larguraTERM = int(os.get_terminal_size().columns)
      X = abs(self.largura - larguraTERM)
      return ("a barra excede a tela, por favor redimensione-a"+
            " em %i caractéres para que possa"%(X)+
            " executar novamente sem distorções.")


# Função auxiliar na criação da barra de progresso.
# Ela cria o progresso em sí.
def constroi_barra(percentagem, simbolo, capacidade):
    # levanta uma exceção em caso de uma porcentagem exagerada.
    if percentagem > 1:
      raise PorcentagemError(percentagem)
    # símbolo que expressa "espaço vázio".
    vazio = "."
    vazio = '.'   # alternativas
    #número de partes da barra de progresso.
    n_barras = int(capacidade * percentagem)
    #qtd. de espaços vázios.
    n_espacos_brancos = capacidade - n_barras
    return (simbolo*n_barras)+(vazio*n_espacos_brancos)


# Retorna a barra de progresso toda personalizada.
# Há dois modos, a que contam numéricamente, e a 
# que leva em consideração que está-se trabalhando
# com grandezas digitais. 
def progresso(qtd_atual, qtd_total, dados=False):
   "retorna uma string contendo informações, e a barra de progresso"
   #porcentagem da tarefa realizada.
   percentagem = qtd_atual / qtd_total

   #medindo algarismos dos números.
   espacamento = len(str(qtd_total))

   # dimensão da tela para ver se tal barra cabe.
   largura = os.get_terminal_size().columns

   # se a opção "dados" estiver ativada, então
   # trocar a "impressão" para os dados.
   if dados:
      encurta = dict(acronomo=True,unidade='byte',sistema='metrico')
      try:
         # uma barra personalizada.
         barra = constroi_barra(percentagem, 'o', 50)

      except PorcentagemError:
         barra = constroi_barra(1.0, '#', 50)
         # conversões os valores de bytes para 
         # legendas legíveis.
         str_atual = legivel.tamanho(qtd_atual,**encurta)
         str_total = legivel.tamanho(qtd_total,**encurta)
         encurta = (str_total, str_total, barra, 100)

      else:
         # conversões os valores de bytes para 
         # legendas legíveis.
         str_atual = legivel.tamanho(qtd_atual,**encurta)
         str_total = legivel.tamanho(qtd_total,**encurta)
         encurta = (str_atual, str_total, barra, percentagem*100)
      
      # retorno de string baseado na percentagem.
      if percentagem == 1:
         # verifica se o texto não excede a largura da 
         # tela de exibição, se sim, "executa" um erro.
         L = len(texto_molde_i.format(*encurta, espaco=espacamento))
         if L+1 > largura:
            raise NaoCabeNaTelaError(len(texto_molde_i)+1)
         return texto_molde_i.format(*encurta,espaco=espacamento)+'\n'

      elif percentagem > 1:
         progresso_str = texto_molde_i.format(*encurta, espaco=espacamento)
         raise FimDoProgressoError(progresso_str)

      else:
         # "executa" um erro me caso de não ajuste
         # na tela de exibição.
         L = len(texto_molde_i.format(*encurta, espaco=espacamento))
         if len(texto_molde_i)+1 > largura:
            raise NaoCabeNaTelaError(len(texto_molde_i)+1)
         return texto_molde_i.format(*encurta,espaco=espacamento)
   else:
      try:
         #sub-string para barra de progresso.
         barra = constroi_barra(percentagem, '#', 50)

      except PorcentagemError:
         barra = constroi_barra(1.0,'#', 50)
         encurta = (qtd_total, qtd_total, barra, 100)

      else:
         # o padrão...
         encurta = (qtd_atual, qtd_total, barra, percentagem*100)

      # retorna uma quebra de linha ou não.
      if percentagem == 1:
         # erro em caso de não ajusta à tela.
         L = len(texto_molde.format(*encurta, espaco=espacamento))
         if L+1 > largura:
            raise NaoCabeNaTelaError(L+1)
         return texto_molde.format(*encurta,espaco = espacamento)+'\n'

      elif percentagem > 1:
         progresso_str = texto_molde.format(*encurta, espaco=espacamento)
         raise FimDoProgressoError(progresso_str)

      else:
         # erro em caso de não ajusta à tela.
         L = len(texto_molde.format(*encurta, espaco=espacamento))
         if L+1 > largura:
            raise NaoCabeNaTelaError(L+1)
         return texto_molde.format(*encurta,espaco = espacamento)


bloqueador = threading.Lock()
class Rotatoria(threading.Thread):
   """ classe que trata do texto e sua
   exibição como uma rolagem. """
   def __init__(self, texto, maximo):
      """ método construtor: cria uma lista dado
      o texto, e armazena o seu limite ao ser
      impresso(sua capacidade). """
      espaco = ' ' * 2 # espaços em branco.
      # concatena espaços para fazer uma separação
      # visual no momento de exibição. A variável
      # é uma lista contendo os caractéres da 
      # string que foi passada.
      self.corrente = list(espaco+texto+espaco)
      self.capacidade = maximo
      threading.Thread.__init__(self)

   def run(self):
      """ implementação que será executada ao 
      iniciar uma thread. Aqui, pegará o último
      elemento da lista e o removerá, posteriormente
      colocará-lo no começo da lista. Isto tudo
      levando um terço de segundo, de modo 
      proposital. """
      for k in range(48):
         sleep(0.3)  # aguarda um 1/3 de segundo para deslocar...
         # remove à última posição e a coloca na 
         # primeira parte.
         char = self.corrente.pop()
         self.corrente.insert(0,char)

   def __repr__(self):
      """ quando 'print' a instância, pega 
      a lista, na mesma ordem, e a transforma
      numa string. """
      texto = ""
      for k in range(self.capacidade):
         bloqueador.acquire()
         texto += self.corrente[k]
         bloqueador.release()
      return texto

class TextoMovimento(Rotatoria):
   def __init__(self, texto, maximo):
      # executa construtor da super classe.
      super().__init__(texto, maximo)
      # razão da quantidade feita, pela quantidade
      # total a ser feita; começa em zero por 
      # instânciar tal classe.
      self.progresso = 0
      # texto original passado.
      self.string= texto

   def run(self):
      # executa o loop até que se atinga 100%.
      while self.progresso < 1.00:
         sleep(0.3)  # aguarda um 1/3 de segundo para deslocar...
         # remove à última posição e a coloca na 
         # primeira parte.
         bloqueador.acquire()
         char = self.corrente.pop()
         self.corrente.insert(0,char)
         # se já alcançou 100%, para loop,
         # consequentemente para thread.
         bloqueador.release()

   def atualiza_progresso(self,novo):
      " atualiza a fração de progresso"
      self.progresso = novo

   def __repr__(self):
      if len(self.string) < self.capacidade:
         return self.string
      else:
         return super().__repr__()


def progresso_rotulo(rotulo, qtd_atual, qtd_total,
dados=False, dinamico=True):
   """
   retorna string contendo barra de progresso, porém com um
   rótulo, que também é animado caso preciso. O modo
   dinâmico é o padrão, tal modo é preciso ter a razão
   m/n, em que m=n, pois só encerra tal execução assim. O
   oposto/desativação disto é o estático, onde a execução
   termina na única impressão; tais modos alternativos
   traduzem-se na movimentação ou não do rótulo.
   """
   # já pega a barra pronta de funções anteriores.
   barra_progresso = progresso(qtd_atual, qtd_total, dados)
   # largura atual da tela do terminal.
   larguraTERM = os.get_terminal_size().columns
   p = qtd_atual/qtd_total # percentagem

   if dinamico:
      global aux
      try:
         aux.atualiza_progresso(p)
         str_aux = "{%s} %s" % (str(aux), barra_progresso)
         # se for 100%, apenas deleta instância
         # que girá texto.
         if p == 1: del aux
         # lança erro se não couber na tela.
         if len(str_aux)+1 > larguraTERM:
            # para interrompter a thread.
            aux.atualiza_progresso(1)
            del aux  # exclui instância.
            raise NaoCabeNaTelaError(len(str_aux)+1)
         # retorna string.
         return str_aux

      except NameError:
         # texto rotatório.
         aux = TextoMovimento(rotulo, 20)
         aux.start()  # inicia thread.
         # chama função novamente após ter criado
         # a instância necessária.
         return progresso_rotulo(rotulo, qtd_atual, qtd_total)
   else:
      if len(rotulo) > 20:
         return "{%s...} %s" % (rotulo[:20],barra_progresso)
      else:
         return "{%s} %s"%(rotulo, barra_de_progresso)


def progresso_redimensionavel(qtd_atual, qtd_total):
   """
   retorna uma string contendo informações, e a barra de
   progresso, assim com a outra, porém este, especifícamente
   o progresso(parte do carregamento) é redimensionável de
   acordo com a dimensão da janela, e também preenche-a
   completamente.
   """
   #porcentagem da tarefa realizada.
   percentagem = qtd_atual / qtd_total
   if percentagem > 1:
      raise PorcentagemError("não pode haver mais de 100%")

   #medindo algarismos dos números.
   espacamento = len(str(qtd_total))

   # quantia de caractéres espaçados da string.
   qtd_espacada = 9
   # nº de algarismos de cada número. Na verdade
   # do total, pois o "atual" cresce.
   total_algs = 2*len(str(qtd_total))

   # dimensão da tela para ver se tal barra cabe.
   largura = os.get_terminal_size().columns

   # o que sobra para preencher com a barra. O que é 
   # contabilizado aqui é, o demais textos e símbolo
   # da barra de progresso inteira; os espaços para 
   # números que crescem; a quantia de algarismos de
   # cada número; a quantia de algarismos da porcentagem
   # que também aparece. A diferença entre isto e, a largura
   # da tela, nos dá o comprimento ideal do progresso.
   resto = largura-(qtd_espacada+espacamento+total_algs+4)

   # barra de progresso em sí.
   simbolo = '\ua4ff'
   barra = constroi_barra(percentagem, simbolo, resto)

   if percentagem == 1.0:
      return texto_molde.format(qtd_atual, qtd_total, barra,
                             percentagem*100, espaco=espacamento)+'\n'
   else:
      return texto_molde.format(qtd_atual, qtd_total, barra,
                             percentagem*100, espaco=espacamento)


class ProgressoPercentual():
   """
   Barra que retorna string dado uma variação
   percentual razoável. A impressão sempre tem
   que ser tratada, pois se não haver variação
   percentual sempre gerará uma exceção no lugar.
   """
   # limite percentual para mostrar a mensagem.
   limite = 1.5

   # construtor.
   def __init__(self, total):
      # máximo a atingir.
      self.qtd_total = total
      # começa do nada, zerado.
      self.qtd_atual = 0
      # percentual do progresso.
      self._percentual = 0.0 * 100
   ...

   # implementação da atualização de valor.
   def __iadd__(self, novo_valor):
      "faz uma atualização do valor via '+=' simbologia"
      # registrando nova quantidade.
      (qt, qa) = (self.qtd_total, self.qtd_atual)
      self._percentual = (qa / qt) * 100
      self.qtd_atual = novo_valor
      return self
   ...

   # implementação da visualização do objeto.
   def __repr__(self):
      "visualização da barra via impressão"
      # apelidos novos para ajudar na legiblidade.
      percentual = self._percentual
      limite = ProgressoPercentual.limite
      # proposições importantes:
      atingiu_limite = (percentual % limite) == 0
      atingiu_total = self.qtd_atual == self.qtd_total
      # veriifcando a variancia de percetual.
      # se tiver "transbordado" mais de 0,5%,
      # então a string real será retornada.
      if atingiu_total or atingiu_limite:
         # terceirizando tarefa de criar uma 
         # barra em sí.
         return progresso(self.qtd_atual, self.qtd_total)
      else:
         # Caso contrário será retornado
         # dado nenhum.
         return "None"
   ...

   def __str__(self):
      "retornando implementação de __repr__"
      return self.__repr__()
...

#[código morto]
class ProgressoTemporal(threading.Thread):
   """
   retornará um impresões num devido tempo
   limitado, e não uma string para cada
   valor atualizado.
   """
   # limite em millisegundos para mostrar a mensagem.
   limite = 3_000

   # construtor.
   def __init__(self, total):
      # máximo a atingir.
      self.qtd_total = total
      # começa do nada, zerado.
      self.qtd_atual = 0
      # valor que indica se tem permissão para 
      # imprimir tal string.
      self.permitido = True
      threading.Thread.__init__(self)
   ...

   def run(self):
      # enquanto não atingir tal valor alternar
      # permissão e interromper por determinado
      # tempo a execução da thread.
      while self.qtd_atual < self.qtd_total:
         # alterna impressão a cada tempo delimitado.
         self.permitido = (not self.permitido)
         # tempo delimitado, interrompe thread.
         tempo = ProgressoTemporal.limite / 1_000
         sleep(tempo)
      else:
         # sempre verdade agora que o progresso
         # foi esgotado.
         self.permitido = True
      ...
   ...

   # implementação da atualização de valor.
   def __iadd__(self, novo_valor):
      "faz uma atualização do valor via '+=' simbologia"
      # registrando nova quantidade.
      self.qtd_atual = novo_valor
      return self
   ...

   # implementação da visualização do objeto.
   def __repr__(self):
      "visualização da barra via impressão"
      # imprime num tempo regular.
      if self.permitido:
         return progresso(self.qtd_atual, self.qtd_total)
      else:
         return "None"
   ...
   def __str__(self):
      "retornando implementação de __repr__"
      return self.__repr__()
...

# nova implementação de outro modo, sem threads.
class ProgressoTemporal_I():
   """
   retornará um impresões num devido tempo
   limitado, e não uma string para cada
   valor atualizado.
   """
   # limite em millisegundos para mostrar a mensagem.
   limite = 700/1_000

   # construtor.
   def __init__(self, total):
      # máximo a atingir.
      self.qtd_total = total
      # começa do nada, zerado.
      self.qtd_atual = 0
      # tempo de inicio.
      self.tempo_inicial = time()
      # permissão de exibição.
      self.permitido = False
   ...

   # implementação da atualização de valor.
   def __iadd__(self, novo_valor):
      "faz uma atualização do valor via '+=' simbologia"
      # para melhor legibilidade ...
      tempo = time()
      diferenca = tempo - self.tempo_inicial
      limite = ProgressoTemporal_I.limite
      # registrando nova quantidade.
      self.qtd_atual = novo_valor
      if diferenca > limite:
         self.permitido = True
         # zera contagem.
         self.tempo_inicial = tempo
      return self
   ...

   # implementação da visualização do objeto.
   def __repr__(self):
      "visualização da barra via impressão"
      # proposições:
      alcancou_o_fim = (
         self.qtd_atual == self.qtd_total
         or self.qtd_atual == 0
      )
      # imprime num tempo regular.
      if self.permitido or alcancou_o_fim:
         # falseando novamente.
         self.permitido = False
         return progresso(self.qtd_atual, self.qtd_total)
      else:
         return str(None)
   ...

   def __str__(self):
      return  self.__repr__()
...

# o que será importado:
__all__ = [
   "PorcentagemError",
   "NaoCabeNaTelaError",
   "progresso",
   "FimDoProgressoError",
   "progresso_rotulo",
   "progresso_redimensionavel",
   "ProgressoPercentual",
   "ProgressoTemporal",
   "ProgressoTemporal_I"
]

