from dataprocess import mathutil
import pandas as pd
import numpy as np
import argparse
import sys

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_speed", type=float, default=None, help="Speed [rpm]", required=True)
    parser.add_argument("--file1", "-f1", type=str, help="Csv-data file 1", required=True)
    parser.add_argument("--file2", "-f2", type=str, help="Csv-data file 2", default=None)
    parser.add_argument("--nominal", "-N", type=float, help="Nominal value (e.g. torque, speed)", default=None, required=True)
    parser.add_argument("--convert", type=float, help="Multiply with coeff to get nominal", default=None)
    parser.add_argument("--is_torque", type=int, help="", default=None)
    args = parser.parse_args(args)
    return args

# Load the csv-data
def loadData(file_path, is_torque=None):
    colnames = ['time', 'signal', 'signal2']
    df1 = pd.read_csv(file_path, names=colnames)
    t = df1['time'].to_numpy()
    y1 = df1['signal'].to_numpy()
    
    if is_torque:
        y2 = df1['signal2'].to_numpy()
        return t, y1, y2
    else:
        return t, y1

def main():
    args = parseArgs()

    if args.is_torque:
        t1, y1, y2 = loadData(args.file1, args.is_torque)
    else:
        t1, y1 = loadData(args.file1)

    # Get only one period of data
    y1 = mathutil.getDataPeriod(args.run_speed, t1, y1)
    if args.convert:
        y1 = y1 * args.convert

    r1 = mathutil.calculateRippleFactor(y1, args.nominal)
    print("RF1:", r1)

    if args.file2:
        t2, y2 = loadData(args.file2)
        y2 = mathutil.getDataPeriod(args.run_speed, t2, y2)
        r2 = mathutil.calculateRippleFactor(y2, args.nominal)
        print("RF2:", r2)
        print("Ratio:", (r1 / r2))

if __name__ == '__main__':
    main()
