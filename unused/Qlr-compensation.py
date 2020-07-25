from dataprocess import mathutil
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ntpath
import os
from linechart2 import lineChart2

DPI = 80

color2 = '#e15129'
color1 = '#0896d3'

def lineChart(filename, times, signal1, signal2, dpi):
    plt.figure('1.'+filename, figsize=(16,10), dpi=dpi)
    plt.ylabel("Angle")
    plt.xlabel("Time [s]")
    plt.plot(times, signal1, label='Speed', linewidth=1.25, color='red')
    plt.plot(times, signal2, label='Torque', linewidth=1.25, color='darkorange')
    plt.legend(loc='upper left')

def amplitudeSpectrum(filename, times, torques, dpi):

    # Compute FFT
    Fv, P1 = mathutil.getOneSidedFFT(times, torques)

    # Plot
    plt.figure('2.'+filename, figsize=(16,10), dpi=dpi)
    plt.rc('grid', linestyle='dotted', color='silver')
    plt.grid(True)
    ax = plt.gca()
    ymax = max(P1[:]) # Find max harmonic amplitude (exclude dc)
    ax.set(xlim=(-0.5, 250), ylim=(0, ymax + 0.05))
    plt.ylabel("Torque amplitude [Nm]", fontsize=14)
    plt.xlabel("Harmonic order no.", fontsize=14)
    plt.plot(Fv, P1, color=color1)

    print("p1 len", len(P1))

    labels =  ['0', '6', '12', '18', '24', '30', '36', '42', '48', '54', '60']
    plt.xticks(np.arange(0, 250, step=24), labels, fontsize=12)  # Set labels

def main():

    directory_path = input("Give full path to the directory:\n")
    os.chdir(directory_path)
    print("Files from '{}' will be processed.\n".format(os.getcwd()))

    # Go through all csv-files in the directory
    for datapath in glob('*.csv'):
        with open(datapath, mode='r') as datafile:
            filename = ntpath.basename(datapath)
            print("Plotting '{}'".format(filename))

            # Load the data
            colnames = ['time', 'speed', 'compensation', 'torque', 'torque_ref']
            df = pd.read_csv(datafile, names=colnames)
            df = df.apply(pd.to_numeric)

            # Convert pandas datacolumns to numpy arrays
            times = df['time'].to_numpy()
            speeds = df['speed'].to_numpy()
            compensation = df['compensation'].to_numpy()
            torques = df['torque'].to_numpy()
            signal2 = df['torque_ref'].to_numpy()

            # Plot the data
            lineChart(filename, times, speeds, torques, DPI)
            #lineChart2(times, speeds, torques, signal1_ylabel='Speed [rpm]', signal2_ylabel='Torque [Nm]')
            amplitudeSpectrum(filename, times, torques, DPI)
            #plt.savefig(filename + ".svg")


    plt.show() # Block

if __name__ == '__main__':
    main()
    