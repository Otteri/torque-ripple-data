from dataprocess import mathutil
import matplotlib.patches as mpatches
from matplotlib import gridspec
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import argparse
import sys
from matplotlib.ticker import AutoMinorLocator
from os import remove, walk, getcwd

color1 = '#0896d3'
color2 = '#69c386'
color3 = '#e15129'

BASE_PATH = ".\\experimental-data\\speeds"

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dpi", type=int, default=200, help="figure resolution")
    parser.add_argument("--save", type=int, help="save figure")
    parser.add_argument("--is_ilc", type=int, help="show ilc in legend if ilc")
    args = parser.parse_args(args)
    return args


def plot(t1, y1, t2, y2, args):
    fig = plt.figure(constrained_layout=True, figsize=(11,5), dpi=args.dpi)
    gs = fig.add_gridspec(2, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    time_titles = ["0%-load", "10%-load", "50%-load", "80%-load"]
    time_axes = [ax1, ax2, ax3, ax4]

    for i in range(len(time_axes)):
        time_axes[i].set_title(time_titles[i])
        time_axes[i].set_xlim(0, 5)
        time_axes[i].set_ylim(50, 70)
        time_axes[i].set_ylabel('Speed [rpm]')
        time_axes[i].set_xlabel('Time [s]')

    print("len:", len(t1))
    # Time plots
    ax1.plot(t1[0], y1[0], linewidth=0.8, color=color1, label='PI')
    ax2.plot(t1[1], y1[1], linewidth=0.8, color=color1, label='PI')
    ax3.plot(t1[2], y1[2], linewidth=0.8, color=color1, label='PI')
    ax4.plot(t1[3], y1[3], linewidth=0.8, color=color1, label='PI')
    
    if args.is_ilc:
        ax1.plot(t2[0], y2[0], linewidth=0.8, color=color2, label='ILC')
        ax2.plot(t2[1], y2[1], linewidth=0.8, color=color2, label='ILC')
        ax3.plot(t2[2], y2[2], linewidth=0.8, color=color2, label='ILC')
        ax4.plot(t2[3], y2[3], linewidth=0.8, color=color2, label='ILC')
    else:
        ax1.plot(t2[0], y2[0], linewidth=0.8, color=color3, label='Q-learning')
        ax2.plot(t2[1], y2[1], linewidth=0.8, color=color3, label='Q-learning')
        ax3.plot(t2[2], y2[2], linewidth=0.8, color=color3, label='Q-learning')
        ax4.plot(t2[3], y2[3], linewidth=0.8, color=color3, label='Q-learning')

    minor_locator1 = AutoMinorLocator(2)
    for ax in time_axes:
        ax.set_xlim(0, 2)
        ax.set_ylim(50, 70)
        ax.set_yticks([55, 65], minor=True)
        ax.grid(linestyle='dotted', color='lightgrey', axis='both', which='major')
        ax.yaxis.set_minor_locator(minor_locator1)
        ax.legend(ncol=2, loc='lower right')

    if args.save:
        plt.savefig("figure.svg", bbox_inches='tight', pad_inches=0)


def main():

    args = parseArgs()

    compensator_times = []
    compensator_speeds = []
    default_times = []
    default_speeds = []

    (_, _, files) = next(walk(BASE_PATH))
    files = [BASE_PATH + '\\' + file for file in files]
    print("Files from '{}' will be processed.\n".format(getcwd()))

    for file in files:
        with open(file, mode='r') as datafile:

            # Load the data
            colnames = ['time', 'speed']
            df = pd.read_csv(datafile, names=colnames)
            df = df.apply(pd.to_numeric)

            # Convert pandas datacolumns to numpy arrays
            time_data = df['time'].to_numpy()  # [s]
            speed_data = df['speed'].to_numpy()#[1000::]  # [rpm]
            
            if "-on" in file.lower():
                compensator_times.append(time_data)
                compensator_speeds.append(speed_data)
            elif "-off" in file.lower():
                print("file:", file, "len", len(time_data))
                default_times.append(time_data)
                default_speeds.append(speed_data)
            else:
                print(file, "cannot be plotted")

    plot(default_times, default_speeds, compensator_times, compensator_speeds, args)

    plt.show(block=True)

if __name__ == '__main__':
    main()