
# meu módulos:
from arvore import matriciar_string
# biblioteca do Python:
from copy import deepcopy

# faz silhueta de matriz.
def silhueta(string):
   matriz = matriciar_string(string)
   m,n = len(matriz), len(matriz[0])
   outra = deepcopy(matriz)
   for i in range(m):
      for j in range(n):
         proposicao = (not matriz[i][j].isspace()) and matriz[i][j]!='¨'
         if proposicao: outra[i][j] = '~'
         elif matriz[i][j] == '¨': outra[i][j] = ' '
   _str = ''
   for i in range(m):
      for j in range(n): _str += outra[i][j]
      _str += '\n'
   return _str

# excluindo resto de módulos importados.
del deepcopy
del matriciar_string


if __name__ == "__main__":
   # apresentando silhueta.
   string = "rosas são vermelhas\nvioletas são azuis\nbreve rima brega\nsalgadinho de alcasuís"
   print(string)
   print(silhueta(string))

   poesia = 'chove chuva\nchove sem parar\nchove chuva\nchove sem parar\nhoje é vou fazer uma prece\npara deus, nosso senhor\npara chuvar parar\nde molhar o meu divino amor\nque é muito lindo\né mais que o infinito\né puro e belo\ninocente como uma flor\npor favor chuva ruin\nnão molhe mais o meu amor assim\npor favor chuva ruuuiinn\nnão molhe mais o meu amoor assim'
   print(poesia)
   print(silhueta(poesia))
...
