from dataprocess import mathutil
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ntpath
import os
import argparse
import sys
import matplotlib.patches as mpatches
from matplotlib.ticker import AutoMinorLocator

DPI = 80

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dpi", type=int, default=200, help="figure resolution")
    parser.add_argument("--save", type=int, help="save figure")
    parser.add_argument("--file1", "-f1", type=str, help="Csv-data file 1", required=True)
    args = parser.parse_args(args)
    return args

def lineChart(filename, times, torques, dpi):
    plt.figure('1.'+filename, figsize=(16,10), dpi=dpi)
    plt.ylabel("Amplitude")
    plt.xlabel("Time [s]")
    plt.plot(times, torques, label='torque', linewidth=0.8)
    plt.legend()

def amplitudeSpectrum(filename, times, torques, dpi):

    # Compute FFT
    Fv, P1 = mathutil.getOneSidedFFT(times, torques)

    # Plot
    plt.figure('2.'+filename, figsize=(16,10), dpi=dpi)
    plt.yscale('log')
    #plt.ylim([0.1,10**3])
    ax = plt.gca()
    ymax = max(P1[1:]) # Find max harmonic amplitude (exclude dc)
    #ax.set(ylim=(ymax)) # ymax + 0.05 xlim=(0, 250)
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency [Hz]")
    plt.plot(Fv, P1)

def getGreater(v1, v2):
    if v1 >= v2:
        return v1
    return v2

def plot(ax, times, torques, compensations):
    #plt.xlim([0,100])
    ax.set_xlim([-0.5,100])
    ax.set_ylim([-0.002, 0.35])
    Fv, P1 = mathutil.getOneSidedFFT(times, torques)
    Fv, P3 = mathutil.getOneSidedFFT(times, compensations)
    #plt.plot(Fv, P2, label='Pulsating torque', linewidth=0.8, color='darkorange')
    ax.plot(Fv, P3, label='Compensation torque', linewidth=1.0, color='green', alpha=0.5)
    ax.plot(Fv, P1, label='Actual torque', linewidth=1.0, color='red', alpha=0.8)
    ax.legend()

    #ax.text(0, 0.01, s='0th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    #ax.text(4, getGreater(P1[idx1], P3[idx1]), s='1st', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    #ax.text(8, getGreater(P1[idx2], P3[idx2]), s='2nd', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    #ax.text(24, getGreater(P1[idx3], P3[idx3]), s='6th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    #ax.text(48, getGreater(P1[idx4], P3[idx4]), s='12th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)

    ax.tick_params(labelsize=16)
    ax.set_ylabel('Torque amplitude [Nm]', fontsize=16)
    ax.set_xlabel('Harmonic order no.', fontsize=16)
    #plt.savefig(filename + ".svg")
    ax.grid(True)


    pos = np.arange(0, 200, step=1)
    labels = np.arange(0, 200, step=1)

    ax.set_xticks(pos[0::24])
    ax.set_xticklabels(labels[0::6])
    minor_locatorx = AutoMinorLocator(6)
    minor_locatory = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locatorx)
    ax.yaxis.set_minor_locator(minor_locatory)


def main():

    args = parseArgs()
    args.file1

    plt.rc('grid', linestyle='dotted', color='silver')
    fig, ax1 = plt.subplots(figsize=(6,5), dpi=200)

    # Go through all csv-files in the directory
    data1 = np.load(args.file1) #.tolist()
    times1, speeds1, torques1, compensations1, pulsations1 = data1 #torquesf1
    torques1 = torques1 * 28.6 # pu. to rpm
    speeds1 = speeds1 * 2000
    compensations1 = compensations1 * 28.6

    plot(ax1, times1, torques1, compensations1)

    #ax1.set_title('Enabled', fontsize=16)
    plt.show(block=False)

    plt.show() # Block

if __name__ == '__main__':
    main()
