from dataprocess import mathutil
from dataprocess import datautil
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import sys
import matplotlib.ticker as ticker

RPM = 3100   # rad/min
POWER = 160000 # watt

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="Csv-data file path", required=True)
    parser.add_argument("--dpi", type=int, default=80, help="figure resolution")
    parser.add_argument("--save", type=int, help="save figure")
    parser.add_argument("--speed", "-rpm", type=int, default=None, help="Speed [rpm]")
    parser.add_argument("--power", "-P", type=int, default=None, help="Power [Watts]")
    return parser.parse_args(args)

# Double y-axis (torque-speed plotter)
def lineChart(filename, times, speeds, torques, torquesf, dpi):
    fig, ax1 = plt.subplots(figsize=(16,10), dpi=dpi)

    color1 = 'royalblue'
    ax1.set_ylabel("Torque [Nm]", color=color1, fontsize=22, labelpad=26)
    ax1.set_xlabel("Time [s]", fontsize=20, labelpad=14)
    d1 = ax1.plot(times, torques, label='torque unfiltered', linewidth=0.8, color='lightblue', alpha=0.45)
    d2 = ax1.plot(times, torquesf, label='torque filtered', linewidth=1.0, color=color1, alpha=1.0)
    ax1.set(ylim=(110, 170))
    ax1.tick_params(axis='y', labelcolor='blue', labelsize=16)
    ax1.tick_params(axis='x', labelcolor='black', labelsize=16)

    color2 = 'indianred'
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel("Speed [rpm]", color=color2, fontsize=22, labelpad=26)  # we already handled the x-label with ax1
    ax2.set(ylim=(199.4, 200.6))
    d3 = ax2.plot(times, speeds, label='speed', linewidth=1.0, color=color2, alpha=1.0)
    ax2.tick_params(axis='y', labelcolor=color2, labelsize=16)
    tick_spacing = 0.2
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    fig.tight_layout()  # otherwise the right y-label is slightly clipped    

    ax2.spines['right'].set_color(color2)
    ax2.spines['left'].set_color(color1)
    ax2.spines['top'].set_color('silver')
    ax2.spines['bottom'].set_color('silver')

    # Create legend
    lns = d2+d1+d3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='lower center', ncol=3, fontsize=16)

def lineChart2(filename, times, signal, dpi):
    fig, ax = plt.subplots(figsize=(16,10), dpi=100)
    plt.ylabel("Speed [rpm]", fontsize=12)
    plt.xlabel("Time [s]",  fontsize=12)
    ax.set(xlim=(0, 30))
    plt.locator_params(axis='y', nbins=10)
    plt.plot(times, signal, linewidth=0.8, color='royalblue') #color='mediumblue'

def amplitudeSpectrum(filename, times, torques, dpi):

    # Compute FFT
    Fv, P1 = mathutil.getOneSidedFFT(times, torques)

    # Plot
    plt.figure(filename, figsize=(16,10), dpi=dpi)
    ax = plt.gca()
    ymax = max(P1[1:]) # Find max harmonic amplitude (exclude dc)
    ax.set(xlim=(0, 250), ylim=(0, ymax + 0.05))
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency [Hz]")
    plt.plot(Fv, P1)

def plot(args):

    with open(args.file, mode='r') as datafile:
        filename = datautil.getBaseName(args.file)
        # Load the data
        colnames = ['time', 'speed', 'torque', 'torquef']
        df = pd.read_csv(datafile, names=colnames)
        df = df.apply(pd.to_numeric)

        # Convert pandas datacolumns to numpy arrays
        times = df['time'].to_numpy()     # [s]
        speeds = df['speed'].to_numpy()   # [rpm]
        torques = df['torque'].to_numpy() # [%]
        torquesf = df['torquef'].to_numpy() # [%]

        # Plot the data
        lineChart(filename, times, speeds, torques, torquesf, args.dpi)
        #lineChart2(filename, times, speeds, args.dpi)
        #amplitudeSpectrum(filename, times, speeds,args.dpi)
        #plt.savefig(filename + ".svg")

        plt.show(block=True)
        if args.save:
            plt.savefig(filename + ".pdf")

def main(args):
    plot(args)

if __name__ == '__main__':
    args = parseArgs()
    main(args)