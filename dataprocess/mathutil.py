import numpy as np
import math

# Functions that can be used in multiple files

# Give power (P) in watts
def getNominalTorque(P, rpm):
    return ((60*P) / (2*math.pi*rpm))

def percentToBaseUnit(percent_value, nominal_value):
    decimals = 0.01 * percent_value
    base_values = decimals * nominal_value
    return base_values

# Computes two sided FFT
def getFFT(times, values):
    T = times[1] - times[0]               # sampling interval 
    Fs = (1/T)                            # calculate frequency
    L = int(Fs * (times[-1] - times[0]))  # Signal length
    Y = np.fft.fft(values)
    P2 = np.array(abs(Y / L))
    f2 = Fs * np.arange(L) / L
    return (f2, P2)

# Computes one sided FFT
def getOneSidedFFT(times, values):
    f2, P2 = getFFT(times, values) # two sided spectrum
    L = times.size-1              # data vector length
    P1 = P2[0:round(L/2)]         # One sided is half the length
    P1[2:-1] = 2*P1[2:-1]         # Double the values
    f1 = f2[0:round(L/2)]
    return (f1, P1)

# Finds the best match value-index from the array
def find_nearest_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

# Returns interesting harmonics
def getHarmonicFrequencies(rpm, poles):
    fn = (poles / 2) * (rpm / 60) # fn: electrical
    return [1*fn, 2*fn, 6*fn, 12*fn, 24*fn]

def interpolate(start, end, steps):
    return np.linspace(start, end, steps)