from dataprocess import mathutil
from matplotlib import gridspec
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import argparse
import sys

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--speed", type=int, default=None, help="Speed [rpm]",required=True)
    parser.add_argument("--poles", "-Np", type=int, help="Number of poles")
    parser.add_argument("--pole_pairs", "-p", type=int, help="Number of pole pairs")
    parser.add_argument("--dpi", type=int, default=150, help="figure resolution")
    parser.add_argument("--save", type=int, help="save figure")
    parser.add_argument("--file1", "-f1", type=str, help="Csv-data file 1", required=True)
    parser.add_argument("--file2", "-f2", type=str, help="Csv-data file 2", required=True)
    parser.add_argument("--file3", "-f3", type=str, help="Csv-data file 3", required=True)

    args = parser.parse_args(args)
    if not (args.poles or args.pole_pairs):
        raise parser.error('Either poles or pole_pairs must be provided')

    return args

def getInterestingHarmonics(time, y, speed_nom, pole_pairs):
    Fv, P1 = mathutil.getOneSidedFFT(time, y)
    frequencies = mathutil.getHarmonicFrequencies(speed_nom, pole_pairs)

    # Harmonic may not be exactly at calculated location, so
    # Search for the max from neighborhood.
    indices = []
    for harmonic in frequencies:
        idx1 = mathutil.findNearestIdx(Fv, harmonic)
        idx2 = np.argmax(P1[idx1-5:idx1+5])
        indices.append(idx1 + (idx2-5))

    x = (Fv[indices[0]], Fv[indices[1]], Fv[indices[2]], Fv[indices[3]], Fv[indices[4]])
    y = (P1[indices[0]], P1[indices[1]], P1[indices[2]], P1[indices[3]], P1[indices[4]])

    print("Harmonic frequencies: ", [ '%.3f' % elem for elem in frequencies ])
    print("Matched frequencies:  ", [ '%.3f' % elem for elem in x ])
    return x, y

def tripleBarChart(ax, y1, y2, y3):
    harmonics_num = 5
    index = np.arange(harmonics_num)
    bar_width = 0.20

    ax.bar(index, y1, width=bar_width, align='center',
    color='r',
    label='PI') 

    ax.bar(index + bar_width, y2, width=bar_width, align='center',
    color='b',
    label='PI-ILC')

    ax.bar(index + 2 * bar_width, y3, width=bar_width, align='center',
    color='g',
    label='PI-Qlr')

    plt.xlabel('Harmonic order no.')
    #plt.ylabel('Amplitude [pu.]')
    plt.xticks(index + bar_width, ('1st', '2nd', '6th', '12th', '24th'))
    plt.legend()

def plot(t1, t2, t3, y1, y2, y3, args):
    fig = plt.figure(constrained_layout=True, figsize=(11,5), dpi=args.dpi)
    gs = fig.add_gridspec(3, 3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[:, 1:])
    
    # Texts around the plots
    ax1.set_title('PI')
    ax2.set_title('PI-ILC')
    ax3.set_title('PI-Qlr')
    ax4.set_title('Harmonics')
    ax2.set_ylabel('Amplitude [pu.]')
    ax3.set_xlabel('Time [s]')

    # Time plots
    ax1.plot(t1, y1, linewidth=0.8, color='red')
    ax2.plot(t2, y2, linewidth=0.8, color='blue')
    ax3.plot(t3, y3, linewidth=0.8, color='green')

    # Compute the locations and the harmonics itself
    _, y1 = getInterestingHarmonics(t1, y1, args.speed, args.pole_pairs)
    _, y2 = getInterestingHarmonics(t2, y2, args.speed, args.pole_pairs)
    _, y3 = getInterestingHarmonics(t3, y3, args.speed, args.pole_pairs)

    # Plot the harmonics
    tripleBarChart(ax4, y1, y2, y3)

    if args.save:
        plt.savefig("figure.svg", bbox_inches='tight', pad_inches=0)

def main():

    args = parseArgs()

    # Load the data
    colnames = ['time', 'signal']
    df1 = pd.read_csv(args.file1, names=colnames)
    df2 = pd.read_csv(args.file2, names=colnames)
    df3 = pd.read_csv(args.file3, names=colnames)

    # Convert pandas datacolumns to numpy arrays
    t1 = df1['time'].to_numpy()   # [s]
    y1 = df1['signal'].to_numpy() # SI / pu.
    t2 = df2['time'].to_numpy()
    y2 = df2['signal'].to_numpy()
    t3 = df3['time'].to_numpy()
    y3 = df3['signal'].to_numpy()

    plot(t1, t2, t3, y1, y2, y3, args)
    plt.show(block=True)

if __name__ == '__main__':
    main()