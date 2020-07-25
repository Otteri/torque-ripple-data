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
    T = float(times[1] - times[0])        # sampling interval 
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
    #print("Zero component:", P1[0])
    return (f1, P1)

# Finds the best match value-index from the array
def findNearestIdx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

# Returns interesting harmonics
def getHarmonicFrequencies(rpm, poles):
    fn = (poles / 2) * (rpm / 60) # fn: electrical
    return [1*fn, 2*fn, 6*fn, 12*fn]

# Returns interesting harmonics
def getSignificantHarmonicFrequencies(rpm, poles):
    #fn = (poles / 2) * (rpm / 60) # fn: electrical
    fn = (rpm / 60.0)
    orders = [0, 1, 2]
    harmonics = [0, 1*fn, 2*fn]
    for i in range(3, 999, 1):
        harmonics.append(i*fn)
        orders.append(i)
    return harmonics, orders

def interpolate(start, end, steps):
    return np.linspace(start, end, steps)

# Returns data corresponding to one mechanical period (one revolution)
# The data is taken at the end of the list as this is likely
# to be better than data in the beginning of the list.
def getDataPeriod(rpm, time, data):
    fn = rpm / 60.0
    print("fn:", fn)
    T = 1.0 / fn
    idx = 0
    while (time[idx] - time[0]) < T:
        idx = idx + 1
    return data[-idx:] # take the last list items

# pass data from single rotation
def calculateRipple(data):
    ripple = np.max(data) - np.min(data)
    return ripple

# data1 / data2
def calculateRippleRatio(data1, data2):
    r1 = calculateRipple(data1)
    r2 = calculateRipple(data2)
    return r1 / r2

# peak-to-peak / nominal value
def calculateRippleFactor(data, nominal_value):
    ripple = calculateRipple(data)
    return (float(ripple) / float(nominal_value)) * 100.0
