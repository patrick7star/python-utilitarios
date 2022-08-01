
"""
Tipos de visualização de qualquer lista
de elementos que for passada.
"""

# meu módulos:
from arvore import matriciar_string
# biblioteca do Python:
from copy import deepcopy
from shutil import get_terminal_size
import array as Array


def listagem(strings):
   # largura do terminal.
   largura = get_terminal_size().columns
   # comprimento da maior string.
   maior = max(len(s) for s in strings)
   # acumulador para concatenação; contador
   # de entradas por linha; e espaço entre
   # entradas.
   (contador, espaco, linhas) = (1, 2, [])

   # entradas por linha.
   total_na_linha = (largura-1) // (maior+espaco) 
   # quantos entradas modificadas serão
   # listadas ao todo.
   total = maior * len(strings)
   while total > 0:
      # remove entrada até que se esgote.
      # Para aí então, acabar o loop.
      try:
         entrada = strings.pop()
      except IndexError:
         break
      # cria uma string baseado na maior
      # entrada, preenchendo os vácuos 
      # restantes com "espaço vázio".
      comprimento = len(entrada)
      diferenca = abs(maior-comprimento)
      aux = entrada + ' ' * (diferenca + espaco)
      linhas.append(aux)

      # passou do limite na linha, então vai
      # a próxima.
      if contador % total_na_linha == 0:
         linhas.append('\n')
      total -=1
      contador += 1
   ...
   
   return "".join(linhas)
...

class Pilha:
    def __init__(self):
       self._array = Array.array('B')
       self._qtd = 0
    ...
    
    def topo(self):
       raise Exception("[ERROR]não implementada ainda!")
    
    def empilha(self, valor):
       self._array.append(valor)
       self._qtd += 1
    
    def desempilha(self):
       if self.vazia():
           raise Exception("[PILHA VÁZIA]")
       remocao = self._array.pop(self._qtd - 1)
       self._qtd -= 1
       return remocao
    ...
    
    def vazia(self):
       return len(self._array) == 0
...

def escada(strings):
   "impressão na forma de escada"
   largura = get_terminal_size().columns
   colidiu_na_parede = False
   linhas = []
   acumulado = 0
   pilha_de_recuos = Pilha()
   
   for entrada in strings:
      recuo = " " * acumulado
      comprimento = len(entrada)
      linhas.append(recuo)
      linhas.append(entrada)
      linhas.append('\n')
      
      if (comprimento + acumulado < largura-5
      and  not colidiu_na_parede):
         meio_str = comprimento //2
         acumulado += meio_str
         pilha_de_recuos.empilha(meio_str)
      else:
         if not pilha_de_recuos.vazia():
            acumulado -= pilha_de_recuos.desempilha()
            colidiu_na_parede = True
         else:
            colidiu_na_parede = False
      ...
   ...
   
   return "".join(linhas)
...

def silhueta(string):
   matriz = matriciar_string(string)
   (m, n) = len(matriz), len(matriz[0])
   outra = deepcopy(matriz)
   # lista para concatenação.
   celulas = Array.array('u')
   
   for i in range(m):
      for j in range(n):
         proposicao = (
            (not matriz[i][j].isspace()) and
            matriz[i][j]!='¨'
         )
         if proposicao: 
            outra[i][j] = '~'
         elif matriz[i][j] == '¨': 
            outra[i][j] = ' '
      ...
   ... 
   
   for i in range(m):
      for j in range(n): 
         celulas.append(outra[i][j])
      celulas.append('\n')
   ...
   return "".join(celulas)
...

# excluindo resto de módulos importados.
#del deepcopy
#del matriciar_string


# o que será importado:
__all__ = ["listagem", "escada", "silhueta"]

if __name__ == "__main__":
    array = [
       "pasta1", "pasta 2", "paste III",
       "configuração.txt", "nada_de_mais.dat",
       "total_porno_aqui.jpg", "arquivosinúteis.txt",
       "arquivo_um.cc", "arquivo_sem_uso", 
       "diretório_qualquer", "rising house",
       "new horleans"
    ]
    
    def testa_listagem():
       print(listagem(array))
    ...
    
    def testa_escada():
       for e in ["memes", "floresta_de_dirs",
       "pasta vázia", "arquivos-binários", 
       "músicas instrumentas"]:
           array.append(e)
       print(escada(array))
    ...
    
    def testa_silhueta():
       # apresentando silhueta.
       string = """rosas são vermelhas
       \rvioletas são azuis
       \rbreve rima brega
       \rsalgadinho de alcasuís"""
       print(string)
       print(silhueta(string))

       poesia = '''chove chuva
       \rchove sem parar
       \rchove chuva
       \rchove sem parar
       \rhoje é vou fazer uma prece
       \rpara deus, nosso senhor
       \rpara chuvar parar
       \rde molhar o meu divino amor
       \rque é muito lindo
       \ré mais que o infinito
       \ré puro e belo
       \rinocente como uma flor
       \rpor favor chuva ruin
       \rnão molhe mais o meu amor assim
       \rpor favor chuva ruuuiinn
       \rnão molhe mais o meu amoor assim'''
       print(poesia)
       print(silhueta(poesia))
    ...
    
    from testes import executa_teste
    executa_teste(testa_listagem)
    executa_teste(testa_escada)
    executa_teste(testa_silhueta)
...
