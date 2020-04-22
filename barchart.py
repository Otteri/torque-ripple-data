import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datautil
import argparse
import sys

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--speed", type=int, default=None, help="Speed [rpm]",required=True)
    parser.add_argument("--poles", "-Np", type=int, help="Number of poles")
    parser.add_argument("--pole_pairs", "-p", type=int, help="Number of pole pairs")
    parser.add_argument("--file1", "-f1", type=str, help="Csv-data file 1", required=True)
    parser.add_argument("--file2", "-f2", type=str, help="Csv-data file 2", required=True)
    parser.add_argument("--file3", "-f3", type=str, help="Csv-data file 3", required=True)

    args = parser.parse_args(args)
    if not (args.poles or args.pole_pairs):
        raise parser.error('Either poles or pole_pairs must be provided')

    return args


def fft(filename, args):
    # Load the data
    colnames = ['time', 'speed', 'torque_ref']
    df = pd.read_csv(filename, names=colnames)

    # Convert pandas datacolumns to numpy arrays
    times = df['time'].to_numpy()     # [s]
    speeds = df['speed'].to_numpy()   # [rpm]
    torque_refs = df['torque_ref'].to_numpy() # [%]

    #T_nom = getNominalTorque(P, rpm)
    #torque_refs = percentToBaseUnit(torque_refs, T_nom)
    Fv, P1 = datautil.getOneSidedFFT(times, speeds)
    frequencies = datautil.getHarmonicFrequencies(args.speed, args.poles)

    # Harmonic may not be exactly at calculated location, so
    # Search for the max from neighborhood.
    indices = []
    for harmonic in frequencies:
        idx1 = datautil.find_nearest_idx(Fv, harmonic)
        idx2 = np.argmax(P1[idx1-5:idx1+5])
        indices.append(idx1 + (idx2-5))

    x = (Fv[indices[0]], Fv[indices[1]], Fv[indices[2]], Fv[indices[3]], Fv[indices[4]])
    y = (P1[indices[0]], P1[indices[1]], P1[indices[2]], P1[indices[3]], P1[indices[4]])

    print("Harmonic frequencies: ", [ '%.3f' % elem for elem in frequencies ])
    print("Matched frequencies:  ", [ '%.3f' % elem for elem in x ])
    return x, y

def main(args, y1, y2, y3):
    # data to plot
    n_groups = 5

    # create plot
    fig, ax = plt.subplots()
    fig.canvas.set_window_title('Harmonics')
    index = np.arange(n_groups)
    bar_width = 0.25

    rects1 = plt.bar(index, y1, bar_width,
    color='b',
    label='data 1') # PI

    rects2 = plt.bar(index + bar_width, y2, bar_width,
    color='g',
    label='data 2') # PI-ILC

    rects3 = plt.bar(index + 2 * bar_width, y3, bar_width,
    color='r',
    label='data 3') # PI-Qlrn

    plt.xlabel('Harmonic [no.]')
    plt.ylabel('Amplitude [pu.]')
    plt.xticks(index + bar_width, ('1st', '2nd', '6th', '12th', '24th'))
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    args = parseArgs()
    _, y1 = fft(args.file1, args)
    _, y2 = fft(args.file2, args)
    _, y3 = fft(args.file3, args)
    main(args, y1, y2, y3)
