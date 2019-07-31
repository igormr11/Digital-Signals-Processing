from scipy.io import loadmat
from pylab import *
import numpy as np
import sounddevice as sd
import time
import math

arq = loadmat('sinal.mat')
sinal = arq['Sinal']
list = sinal.tolist() # Lista de listas

V = 2
A = 87.6
uniform = []
compressed = []
leiA = []
uniform_err = []
compressed_err = []

#Quantização Uniforme

for n in [1,2,3,4,5,6,7,8]:
    R = V/(2**n)        # Resolução
    quant = [];
    err = [];
    for i in list:
        for x in i:
            b = int((x+1)/R)    # Determinação do nível
            xq = -1 + b*R       # Sinal quantizado
            eq = (x - xq)**2
            quant.append(xq)    # Guarda as amostras do sinal quantizado
            err.append(eq)      # Guarda o erro quadrático
    err_med = sum(err)/len(err) # Cálcula o erro médio quadrático
    figure()
    plot(quant)
    uniform_err.append(err_med) # Guarda os valores do erro medio para cada n
    uniform.append(quant)       # Guarda os valores quantizados para cada n

#Quantização LeiA

for i in list:
    for x in i:
        if x >= 0:
            sgn = 1
        else:
            sgn = -1
        x = abs(x)
        if x < (1/A):
            c = sgn*A*x/(1 + log(A))
        if  1/A <= x <= 1:
            c = sgn*(1+log(A*x))/(1+log(A))
        compressed.append(c)

for n in [1,2,3,4,5,6,7,8]:
    R = V/(2**n)                # Resolução
    quant = [];
    err = [];
    for x in compressed:
            b = int((x+1)/R)    # Determinação do nível
            xq = -1 + b*R       # Sinal quantizado
            quant.append(xq)
            err.append(eq)      # Guarda o erro quadrático
    err_med = sum(err)/len(err) # Cálcula o erro médio quadrático
    figure()
    plot(quant)
    leiA.append(quant)
    compressed_err.append(err_med)

# Printando erros
print ("Valores de erro médio quadrático:")
for i in [0,1,2,3,4,5,6,7]:
    print ("Número de bits igual a ", i+1)
    print ("Quantização Uniforme: e =", uniform_err[i], "V\nQuantização Lei A: e =", compressed_err[i], "V")
    print ("----------------------------")

# Reproduzindo audios
print ("Reproduzindo áudios")
for i in [0,1,2,3,4,5,6,7]:
    print ("Número de bits igual a", i+1)
    print ("Quantização Uniforme...")
    sd.play(uniform[i], 8000)
    time.sleep(4)
    print ("Quantização Lei A...")
    sd.play(leiA[i], 8000)
    time.sleep(4)
    print ("--------------------")

show()

# Figuras de 1 a 8 correspondem à quantização linear e figuras de 9 a 16 correspondem à quantização não linear
# O valor de erro médio quadrático é muito menor para a quantização não linear, principalmente para um número de bits menor que 7
# A inteligibilidade do áudio aumenta com o número de bits, a mensagem pode ser compreendida a partir de n = 5.
