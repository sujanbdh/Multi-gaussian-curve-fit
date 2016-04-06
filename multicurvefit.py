import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import pandas as pd


#--------get data--------------------

data = pd.read_csv('metalpipe_FFT1.xl.csv', sep=",", header=None)
data=data.as_matrix()

def gaussian(x, height, center, width, offset):
    return height*np.exp(-(x - center)**2/(2*width**2)) + offset

def six_gaussians(x, h1, c1, w1, 
		h2, c2, w2, 
		h3, c3, w3,
		h4, c4, w4,
		h5, c5, w5,
		h6, c6, w6,
		offset):
    return (gaussian(x, h1, c1, w1, offset=0) +
        gaussian(x, h2, c2, w2, offset=0) +
        gaussian(x, h3, c3, w3, offset=0) + 
        gaussian(x, h4, c4, w4, offset=0) + 
        gaussian(x, h5, c5, w5, offset=0) + 
        gaussian(x, h6, c6, w6, offset=0) + 
        offset)

errfunc6 = lambda p, x, y: (six_gaussians(x, *p) - y)**2

guess6= [.22, 360, 65, 
	.22, 834, 65, 
	.39, 1164, 140,
	.59, 1550, 200,
	.3, 1990, 200,
	.3, 2350, 75, 0]
optim6, success = optimize.leastsq(errfunc6, guess6[:], args=(data[:,0], data[:,2]))
print
print "Fundamental frequency:  ampl ={0:5.1f}, freq ={1:5.1f} Hz, sigma ={2:5.2f} Hz".format(optim6[0],optim6[1],optim6[2]/2)
print "First harmonic:  ampl ={0:5.1f}, freq ={1:5.1f} Hz, sigma ={2:5.2f} Hz".format(optim6[3],optim6[4],optim6[5]/2)
print "Second harmonic:  ampl ={0:5.1f}, freq ={1:5.1f} Hz, sigma ={2:5.2f} Hz".format(optim6[6],optim6[7],optim6[8]/2)
print "Third harmonic:  ampl ={0:5.1f}, freq ={1:5.1f} Hz, sigma ={2:5.2f} Hz".format(optim6[9],optim6[10],optim6[11]/2)
print "Fourth harmonic:  ampl ={0:5.1f}, freq ={1:5.1f} Hz, sigma ={2:5.2f} Hz".format(optim6[12],optim6[13],optim6[14]/2)
print "Fifth harmonic:  ampl ={0:5.1f}, freq ={1:5.1f} Hz, sigma ={2:5.2f} Hz".format(optim6[15],optim6[16],optim6[17]/2)



plt.scatter(data[:,0], data[:,2], c='pink', label='measurement', marker='.', edgecolors=None)
plt.plot(data[:,0], six_gaussians(data[:,0], *optim6),
    c='b', label='fit of 6 Gaussians')
plt.title("FFT of white noise hitting an open metal tube")
plt.ylabel("Amplitude")
plt.xlabel("Frequency (Hz)")
plt.legend(loc='upper left')
plt.savefig('result.png')
