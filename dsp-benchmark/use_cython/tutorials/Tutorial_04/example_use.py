#%%
from matplotlib import pyplot as plt
import numpy as np
from collections import namedtuple

from scipy.signal import firwin, fftconvolve, lfilter, kaiserord
import demodulation

#%%
# Create a signal and a window
pi = np.pi 
 
sample_rate = 400.0
nsamples = 5001
N = 401
t = np.arange(nsamples) / sample_rate
 
Harmonic = namedtuple('Harmonic', ['frequency', 'amplitude', 'phase'])
harmonics = [Harmonic(1, 0.5, 0), 
             Harmonic(0.4, 2.5, pi/2 + 0.1),
             Harmonic(0.2, 15.3, pi/2),
             Harmonic(0.1, 23.45, pi/2 + 0.8)]
 
signal = np.zeros((N, nsamples))
for ampl, freq, phase in harmonics:
    ampl = ampl*np.ones(t.shape)
    ampl = np.tile(ampl, (N,1)) + np.outer(0.2*np.random.randint(2, size=(N,)), ampl)
 
    phase = phase*np.ones(t.shape)
    phase = np.tile(phase, (N,1)) + np.outer(0.5*np.random.randint(2, size=(N,)), phase)
 
    x = ampl * np.cos(2*pi*freq*t + phase)
    signal += np.random.normal(0, 0.8*ampl, (N, nsamples)) + x
 
f = 2.5
yI = np.cos(2*pi*f*t)
yQ = np.sin(2*pi*f*t)
 
nyq_rate = sample_rate / 2.0
width = 5.0/nyq_rate
 
ripple_db = 40.0
ntaps, beta = kaiserord(ripple_db, width)
cutoff_hz = 10.0
taps = firwin(ntaps, cutoff_hz/nyq_rate, window=('kaiser', beta))

# %%
Q = demodulation.pure_c_mt(signal, t, taps, 2.5)

# %%
%timeit demodulation.pure_c_mt(signal, t, taps, 2.5)
# %%
