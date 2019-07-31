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

#Uniform Quantization

for n in [1,2,3,4,5,6,7,8]:
    R = V/(2**n)        # Resolution
    quant = [];
    err = [];
    for i in list:
        for x in i:
            b = int((x+1)/R)    # Determining the level of the current sample
            xq = -1 + b*R       # Quantized sample
            eq = (x - xq)**2
            quant.append(xq) 
            err.append(eq)      # Store the quadratic error
    err_med = sum(err)/len(err) # Mean square error
    figure()
    plot(quant)
    uniform_err.append(err_med) # Store the values of the mean square error for each n
    uniform.append(quant)       # Store the quantized signal for each n

#A-Law quantization

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
    R = V/(2**n)               
    quant = [];
    err = [];
    for x in compressed:
            b = int((x+1)/R)    
            xq = -1 + b*R       
            quant.append(xq)
            err.append(eq)      
    err_med = sum(err)/len(err) 
    figure()
    plot(quant)
    leiA.append(quant)
    compressed_err.append(err_med)

# Printando erros
print ("Values of the mean square error")
for i in [0,1,2,3,4,5,6,7]:
    print ("Bits per sample: ", i+1)
    print ("Uniform quantization: e =", uniform_err[i], "V\nA-Law Quantization: e =", compressed_err[i], "V")
    print ("----------------------------")

# Reproduzindo audios
print ("Playing audios")
for i in [0,1,2,3,4,5,6,7]:
    print ("Bits per sample: ", i+1)
    print ("Uniform quantization...")
    sd.play(uniform[i], 8000)
    time.sleep(4)
    print ("A-Law quantization...")
    sd.play(leiA[i], 8000)
    time.sleep(4)
    print ("--------------------")

show()

# Figures 1 to 8 are for linear quantization and figures 9 to 16 corresponds to A-Law quantization
