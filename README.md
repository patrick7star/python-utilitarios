# Utilitários em Python 

<h4> versões:&nbsp   
<a href="https://github.com/TheAlgorithms/">
    <img src="https://img.shields.io/pypi/pyversions/tomlkit.svg?logo=python&logoColor=white" height="15">
</a>
</h4>

É uma biblioteca com funções básicas em Python que escrevi há muito tempo, pórem são reutilizados, bastante, em vários dos meus códigos.
Entre tudo está:
    . Conversões de números no sistema decimal posicional e números romanos.
    
    . Gerador de árvores dado o diretório raíz, onde ramifica subdiretórios
      ou arquivos(este pode ser opcional) de maneira visual.
    
    . Gerador de barra de progresso, que leva tanto quantidade unitários
      como dados em questão, com parâmetros para personalização.
    
    . Uma tela-de-impressão que permite impressão posicionada, e também 
      possibilita a emolduração de determinado conjunto de textos, ótimo
      para programar jogos em "ncurses", só precisaria imprimir-lá.
      
    . Não totltamente terminado, porém a conversão de números decimais 
      em texto por extensos.
     
    . Um código para gerar uma espiral-efeito, poode ser aplicado em 
      matriz ou na própria tela de impressão.
     
    . Gerador de silhueta, pege qualquer arquivo de texto, e ele faz 
      sua sombra levando em conta os espaços e quebra de linhas, retornando
      uma bela impressão sobre o seu texto.
     
    . Um arquivo com funções básicas de aritmética, como gerar **n** primos,
     ou se um número é primo, computa divisores e etc.

    . Também têm um módulo que cuida de escrever letras, palavras, frases
     ou textos passados como argumento num *texto-desenhado*.


## Exemplos:

### módulo *tela*:
```python
tela = Tela(15, 20, grade=True)
tela.risca(Ponto(5, 6), simbolo='+')
```

### módulo *barra_de_progresso*:
```python
tota = 50_329
progresso = ProgressoTemporal(total)
for valor in range(1, total + 1):
    print(progresso(valor))
```
