from dataprocess import mathutil
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ntpath
import os

DPI = 80
RPM = 2000   # rad/min
POWER = 6000 # watt

def lineChart(filename, times, torques, dpi):
    plt.figure('1.'+filename, figsize=(16,10), dpi=dpi)
    plt.ylabel("Amplitude", fontsize=16)
    plt.xlabel("Time [s]")
    plt.plot(times, torques, label='torque', color='r', linewidth=0.8)
    plt.legend()

def amplitudeSpectrum(filename, times, torques, dpi):

    # Compute FFT
    Fv, P1 = mathutil.getOneSidedFFT(times, torques)

    # Plot
    plt.figure('2.'+filename, figsize=(16,10), dpi=dpi)
    ax = plt.gca()
    ymax = max(P1[1:]) # Find max harmonic amplitude (exclude dc)
    ax.set(xlim=(0, 250)) # ylim=(ymax + 0.05)
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency [Hz]")
    plt.plot(Fv, P1)

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
            colnames = ['time', 'speed', 'torque_ref']
            df = pd.read_csv(datafile, names=colnames)
            df = df.apply(pd.to_numeric)

            # Convert pandas datacolumns to numpy arrays
            times = df['time'].to_numpy()     # [s]
            speeds = df['speed'].to_numpy()   # [rpm]
            torque_refs = df['torque_ref'].to_numpy() # [%]

            T_nom = mathutil.getNominalTorque(POWER, RPM)
            torque_refs = mathutil.percentToBaseUnit(torque_refs, T_nom)

            # Plot the data
            lineChart(filename, times, speeds, DPI)
            #amplitudeSpectrum(filename, times, speeds, DPI)
            #plt.savefig(filename + ".svg")
    
    plt.show() # Block

if __name__ == '__main__':
    main()
    