from dataprocess import mathutil
import matplotlib.patches as mpatches
from matplotlib import gridspec
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import argparse
import sys
from matplotlib.ticker import AutoMinorLocator


color1 = '#0896d3'
color2 = '#69c386'
color3 = '#e15129'

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_speed", type=int, default=None, help="Speed [rpm]", required=True)
    parser.add_argument("--poles", "-Np", type=int, help="Total number of poles", required=True)
    parser.add_argument("--dpi", type=int, default=150, help="figure resolution")
    parser.add_argument("--save", type=int, help="save figure")
    parser.add_argument("--file1", "-f1", type=str, help="Csv-data file 1", required=True)
    parser.add_argument("--file2", "-f2", type=str, help="Csv-data file 2", required=True)
    parser.add_argument("--file3", "-f3", type=str, help="Csv-data file 3", required=True)
    parser.add_argument("--file4", "-f4", type=str, help="Csv-data file 4", default=None)
    parser.add_argument("--file5", "-f5", type=str, help="Csv-data file 5", default=None)
    parser.add_argument("--file6", "-f6", type=str, help="Csv-data file 6", default=None)
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
    color=color1,
    label='PI') 

    ax.bar(index + bar_width, y2, width=bar_width, align='center',
    color=color2,
    label='PI-ILC')

    ax.bar(index + 2 * bar_width, y3, width=bar_width, align='center',
    color=color3,
    label='PI-Qlr')

    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(('1st', '2nd', '6th', '12th', '24th'))


def plot(t1, t2, t3, y1, y2, y3, args):
    fig = plt.figure(constrained_layout=True, figsize=(11,5), dpi=args.dpi)
    gs = fig.add_gridspec(3, 3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[:, 1:])
    time_axes = [ax1, ax2, ax3]
    time_titles = ['PI', 'PI-ILC', 'PI-Qlr']

    for i in range(len(time_axes)):
        time_axes[i].set_title(time_titles[i])
        time_axes[i].set_xlim(0, 10)
        time_axes[i].set_ylim(50, 70)

    # Labels
    ax2.set_ylabel('Speed [rpm]')
    ax3.set_xlabel('Time [s]')
    ax4.set_title('Harmonics')
    ax4.set_ylabel('Speed amplitude [rpm]')
    ax4.set_xlabel('Harmonic order no.')

    # Time plots
    ax1.plot(t1, y1, linewidth=0.8, color=color1)
    ax2.plot(t2, y2, linewidth=0.8, color=color2)
    ax3.plot(t3, y3, linewidth=0.8, color=color3)

    # Compute the locations and the harmonics itself
    _, y1 = getInterestingHarmonics(t1, y1, args.run_speed, args.poles)
    _, y2 = getInterestingHarmonics(t2, y2, args.run_speed, args.poles)
    _, y3 = getInterestingHarmonics(t3, y3, args.run_speed, args.poles)

    # Plot the harmonics
    tripleBarChart(ax4, y1, y2, y3)

    if args.save:
        plt.savefig("figure.svg", bbox_inches='tight', pad_inches=0)

def plot2(t1, t2, t3, t4, t5, t6, y1, y2, y3, y4, y5, y6, args):
    fig = plt.figure(constrained_layout=True, figsize=(11,5), dpi=args.dpi)
    gs = fig.add_gridspec(10, 3)
    ax0 = fig.add_subplot(gs[0:1, 0])
    ax1 = fig.add_subplot(gs[1:4, 0])
    ax2 = fig.add_subplot(gs[4:7, 0])
    ax3 = fig.add_subplot(gs[7:10, 0])
    ax4 = fig.add_subplot(gs[:10, 1])
    ax5 = fig.add_subplot(gs[:10, 2])
    data_axes = [ax1, ax2, ax3, ax4, ax5]

    ax0.axis('off') # only for common legend
    time_axes = [ax1, ax2, ax3]
    fig.set_constrained_layout_pads(wspace=0.05)

    # Labels
    ax2.set_ylabel('Speed [rpm]')
    ax3.set_xlabel('Time [s]')
    ax4.set_xlabel('Harmonic order no.')
    ax5.set_xlabel('Harmonic order no.')
    ax4.set_ylabel('Speed amplitude [rpm]')
    ax5.set_ylabel('Torque amplitude [Nm]')

    # Manual legend
    pi = mpatches.Patch(color=color1, label='PI')
    pi_ilc = mpatches.Patch(color=color2, label='PI-ILC')
    pi_qlr = mpatches.Patch(color=color3, label='PI-Qlr')
    ax0.legend(handles=[pi, pi_ilc, pi_qlr], ncol=3, loc='upper left', fancybox=True)

    # Time plots for speed
    ax1.plot(t1, y1, linewidth=0.5, color=color1)
    ax2.plot(t2, y2, linewidth=0.5, color=color2)
    ax3.plot(t3, y3, linewidth=0.5, color=color3)

    # Compute the locations and the harmonics itself
    _, y1 = getInterestingHarmonics(t1, y1, args.run_speed, args.poles)
    _, y2 = getInterestingHarmonics(t2, y2, args.run_speed, args.poles)
    _, y3 = getInterestingHarmonics(t3, y3, args.run_speed, args.poles)
    _, y4 = getInterestingHarmonics(t4, y4, args.run_speed, args.poles)
    _, y5 = getInterestingHarmonics(t5, y5, args.run_speed, args.poles)
    _, y6 = getInterestingHarmonics(t6, y6, args.run_speed, args.poles)

    # Plot the harmonics
    tripleBarChart(ax4, y1, y2, y3)
    tripleBarChart(ax5, y4, y5, y6)
    
    # Create grid lines
    for ax in data_axes:
        ax.grid('y', which='major')
        ax.set_axisbelow(True)
        ax.grid(linestyle=':', color='silver', axis='y', which='minor')
        ax.grid(linestyle='--', color='silver', axis='y', which='major')
        ax.xaxis.grid() # vertical lines

    for ax in time_axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(50, 70)
        ax.set_yticks([55, 65], minor=True)
        ax.grid(linestyle='dotted', color='silver', axis='both', which='minor')
        ax.grid(linestyle='dotted', color='silver', axis='both', which='major')

        # Ticks
        minor_locator1 = AutoMinorLocator(5)
        minor_locator2 = AutoMinorLocator(5)
        ax4.yaxis.set_minor_locator(minor_locator1)
        ax5.yaxis.set_minor_locator(minor_locator2)

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

    # Read also torque data if provided
    if args.file4 != None:
        df4 = pd.read_csv(args.file4, names=colnames)
        df5 = pd.read_csv(args.file5, names=colnames)
        df6 = pd.read_csv(args.file6, names=colnames)

        t4 = df4['time'].to_numpy()
        y4 = df4['signal'].to_numpy()
        t5 = df5['time'].to_numpy()
        y5 = df5['signal'].to_numpy()
        t6 = df6['time'].to_numpy()
        y6 = df6['signal'].to_numpy()

        plot2(t1, t2, t3, t4, t5, t6, y1, y2, y3, y4, y5, y6, args)
    else:
        plot(t1, t2, t3, y1, y2, y3, args)

    if args.save:
        plt.savefig("comparison.pdf", bbox_inches='tight', pad_inches=0)

    plt.show(block=True)

if __name__ == '__main__':
    main()