# importando 'lib' especifica a testar.
from biblioteca import Tela, Ponto

# primeira tela, sem borda vísivel e
# contendo grade.
t = Tela(1000,1000,True)
t.risca(5, 20,5 ,horizontal=False)

t.circula(Ponto(5, 40), Ponto(10, 60))
t.circula(Ponto(0, 0), Ponto(3, 15))
t.circula(
   Ponto(t.linhas-5, t.colunas-10),
   Ponto(t.linhas, t.colunas)
)
# imprimindo...
print(t)


t = Tela(10_000, 1_000,borda=True, grade=False)

t.circula(Ponto(8, 20), Ponto(12,55))
# imprimindo...
print(t)

t.risca(3, 10, 20, simbolo='X')

A = Ponto((26-3)-7, 0)
B = Ponto(26-3, 15)
t.circula(A, B)
# imprimindo modificação...
print(t)

t.risca(3, 10, 20, horizontal=False)
A = Ponto(0, t.colunas-5)
B = Ponto(8, t.colunas)
t.circula(A, B)
# imprimindo modificação...
print(t)


# testando circunscrição em todos lados e cantos.
t = Tela(1_000, 1_000, borda=True, grade=False)
compr = 7
(P, Q) = Ponto(0, 0), Ponto(compr, compr)
t.circula(P, Q)

(P, Q) = Ponto(t.linhas-compr, 0), Ponto(t.linhas, compr)
t.circula(P, Q)

(P, Q) = (
   Ponto(0, t.colunas-compr),
   Ponto(compr, t.colunas)
)
t.circula(P, Q)

(P, Q) = (
   Ponto(t.linhas-compr, t.colunas-compr),
   Ponto(t.linhas, t.colunas)
)
t.circula(P, Q)

(P, Q) = (
   Ponto(0, int(t.colunas/2)-compr),
   Ponto(compr, int(t.colunas/2))
)
t.circula(P, Q)

(P, Q) = (
   Ponto(t.linhas-compr, int(t.colunas/2)-compr),
   Ponto(t.linhas, int(t.colunas/2))
)
t.circula(P, Q)

(P, Q) = Ponto(compr+3, 0), Ponto(2*compr, 17)
t.circula(P, Q)

(P, Q) = (
   Ponto(int(t.linhas/2), t.colunas-17),
   Ponto(int(t.linhas/2)+compr, t.colunas)
)
t.circula(P, Q)

# imprimindo...
print(t)
