from dataprocess import mathutil
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ntpath
import os

DPI = 80

def lineChart(filename, times, signal1, signal2, dpi):
    plt.figure('1.'+filename, figsize=(16,10), dpi=dpi)
    plt.ylabel("Angle")
    plt.xlabel("Time [s]")
    plt.plot(times, signal1, label='electrical angle', linewidth=1.25, color='red')
    plt.plot(times, signal2, label='discretized angle', linewidth=1.25, color='darkorange')
    plt.legend(loc='upper left')


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
            colnames = ['time', 'speed', 'torque_ref', 'theta_e', 'theta_disc']
            df = pd.read_csv(datafile, names=colnames)
            df = df.apply(pd.to_numeric)

            # Convert pandas datacolumns to numpy arrays
            times = df['time'].to_numpy()
            speeds = df['speed'].to_numpy()
            torque_refs = df['torque_ref'].to_numpy()
            signal1 = df['theta_e'].to_numpy()
            signal2 = df['theta_disc'].to_numpy()

            # Plot the data
            lineChart(filename, times, signal1, signal2, DPI)
            #plt.savefig(filename + ".svg")
    
    plt.show() # Block

if __name__ == '__main__':
    main()
    