from dataprocess import mathutil
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ntpath
import os
from matplotlib.ticker import FormatStrFormatter

DPI = 80
RPM = 2000   # rad/min
POWER = 6000 # watt

color2 = 'indianred'
color1 = 'royalblue'

def simulationPlot(filename, times, torques, dpi, label, color):
    #torques = torques * 28.6
    plt.ylabel("Amplitude [p.u.]", fontsize=16)
    plt.xlabel("Time [s]", fontsize=16)
    plt.plot(times, torques, label=label, color=color, linewidth=0.8)
    #plt.legend(loc='upper right', prop={'size': 14})
    plt.xlim((500, 501))

def main():

    directory_path = input("Give full path to the directory:\n")
    os.chdir(directory_path)
    print("Files from '{}' will be processed.\n".format(os.getcwd()))

    #fig, ax1 = plt.subplots(figsize=(16,10), dpi=80)
    axs = []
    fig, axes = plt.subplots(3) #sharey=True
    for ax1 in axes:
        ax1.set(xlim=(500, 501))
        ax2 = ax1.twinx()
        ax1.set(ylim=(-2, 2))
        ax2.set(ylim=(57, 63))
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        ax1.set_xticklabels(['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'])
        ax1.tick_params(axis='x', labelsize=14)
        axs.append(ax1)
        axs.append(ax2)
    
    axs[2].set_ylabel("Torque [Nm]", color=color1, fontsize=16, labelpad=8)
    axs[3].set_ylabel("Speed [rpm]", color=color2, fontsize=16, labelpad=8)
    axs[4].set_xlabel("Time [s]", fontsize=16, labelpad=12)
    idx = 0

    axs[0].set_title("PI", fontsize=16)
    axs[3].set_title("ILC", fontsize=16)
    axs[4].set_title("Q-learning", fontsize=16)

    plt.subplots_adjust(left=0.125,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.5)

    # Go through all csv-files in the directory
    for datapath in glob('*.csv'):
        with open(datapath, mode='r') as datafile:
            filename = ntpath.basename(datapath)
            print("Plotting '{}'".format(filename))

            # Load the data
            colnames = ['time', 'speed', 'torque_ref']
            df = pd.read_csv(datafile, names=colnames)
            df = df.apply(pd.to_numeric)

            # Convert pandas datacolumns to numpy arrays
            times = df['time'].to_numpy()     # [s]
            speeds = df['speed'].to_numpy()   # [rpm]
            
            ax = axs[idx]
            if 'torque' in filename:
                speeds = speeds * 28.6
                ax.tick_params(axis='y', labelcolor=color1, labelsize=14)
                ax.plot(times, speeds, color=color1, linewidth=0.8, alpha=0.9)
                idx = idx + 1

            if 'speed' in filename:
                speeds = speeds * 2000.0
                ax.plot(times, speeds, color=color2, linewidth=1.0)
                ax.tick_params(axis='y', labelcolor=color2, labelsize=14)
                idx = idx + 1
                
    plt.show() # Block

if __name__ == '__main__':
    main()
    