
"""
importa todos módulos atualmente importante
para aqui, então serão exportados. Os códigos
dados como "mortos", pois foram criados
otimizações, ou descontinuados não serão
exportados novamente. Muitos destes módulos
reescritos com otimizações, ganharão o nome
original, e como já dito, exportado.
"""

import barra_de_progresso
import espiral
import legivel
import romanos
import silhueta
# sendo renomeada com a versão otimizada,
# pelo menos até o momento.
import tela_i as tela
import arvore_ii as arvore
import numeros_por_extenso
import testes

# não usado muito, então dado como
# descontinuado.
#import aritmetica

# re-exportando ...
__all__ = [
   "arvore",
   "barra_de_progresso",
   "espiral",
   "legivel",
   "romanos",
   "silhueta",
   "tela"
]
