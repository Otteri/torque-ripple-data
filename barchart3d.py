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
BASE_PATH = "C:\\Code\\torque-ripple\\data-analysis\\simulation-data\\FEM\\cogging-different-operating-points\\filtered\\"
#BASE_PATH = "C:\\Code\\torque-ripple\\data-analysis\\simulation-data\\FEM\\flux-different-operating-points\\filtered\\"


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
    print("freqs:", frequencies)
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

print("time1:", time1[0])
torque1 = data1.torque.to_numpy()

# Compute FFT
f1, P1 = mathutil.getOneSidedFFT(time1, torque1)
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
        # print("f_Harm", f_harmonics)
        # idx_1  = mathutil.findNearestIdx(f[i], f_harmonics[0])
        # idx_2  = mathutil.findNearestIdx(f[i], f_harmonics[1])
        # idx_6  = mathutil.findNearestIdx(f[i], f_harmonics[2])
        # idx_12 = mathutil.findNearestIdx(f[i], f_harmonics[3])
        # idx_24 = mathutil.findNearestIdx(f[i], f_harmonics[4])

    #     harmonics_1.append(P[i][idx_1])
    #     harmonics_2.append(P[i][idx_2])
    #     harmonics_6.append(P[i][idx_6])
    #     harmonics_12.append(P[i][idx_12])
    #     harmonics_24.append(P[i][idx_24])
    # print("sixth harmonics:", harmonics_6)
    # 60rpm 
        #xpos.append(np.arange(1,25))



# for j in range(1, 25):
#     xpos.append(np.full((1, 5), j))
#     ypos.append([60,120,240,480,960])

xpos = np.tile(np.array(np.arange(1,25)),(1,5))
#ypos = np.tile(np.array(np.arange(1,25)),(5,1))

ypos = []
ypos.append(np.full((1, 24), 60))
ypos.append(np.full((1, 24), 120))
ypos.append(np.full((1, 24), 240))
ypos.append(np.full((1, 24), 480))
ypos.append(np.full((1, 24), 960))

xpos = np.array( xpos ).flatten()
ypos = np.array( ypos ).flatten()


print("len x,y", len(xpos), len(ypos))

#lineChart(f4, P4)
#plt.plot(f4, P4, linewidth=0.8, color='royalblue')

fig = plt.figure()
ax = fig.gca(projection = '3d')
#harmonics = np.array( [harmonics_1, harmonics_2, harmonics_6, harmonics_12, harmonics_24] )
harmonics = np.array( [harmonics] ).flatten()
#print("harmonics:", harmonics)
#xpos = [1,1,1,1,1, 2,2,2,2,2, 6,6,6,6,6, 12,12,12,12,12, 24,24,24,24,24]
print("xpos:", xpos, "len:", len(xpos))
#ypos = [60,60,60,60,60 ,120,120,120,120,120, 240,240,240,240,240, 480, 480, 480, 480, 480, 960, 960, 960, 960, 960 ]
#ypos = [60,120,240,480,960, 60,120,240,480,960, 60,120,240,480,960, 60,120,240,480,960,  60,120,240,480,960]

#print("ypos:", ypos, "len yy", len(ypos))
#ypos = [60,120,240,480,960 ,1000 ]
zpos = np.zeros(120)
#print("len zpo", len(zpos))
dx = 1.0 * np.ones(120)
dy = 50 * np.ones(120)
dz = harmonics

print("len x,y,z", len(xpos), len(ypos), len(zpos))
colors = cm.rainbow( [0.2 + (1-0.2)/(len(xpos)-1)*i for i in range(len(xpos))] )
color1 = [1.00000000e-01, 5.87785252e-01, 9.51056516e-01, 1.00000000e+00]
color2 = [4.09803922e-01, 9.89980213e-01, 7.55382735e-01, 1.00000000e+00]
color3 = [8.56862745e-01, 8.46958211e-01, 4.83911424e-01, 1.00000000e+00]
color4 = [1.00000000e+00, 5.87785252e-01, 3.09016994e-01, 1.00000000e+00]
color5 = [1.00000000e+00, 1.22464680e-16, 6.12323400e-17, 1.00000000e+00]
print("colors:", colors)



norm=plt.Normalize(0,5)
cmap = mpl.colors.LinearSegmentedColormap.from_list("", [color1, color2, color3, color4, color5])

p = ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors)
#plt.xticks(np.arange(0, 50, 1))
ticks  = np.arange(0, 200, 1)
plt.xticks(np.arange(0, 26, 6), ticks[::24])
plt.yticks([60, 240, 480, 960], ('60', '240', '480', '960'))
plt.yticks(fontsize=10)

cbaxes = fig.add_axes([0.1, 0.1, 0.03, 0.8])
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cbaxes, fraction=0.1, pad=0.2, label='Frequency')
cbar.set_ticks([])
cbaxes.yaxis.set_label_position('left')


print("dz:", dz)

ax.set_xlabel('Harmonic order no.')
ax.set_ylabel('Rpm', labelpad=10)
ax.set_zlabel('Amplitude [Nm]')


# Xi = [1, 2, 6, 12, 24]
# Yi = [60]
# Zi = np.zeros(1)

# dx = .25 * np.ones(5)
# dy = .25 * np.ones(1)
# dz = [P1[idx1], P1[idx1], P1[idx1], P1[idx1], P1[idx1]]

# ax.set_xlabel('Harmonic order no.')
# ax.set_ylabel('Rpm')
# ax.bar3d(Xi, Yi, Zi, dx, dy, dz, color = 'w')






# # Data generation
# alpha = np.linspace(1, 8, 5)
# t = np.linspace(0, 5, 16)
# T, A = np.meshgrid(t, alpha)
# data = np.exp(-T * (1. / A))

# # Plotting
# fig = plt.figure()
# ax = fig.gca(projection = '3d')

# Xi = T.flatten()
# Yi = A.flatten()
# Zi = np.zeros(data.size)

# dx = .25 * np.ones(data.size)
# dy = .25 * np.ones(data.size)
# dz = data.flatten()

# ax.set_xlabel('T')
# ax.set_ylabel('Alpha')
# ax.bar3d(Xi, Yi, Zi, dx, dy, dz, color = 'w')

plt.show()