from dataprocess import datautil
from os.path import splitext, isfile
from os import remove, rename
from glob import glob
import csv
import re

"""
What the script does?
Main task is to remove all irrelevant data and leave only measured values.
The refined data is then saved into csv file, which allows further use. 
By providing the optional arguments, the script can also:
- collect the data from certain time span
- convert values by multiplying with a given coefficient

data_start_row (int): Data starts from this row. (Skips preceding rows).
file_ext       (str): extension of the files that shall be processed.
delimeter_out  (str): delimeter to be used in the output data file. Optional.
time_tuple     (time_col_idx, start_time, end_time), optional.
convert        (col_idx, multiplier), optional.
"""
def collectData(file, data_start_row, file_ext, delimiter_out=', ', time_tuple=(0, float('-inf'), float('inf')), convert=None):

    # Always written like: time [ms], Time [s] or Time(s)
    # Picks the unit inside brackets / parantheses
    def getTimeUnit(string):
        m = re.search(r'\[\w+\]|\(\w+\)', string)
        unit = m.group(0)[1:-1]
        return unit

    with open(file, mode='r') as input_data:
        new_filename = datautil.getUniqueFilename(file)
        csv_copy = open(new_filename, 'w')
    
        for idx, row in enumerate(input_data):
            row = datautil.splitDataRow(row, file_ext)

            # Search time unit from the beginning of the file
            if "time" in row[time_tuple[0]].lower():
                time_unit = getTimeUnit(row[time_tuple[0]])

            # Start collecting data values
            if idx > data_start_row:
                time_seconds = datautil.convertToSeconds(float(row[time_tuple[0]]), time_unit)
                if convert:
                    row[convert[0]] = str(float(row[convert[0]]) * convert[1])

                if time_tuple[1] <= time_seconds <= time_tuple[2]:
                    datautil.writeDataRow(csv_copy, row)

        csv_copy.close()

        print("Processed '{}' ({} lines).".format(file, idx+1)) 
    return (file, new_filename)

if __name__ == '__main__':
    file = input("Give file path:\n")

    # Use this for Composer monitor files
    # collectData(files, 8, '.dcexp' , ', ')

    # Use this for simulators csv-logs
    collectData(file, 2, '.fem', ', ', time_tuple=(0, 2.0, 3.0))