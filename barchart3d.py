import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from dataprocess import mathutil
from dataprocess import datautil
import pandas as pd
from matplotlib import cm
import matplotlib as mpl
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

DPI = 150
BASE_PATH = ".\\simulation-data\\FEM\\cogging-various-speeds\\"


def lineChart(x, y):
    plt.figure(figsize=(16,10), dpi=DPI)
    plt.ylabel("y")
    plt.xlabel("x")
    plt.plot(x, y, linewidth=0.8, color='royalblue')

def getHarmonicFrequencies(rpm, poles):
    fn = (poles / 2) * (rpm / 60) # fn: electrical
    frequencies = []
    for i in range(1, 25):
        frequencies.append(i * fn)
    return frequencies

data1 = pd.read_csv(BASE_PATH + "60rpm.csv", skiprows=1, delimiter=';', names=['time', 'speed', 'torque'])
data2 = pd.read_csv(BASE_PATH + "120rpm.csv", skiprows=1, delimiter=';', names=['time', 'speed', 'torque'])
data3 = pd.read_csv(BASE_PATH + "240rpm.csv", skiprows=1, delimiter=';', names=['time', 'speed', 'torque'])
data4 = pd.read_csv(BASE_PATH + "480rpm.csv", skiprows=1, delimiter=';', names=['time', 'speed', 'torque'])
data5 = pd.read_csv(BASE_PATH + "960rpm.csv", skiprows=1, delimiter=';', names=['time', 'speed', 'torque'])

# Get time array in seconds
time1 = datautil.convertToSeconds(data1.time.to_numpy(), 'ms')
time2 = datautil.convertToSeconds(data2.time.to_numpy(), 'ms')
time3 = datautil.convertToSeconds(data3.time.to_numpy(), 'ms')
time4 = datautil.convertToSeconds(data4.time.to_numpy(), 'ms')
time5 = datautil.convertToSeconds(data5.time.to_numpy(), 'ms')

# Compute FFT
f1, P1 = mathutil.getOneSidedFFT(time1, data1.torque.to_numpy())
f2, P2 = mathutil.getOneSidedFFT(time2, data2.torque.to_numpy())
f3, P3 = mathutil.getOneSidedFFT(time3, data3.torque.to_numpy())
f4, P4 = mathutil.getOneSidedFFT(time4, data4.torque.to_numpy())
f5, P5 = mathutil.getOneSidedFFT(time5, data5.torque.to_numpy())

# Combine, so we can stop copy-pasting already
f = [f1, f2, f3, f4, f5]
P = [P1, P2, P3, P4, P5]
rpms = [60, 120, 240, 480, 960]

harmonics_1 = []
harmonics_2 = []
harmonics_6 = []
harmonics_12 = []
harmonics_24 = []

harmonics = []
xpos = []
ypos = []
for i in range(len(rpms)):
    f_harmonics = getHarmonicFrequencies(rpms[i], 24)
    for j in range(0, 24):
        harmonic_idx = mathutil.findNearestIdx(f[i], f_harmonics[j])
        harmonics.append(P[i][harmonic_idx])

xpos = np.tile(np.array(np.arange(1,25)),(1,5))


ypos = []
ypos.append(np.full((1, 24), 60))
ypos.append(np.full((1, 24), 120))
ypos.append(np.full((1, 24), 240))
ypos.append(np.full((1, 24), 480))
ypos.append(np.full((1, 24), 960))

xpos = np.array( xpos ).flatten()
ypos = np.array( ypos ).flatten()

fig = plt.figure()
ax = fig.gca(projection = '3d')
harmonics = np.array( [harmonics] ).flatten()

zpos = np.zeros(120)
dx = 1.0 * np.ones(120)
dy = 50 * np.ones(120)
dz = harmonics

colors = cm.rainbow( [0.2 + (1-0.2)/(len(xpos)-1)*i for i in range(len(xpos))] )
color1 = [1.00000000e-01, 5.87785252e-01, 9.51056516e-01, 1.00000000e+00]
color2 = [4.09803922e-01, 9.89980213e-01, 7.55382735e-01, 1.00000000e+00]
color3 = [8.56862745e-01, 8.46958211e-01, 4.83911424e-01, 1.00000000e+00]
color4 = [1.00000000e+00, 5.87785252e-01, 3.09016994e-01, 1.00000000e+00]
color5 = [1.00000000e+00, 1.22464680e-16, 6.12323400e-17, 1.00000000e+00]

norm=plt.Normalize(0,5)
cmap = mpl.colors.LinearSegmentedColormap.from_list("", [color1, color2, color3, color4, color5])

p = ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)
ticks  = np.arange(0, 500, 1)
plt.xticks(np.arange(0, 26, 6), ticks[::72])
plt.yticks([60, 240, 480, 960], ('60', '240', '480', '960'))
plt.yticks(fontsize=10)

cbaxes = fig.add_axes([0.13, 0.12, 0.03, 0.72]) # colorbar pos
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbaxes, fraction=0.1, pad=0.2, label='Frequency')
cbar.set_ticks([])
cbaxes.yaxis.set_label_position('left')

ax.set_xlabel('Harmonic order no.')
ax.set_ylabel('Rpm', labelpad=10)
ax.set_zlabel('Amplitude [Nm]')

plt.show()
