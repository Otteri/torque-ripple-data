import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataprocess import mathutil
from dataprocess import datautil
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

# Load the data
BASE_PATH = ".\\simulation-data\\FEM\\"
data1 = pd.read_csv(BASE_PATH + "FEM-current-measurement-error.csv", skiprows=1, delimiter=';', names=['time', 'speed', 'torque'])

# Get time array in seconds
time1 = datautil.convertToSeconds(data1.time.to_numpy(), 'ms')

# Compute FFT
f, P = mathutil.getOneSidedFFT(time1, data1.torque.to_numpy())

harmonic_frquencies, orders = mathutil.getSignificantHarmonicFrequencies(3100, 6) # nominal op.

indices = []
N = 2
f2 = []
P2 = []
for freq in harmonic_frquencies:
    idx = mathutil.findNearestIdx(f, freq)
    f2.append(freq)
    P2.append(P[idx])
    indices.append(idx)

f2 = f2[::3] # plot integer harmonics only
P2 = P2[::3] # -> resolution 155 hz with 160-kW motor

fig, ax = plt.subplots(figsize=(16,10), dpi=80) # 150
plt.yscale('log')
plt.margins(.01, .025)
plt.grid(True, which="both", axis="y")
ax.set_axisbelow(True)
ax.vlines(x=f2, ymin=0, ymax=P2, color='mediumblue', alpha=1.0, linewidth=6)
ax.scatter(x=f2, y=P2, s=60, color='mediumblue', alpha=1.0)
ax.set_ylabel('Torque amplitude [Nm]', fontsize=20, labelpad=30)
ax.set_xlabel('Harmonic order no.', fontsize=20, labelpad=10)
plt.ylim([1.0, 10**3])
plt.xlim([-100, 7550]) # 7550

# labels and ticks
ax.set_xticks(np.arange(0, 7550, step=930))
labels = np.arange(0, 156, step=6)
ax.set_xticklabels(labels)
ax.set_xticks(P[1::2], minor=True)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=4)
ax.tick_params(labelsize=16)

minor_locator1 = AutoMinorLocator(6)
ax.xaxis.set_minor_locator(minor_locator1)


#ax.xaxis.set_ma_formatter(FormatStrFormatter('%d'))

plt.show()