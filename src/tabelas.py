
"""
 Implementando a formação de Tabelas para
 minha 'biblioteca padrão' Python.
"""

class Coluna():
   def __init__(self, rotulo, array):
      self._rol = array
      self._nome = rotulo
   ...
   
   def rol_iter(self):
      "itera todos dados do rol"
      for dado in self._rol:
         yield dado
   ...
   
   def nome(self):
      "encapsulamento, retorna o rótulo da coluna"
      return self._nome
   
   def __len__(self):
      "quantia de dados no rol"
      return len(self._rol)
...

# separador inicial das células e rótulos.
BARRA = '#'
# vácuo de espaço comum para debug.
ESPACO = ' '


def equilibra_str(string, comprimento):
   str_comprimento = len(string)
   if str_comprimento % 2 != 0:
      consertada = string + ESPACO
      return equilibra_str(consertada, comprimento)
      
   if len(string) <= comprimento:
      diferenca = abs(len(string) - comprimento)
      while len(string) < comprimento:
         string = (
            "{espaco}{}{espaco}"
            .format(string, espaco=ESPACO)
         )
      ...
   ...
   return string
...

def cria_tabela(coluna1, coluna2):
   linhas = []
   maior_qtd = max(len(coluna1), len(coluna2))
   
   i1 = coluna1.rol_iter()
   i2 = coluna2.rol_iter()
   
   rotulo1 = coluna1.nome()
   rotulo1 = equilibra_str(rotulo1, len(rotulo1))
   rotulo2 = coluna2.nome()
   rotulo2 = equilibra_str(rotulo2, len(rotulo2))
   linhas.append(
      "{barra}{0}{barra}{1}{barra}"
      .format(
         rotulo2, 
         rotulo1, 
         barra=BARRA
      )
   )
   
   # computando o valor com mais dígitos do rols, ou
   # o rótulo com mais letras.
   mc1 = max(len(str(v)) for v in coluna1.rol_iter())
   mc2 = max(len(str(v)) for v in coluna2.rol_iter())
   mc1 = max(len(rotulo1), mc1)
   mc2 = max(len(rotulo2), mc2)
   
   while maior_qtd != 0:
      linha = BARRA
      try:
         celula = str(next(i2))
         linha += equilibra_str(celula, mc2) + BARRA
      except StopIteration:
         linha += '-' * mc2 + BARRA
      ...
      try:
         celula = str(next(i1))
         linha += equilibra_str(celula, mc1) + BARRA
      except StopIteration:
         linha += '-' * mc1 + BARRA
      ...
      linhas.append(linha)
      maior_qtd -= 1
      del linha
   ...
   tabela = "\n".join(linhas)
   # criando barras superior e inferior.'
   return tabela
...

def tampa_tabela(tabela_str):
   "cria barras superiores e inferiores para ela"
   linhas = tabela_str.split('\n')
   comprimento = len(linhas[0])
   barra = BARRA * comprimento
   # adiciona barra superior.
   linhas.insert(0, barra)
   # adicionando barra inferior.
   linhas.append(barra)
   return "\n".join(linhas)
...

# testes unitários:
if __name__ == "__main__":
   from testes import executa_teste
   
   # dados comuns:
   coluna1 = Coluna("gênero", ['M', 'F', 'F', 'F', 'M'])
   coluna2 = Coluna("idade", [14, 27, 38, 13, 51, 24])
   
   def testa_funcao_cria_tabela():
      tabela = cria_tabela(coluna1, coluna2)
      print(tabela, end='\n\n')

   def testa_tampa_tabela():
      tabela = cria_tabela(coluna1, coluna2)
      print(tampa_tabela(tabela))
   
   executa_teste(testa_funcao_cria_tabela)
   executa_teste(testa_tampa_tabela)
...