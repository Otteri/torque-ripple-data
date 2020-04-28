from dataprocess.interpolate import interpolateMissingData
from dataprocess.datacollect import collectData
from dataprocess.retime import reTime
from os import remove, walk, getcwd
import argparse
import sys

# This file automates data handling. Converts raw-data to more easily usable format.
# The conversion procedures are defined elsewhere; only calls correct functions.

def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_time", type=float, default=float('-inf'), help="Start data collection [s]")
    parser.add_argument("--end_time", type=float, default=float('inf'), help="Stop data collection [s]")
    parser.add_argument("--time_idx", type=int, default=0, help="Time column index in datafile")
    return parser.parse_args(args)

def askFileRemove(files):
    ans = input("Delete original datafiles? (y/N)\n")
    if(ans == 'y' or ans == 'Y'):
        for file in files:
            remove(file)
            print("Removed '{}'".format(file))

if __name__ == '__main__':
    args = parseArgs()

    print("Info: Using column index '{}' for the time data".format(args.time_idx))
    time_tuple = (args.time_idx, args.start_time, args.end_time)
        
    directory_path = input("Which files require processing? Give full path to the directory:\n")
    (_, _, files) = next(walk(directory_path))
    files = [directory_path + '\\' + file for file in files]
    print("Files from '{}' will be processed.\n".format(getcwd()))

    print("What kind of data you are trying to process?")
    print("  [1] Simulator (.csv)")
    print("  [2] Composer  (.dcexp)")
    print("  [3] DT        (.txt)")
    ans = int(input())

    processed_files = []
    for file in files:
        if ans == 1:
            # Simulator data
            old_file, new_file = collectData(file, 2, '.csv', ', ', time_tuple)
            interpolateMissingData(new_file, 1)
            reTime(new_file, 0, 'ms') # make time to start from 0
            processed_files.append(old_file)
        elif ans == 2:
            # Composer data
            old_file, new_file = collectData(file, 8, '.dcexp', ', ', time_tuple)
            interpolateMissingData(new_file, 1)
            reTime(new_file, 0)
            processed_files.append(old_file)
        elif ans == 3:
            # DT data
            old_file, new_file = collectData(file, 0, '.txt', ', ', time_tuple=time_tuple, convert=(1, 2000))
            interpolateMissingData(new_file, 1)
            reTime(new_file, 0)
            processed_files.append(old_file)
        else:
            print("Invalid selection")
    if len(processed_files) > 0:
        askFileRemove(processed_files) # give an option to delete original files
