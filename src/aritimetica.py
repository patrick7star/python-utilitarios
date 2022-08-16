'''
    Programa fatora um valor, verifica se um número
é primo, obtem os divisores dado um valor e etc. Voltado
para problemas básicos de aritmética.
'''
# *** *** *** funções *** *** ***

def divisores(n):
    '''
        Retorna uma sequência, contendo todos os divisores
    do número passado. Também contendo o um(1), e o
    próprio número(n).
    '''
    return tuple(d for d in range(1, n + 1) if n % d == 0)

def fatora(n):
    '''
        Função que retorna a fatoração de um número inteiro
    positivo qualquer passado. Ele será retornado da seguinte
    forma: Num dicionário, onde a chave é o primo e, o valor é
    a potência que ele estará elevado, tudo de acordo com
    o "Teorema Fundamental da Aritmética".
    '''
    fatores, N, i = {}, n, 2
    #dividi o valor até atingir um.
    while N > 1:
        #os números que o dividem, serão
        #divididos repetidas vezes até  que o
        #o quociente não seja mais divisível.
        if N % i == 0:
            try:
                #se é dividido, então tal número é
                #adicionado ao dicionário como chave,
                #a quantia de vezes que divide-se por
                #ele é armazenado no dicionário como
                #valor daquela chave.
                fatores[i] += 1
            except KeyError:
                fatores[i] = 0
                continue
            #divide pelo o sucessor válido.
            N = int(N / i)
        else: i += 1 #testa um possivel sucessor como divisor.
    #retorna o dicionário com os primos divisores e,
    #suas respectivas potências.
    return fatores

def qtdDivisores(n):
    '''
        Calcula a quantidade de divisores que
    um número passado tem.
    '''
    #Para fazer isso, usa-se da função que fatora o
    #número, já que, ela tem a expressão fatorada
    #do número em forma de dicionário, onde a
    #chave é o primo, e, o valor referente a ele
    #é a potência que o eleva.
    def reduz(funcao, lista):
        for e in lista[1:]: lista[0] = funcao(lista[0], e)
        return lista[0]
    return reduz((lambda a, b: a*b), [x + 1 for x in fatora(n).values()])

def ePrimo(n):
    '''
        Verifica se o inteiro positivo passado é, ou
    não é, um número primo. Se for retorna o valor
    lógico "verdadeiro", e "falso" caso contrário; o
    de não ser.
    '''
    #Bem com já há uma função que lista os divisores,
    #então apenas verificamos se há dois divisores(um e
    #o próprio número), que é a condição para ser um
    #primo.
    #return True if qtdDivisores(n) == 2 else False

    # agora o mesmo algoritímo que usado em C.
    for i in range(2, n):
      # se for divisível, então não pode ser primo.
      if n % i == 0: return False
    # se chegar até aqui, então é primo.
    return True

def mmc(a,b):
    '''
        Calcula o mmc de dois números interios. Sendo
    este o retorno da função.
    '''
    #evitar argumentos negativos.
    if a < 0 or b < 0:
        return mdc(-a, b) if a < 0 else mdc(a, -b)
    #ao invés de, procurar multiplos comuns, o algoritmo
    #usado aqui será um truque para achar o resultado.
    #dado a fatoração de tal.
    fa, fb = fatora(a), fatora(b)
    #todos primos comuns de ambos valores.
    primos = set(fa).union(set(fb))
    _mmc = 1
    #pecorrer tais primos.
    for primo in primos:
        #se houver em ambos, tal primo, buscar
        #pelo o maior.
        if (primo in fa) and (primo in fb):
            #caso a potência, de tal primo em a,
            #for maior que b, multiplica por ele;
            #caso contrário, o inverso.
            if fa[primo] > fb[primo]: _mmc *= (primo ** fa[primo])
            else: _mmc *= (primo ** fb[primo])
        else:
            #caso ambos não tenham o mesmo fator;
            #neste caso escolher o que existe, simples assim.
            if primo in fa: _mmc *= (primo ** fa[primo])
            else: _mmc *= (primo ** fb[primo])
    return _mmc

def mdc(a, b):
    #mudando posições, primeiro, por serem
    #equivalentes; segundo, evita de fazer
    #isso na codificação abaixo. Coloquemos
    #o 'a' como sempre maior que 'b'.
    if b > a: return mdc(b, a)
    #se algum for zero, então o maior
    #divisor será o não nulo. Já se,
    #forem iguais, o maior valor é
    #o retorno de qualquer um.
    if a == 0 or b == 0:
        return a if b == 0 else b
    elif a == b: return b
    else:
        #levando em consideração a diferença de digitos
        #entre ambos números. Aciona se houver quatro
        #ou mais algarismos de diferença.
        if abs(len(str(a)) - len(str(b))) >= 4:
            #antecessor do quociente mais perto que resulta
            #no valor atual.
            c = int(a / b) - 1
            return mdc(b,a-b*c)
        else:
            try:
                #usa desta propriedade, o "algoritmo
                #do restos", para achar o "mdc". Ele
                #usará da equivalência de "mdc's" até
                #achar um menor, ou seja fácil de calcular.
                #O uso da recursividade é utilizado aqui.
                return mdc(b, a - b)
            except RecursionError:
                #passou de 1000 vezes a recursão. É preciso
                #aumenta-lo um pouquinho cada vez que acontence.
                from sys import setrecursionlimit, getrecursionlimit
                #print('chega num limite de recursão.' + str(getrecursionlimit()))
                #aumentando o limite de recursão em 5% cada vez
                #que dá error.
                setrecursiononlimit = int(1.05*getrecursionlimit())
                #print('aumenta o atual limite de recursão.')
                #continua o cálculo.
                #print('continua o cálculo...')
                return mdc(a, b - a)

def eNumeroPerfeito(n):
    '''
        Verifica se um número é "perfeito" ou não.
    Caso seja retorna um booleano "true", e o "falso"
    caso contrário.
    '''
    if sum(sorted(divisores(n))[0:-1]) == n: return True
    return False

def geraNPrimos(n, comeca = 2):
    '''
        Função gera a quantia de primos passada aos
    parâmetros. Retorna um conjunto contendo todos
    os 'n' primos achados. Já o 'começa' é de onde
    começar a procurar tais primos, por padrão, ele
    está definido no 2, que apesar de ser primo, o
    valor passado no lugar dele não precisa ser.
    '''
    #ela já começa com os primos básicos, logo
    #não é preciso buscar-lôs
    primos, L = set([]), comeca
    #limite superior definido inicialmente como o dobro.
    S = L + n + 150
    #o algoritmo condiciona que não vai parar o
    #laço até que todos 'n' primos tenham sido
    #encontrados.
    while len(primos) < n:
        while L < S:
            #adiciona se primo.
            if ePrimo(L): primos.add(L)
            #se alcançar a quantia de primos antes
            #de o laço terminar, termina procedimento.
            if len(primos) == n: break
            L += 1
        #varrendo de cinquenta em cinquenta valores inteiros.
        S = L + (n + 50)
    else: return primos, (S-1)
    #caso tenha sido interrompido antes(por break statement).
    return primos, L

def relacaoBezot(a,b):
    '''
        Retorna as constantes que multiplicado aos
    termos 'a' e 'b', quando somados, retorna o "mdc"
    de tais números. Veja a relação abaixo:
            mdc(a,b) = m * a + n * b
    '''
    def expressao(a,b,m,n):
        if mdc(a, b) == a*m + b*n:
            return 'mdc({A},{B}) = ({M}*{A})+({N}*{B})'.format(A=a,M=m,N=n,B=b)
        return 'mdc({A},{B}) ≠ ({M}*{A})+({N}*{B})'.format(A=a,M=m,N=n,B=b)

    from random import randint

    m, n, L, _mdc = 1,2, 100, mdc(a,b)
    Jt = set([]) #já testado.

    while True:
        m,n = randint(0,L), randint(-L, 0)

        if ((m,n) in Jt or (-m,-n) in Jt or
            (n,m) in Jt or (-n,-m) in Jt): continue
        else:
            print(expressao(a = a, b = b, n = n, m = m))
            Jt.add((m,n))
            print(expressao(a = a, b = b, n = -n, m = -m))
            Jt.add((-m,-n))
            print(expressao(a = a, b = b, n = m, m = n))
            Jt.add((n, m))
            print(expressao(a = a, b = b, n = -m, m = -n))
            Jt.add((-n,-m))

            from legivel import tamanho
            print('qtd. de dados processados:%s'%tamanho(len(Jt), unidade='byte', acronomo=True))

        if m*a + n*b == _mdc: return (m,n)
        elif (-m)*a+(-n)*b == _mdc: return (-m,-n)
        elif n*a+m*b == _mdc: return (n,m)
        elif (-n)*a+(-m)*b == _mdc: return (-n,-m)

def buscaNumerosPerfeitos(a_partir=1, faixa = 1000):
    '''
        Faz uma busca entre, inicialmente, mil números,
    isso à partir de certo valor, que o padrão se nada
    colocado é um.
        O retorno é uma lista com valores achados, e o
    último valor verificado.
    '''
    nP,i=[],a_partir
    while i <= a_partir+faixa:
        if eNumeroPerfeito(i): nP.append(i)
        i += 1
    return (nP, i)

__all__ = [
   "ePrimo", "mmc", "mdc",
   "buscaNumerosPerfeitos",
   "eNumeroPerfeito",
   "geraNPrimos",
   "fatora"
]

# *** *** *** execução *** *** ***

if __name__ == '__main__':

    '''
    #gerando 19 primos, partindo da casa dos milhões.
    primos = geraNPrimos(comeca = 3923823, n = 19)
    print('lista de primos:',sorted(primos[0]))
    print('último valor verificado:',primos[1])
    print('quantidade de primos:', len(primos[0]))

    #mdc de números gigantes.
    num1, num2 = 3813391843012837120133,9340102000001
    print(len(str(num1)))
    print(len(str(num2)))
    print(len(str(num1))-len(str(num2)))
    print(mdc(num1,num2))
    '''
    print(buscaNumerosPerfeitos())
