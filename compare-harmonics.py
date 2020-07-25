from dataprocess import mathutil
import matplotlib.patches as mpatches
from matplotlib import gridspec
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import argparse
import sys
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from os import remove, walk, getcwd
from dataprocess import mathutil

color1 = '#0896d3'
#color2 = None #'#69c386'
#color3 = '#e15129'

#BASE_PATH = ".\\experimental-data\\speeds"
BASE_PATH = ".\\experimental-data\\torques"

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_speed", type=int, default=None, help="Speed [rpm]", required=True)
    parser.add_argument("--poles", "-Np", type=int, help="Total number of poles", required=True)
    parser.add_argument("--dpi", type=int, default=200, help="figure resolution")
    parser.add_argument("--save", type=int, help="save figure")
    parser.add_argument("--is_ilc", type=int, help="show ilc in legend if ilc", required=True)
    parser.add_argument("--is_torque", type=int, help="torque harmonics", required=True)
    args = parser.parse_args(args)
    return args

def getInterestingHarmonics(time, y, speed_nom, poles):
    Fv, P1 = mathutil.getOneSidedFFT(time, y)
    frequencies = mathutil.getHarmonicFrequencies(speed_nom, poles)

    # Harmonic may not be exactly at calculated location, so
    # Search for the max from neighborhood.
    indices = []
    for harmonic in frequencies:
        idx1 = mathutil.findNearestIdx(Fv, harmonic)
        idx2 = np.argmax(P1[idx1-5:idx1+5])
        indices.append(idx1 + (idx2-5))
    
    x = (Fv[indices[0]], Fv[indices[1]], Fv[indices[2]], Fv[indices[3]])
    y = (P1[indices[0]], P1[indices[1]], P1[indices[2]], P1[indices[3]])

    print("Harmonic frequencies: ", [ '%.3f' % elem for elem in frequencies ])
    print("Matched frequencies:  ", [ '%.3f' % elem for elem in x ])
    return x, y


def doubleBarChart(ax, y1, y2, args):
    if args.is_ilc:
        color2 = '#69c386'
        label = 'ILC'
    else:
        color2 = '#e15129'
        label = 'Q-learning'


    harmonics_num = 4
    index = np.arange(harmonics_num)
    bar_width = 0.30

    ax.bar(index, y1, width=bar_width,
    color=color1,
    label='PI') 

    ax.bar(index + bar_width, y2, width=bar_width,
    color=color2,
    label=label)

    ax.set_xticks(index + bar_width/2.0)
    ax.set_xticklabels(('1st', '2nd', '6th', '12th'))


def plot(t1, y1, t2, y2, args):
    fig = plt.figure(constrained_layout=True, figsize=(11,5), dpi=args.dpi)
    gs = fig.add_gridspec(1, 4)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[0, 3])
    time_titles = ["0%-load", "10%-load", "50%-load", "80%-load"]
    axes = [ax1, ax2, ax3, ax4]

    on_harmonics = []
    off_harmonics = []
    
    # Compute the locations and the harmonics itself
    for i in range(0, len(y1)):
        _, off = getInterestingHarmonics(t1[i], y1[i], args.run_speed, args.poles)
        _, on = getInterestingHarmonics(t2[i], y2[i], args.run_speed, args.poles)
        off_harmonics.append(off)
        on_harmonics.append(on)
        doubleBarChart(axes[i], off_harmonics[i], on_harmonics[i], args)


    minor_locator1 = AutoMinorLocator(5)
    minor_locator2 = AutoMinorLocator(5)
    for ax in axes:
        ax.set_ylim(0, 2.7)
        ax.grid('y', which='major')
        ax.set_axisbelow(True)
        ax.grid(linestyle=':', color='lightgrey', axis='y', which='minor')
        ax.grid(linestyle='--', color='lightgrey', axis='y', which='major')
        ax.xaxis.grid() # vertical lines
        ax.set_xlabel('Harmonic order no.')
        ax.legend(ncol=1, loc='upper right')
        ax.yaxis.set_minor_locator(minor_locator1)
        ax.yaxis.set_major_locator(MultipleLocator(0.5))

        if args.is_torque:
            ax.set_ylabel('Torque amplitude (%)')
        else:
            ax.set_ylabel('Speed amplitude [rpm]')


    for i in range(len(axes)):
        axes[i].set_title(time_titles[i])
        # Special treatment
        #if(i == 3):
        #    axes[3].yaxis.set_minor_locator(minor_locator2)
        #    axes[3].set_ylim(0, 6.3)
        #else:
        axes[i].yaxis.set_minor_locator(minor_locator1)
        axes[i].set_ylim(0, 2.0)            
        #if args.is_torque:


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
            time_data = df['time'].to_numpy()   # [s]
            speed_data = df['speed'].to_numpy()  # [rpm]
            
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