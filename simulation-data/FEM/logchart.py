import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the data
colnames = ['time', 'torque']
df1 = pd.read_csv('FEM-cogging.csv', names=colnames)
df2 = pd.read_csv('FEM-flux.csv', names=colnames)

# Convert pandas datacolumns to numpy arrays
times1 = df1['time'].to_numpy()
torques1 = df1['torque'].to_numpy()
times2 = df2['time'].to_numpy()
torques2 = df2['torque'].to_numpy()

Y = torques2
X2, Y2 = [], []
for i in range(0, 99, 2):
    Y2.append(Y[i])
    X2.append(i)


fig, ax = plt.subplots(figsize=(16,10), dpi=150)
plt.yscale('log')
plt.margins(.01, .025)
plt.grid(True, which="both", axis="y")
ax.set_axisbelow(True)
ax.vlines(x=X2, ymin=0, ymax=Y2, color='mediumblue', alpha=1.0, linewidth=6)
ax.scatter(x=X2, y=Y2, s=60, color='mediumblue', alpha=1.0)
ax.set_ylabel('Torque amplitude [Nm]', fontsize=20, labelpad=30)
ax.set_xlabel('Harmonic order no.', fontsize=20, labelpad=30)

# labels and ticks
ax.set_xticks(np.arange(0, 99, step=4))
labels = np.arange(0, 299, step=2)
ax.set_xticklabels(labels)
ax.set_xticks(X2[1::2], minor=True)
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=4)
ax.tick_params(labelsize=16)

plt.show()