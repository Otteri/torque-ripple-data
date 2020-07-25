import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import ntpath
from glob import glob
from matplotlib.ticker import AutoMinorLocator

DPI = 100

def fluxHarmonics(X, Y):

    fig, ax = plt.subplots(figsize=(16,10), dpi=DPI)
    ax.vlines(x=X, ymin=0, ymax=Y, color='mediumblue', alpha=0.7, linewidth=6)
    ax.scatter(x=X, y=Y, s=80, color='mediumblue', alpha=0.8)
    plt.tick_params(labelsize=16)
    ax.set_ylabel('Amplitude [Nm]', fontsize=20)
    ax.set_xlabel('Frequency [Hz]', fontsize=20)

    # Flux harmonics
    ax.set(xlim=(810, 5000), ylim=(-0.5, 25))
    ax.text(0, Y[0]+0.1, s='0th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    ax.text(930, Y[12]+0.6, s='6th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    ax.text(1860, Y[24]+0.6, s='12th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    ax.text(2790, Y[36]+0.6, s='18th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    ax.text(3720, Y[48]+0.6, s='24th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    ax.text(4650, Y[60]+0.6, s='30th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)

def coggingHarmonics(X, Y):
    fig, ax = plt.subplots(figsize=(16,10), dpi=DPI)
    ax.vlines(x=X, ymin=0, ymax=Y, color='mediumblue', alpha=0.7, linewidth=6)
    ax.scatter(x=X, y=Y, s=80, color='mediumblue', alpha=0.8)
    ax.set_ylabel('Amplitude [Nm]', fontsize=20)
    ax.set_xlabel('Frequency [Hz]', fontsize=20)

    # Cogging harmonics
    plt.tick_params(labelsize=16)
    ax.set(xlim=(-150, 8000), ylim=(-0.14, 6))

    ax.text(0, Y[0]+0.1, s='0th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    ax.text(3720, Y[24]+0.1, s='24th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)
    ax.text(7440, Y[48]+0.1, s='48th', horizontalalignment='center', verticalalignment='bottom', fontsize=16)

# Plot harmonic order on x-axle and amplitude on y-axle.
def coggingHarmonicOrders(X, Y):
    X2, Y2 = [], []
    dots = 50
    for i in range(0, dots, 1):
        Y2.append(Y[i])
        X2.append(i)

    fig, ax = plt.subplots(figsize=(16,10), dpi=DPI)
    plt.rc('grid', linestyle='dotted', color='silver')
    plt.grid(True)
    ax.set_axisbelow(True)
    ax.set(xlim=(-1, dots), ylim=(-0.07, 5.0))
    ax.vlines(x=X2, ymin=0, ymax=Y2, color='mediumblue', alpha=1.0, linewidth=6)
    ax.scatter(x=X2, y=Y2, s=80, color='mediumblue', alpha=1.0)
    ax.set_ylabel('Torque amplitude [Nm]', fontsize=20, labelpad=30)
    ax.set_xlabel('Harmonic order no.', fontsize=20, labelpad=6)

    labels = np.arange(0, 600, step=1)
    plt.xticks(X2[0::4], labels[0::12])
    minor_locatorx = AutoMinorLocator(2)
    minor_locatory = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locatorx)
    ax.yaxis.set_minor_locator(minor_locatory)

    ax.tick_params(which='major', length=6)
    ax.tick_params(which='minor', length=4)
    ax.tick_params(labelsize=16)

def currentMeasErrorHarmonics(X, Y):

    X2, Y2 = [], []
    dots = 50
    for i in range(0, dots, 1):
        Y2.append(Y[i])
        X2.append(i)

    fig, ax = plt.subplots(figsize=(16,10), dpi=DPI)
    plt.rc('grid', linestyle='dotted', color='silver')
    plt.grid(True)
    ax.set_axisbelow(True)
    #ax.set(xlim=(-1, dots), ylim=(-0.07, 5.0))
    ax.vlines(x=X2, ymin=0, ymax=Y2, color='mediumblue', alpha=1.0, linewidth=6)
    ax.scatter(x=X2, y=Y2, s=80, color='mediumblue', alpha=1.0)
    ax.set_ylabel('Torque amplitude [Nm]', fontsize=20, labelpad=30)
    ax.set_xlabel('Harmonic order no.', fontsize=20, labelpad=6)

    labels = np.arange(0, 600, step=1)
    plt.xticks(X2[0::4], labels[0::12])
    minor_locatorx = AutoMinorLocator(2)
    minor_locatory = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locatorx)
    ax.yaxis.set_minor_locator(minor_locatory)

    ax.tick_params(which='major', length=6)
    ax.tick_params(which='minor', length=4)
    ax.tick_params(labelsize=16)


def main():
    # Fundamental frequency of the motor
    fn = 155

    # Load the data
    colnames = ['time', 'torque']
    df1 = pd.read_csv('FEM-cogging.csv', names=colnames)
    #df2 = pd.read_csv('FEM-flux.csv', names=colnames)

    # Convert pandas datacolumns to numpy arrays
    times1 = df1['time'].to_numpy()
    torques1 = df1['torque'].to_numpy()
    #times2 = df2['time'].to_numpy()
    #torques2 = df2['torque'].to_numpy()

    # Plot the harmonics
    coggingHarmonics(times1, torques1)
    coggingHarmonicOrders(times1, torques1)
    #currentMeasErrorHarmonics(times1, torques1)
    plt.savefig("cogging-harmonics.pdf")

    #fluxHarmonics(times2, torques2)
    plt.savefig("flux-harmonics.pdf")


    plt.show() # Block

if __name__ == '__main__':
    main()
    