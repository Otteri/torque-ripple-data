from dataprocess.datautil import convertToSeconds
from dataprocess.datautil import splitData
from os.path import splitext, isfile
from os import remove, rename
from glob import glob
import csv
import re

##############################################################################
# What the script does?
# Script removes irrelevant string-data and leaves only numerical values.
# This allows use of e.g. CSV-reader in Matlab. It is also possible to provide
# a time range, which is used for the data collection.
#
# Usage:
# Setting: data_start_row > 0, allows to skip columnames and such.
##############################################################################

# Removes strings from beginning and converts the original file to csv-format.
# data_start_row (int): Data starts from this row. (Skips preceding rows)
# file_ext (str): extension of the files that shall be processed
# delimeter_out (str): delimeter to be used in the output data file
# Optional, time_tuple: (time_col_idx, start_time, end_time)
def collectData(file, data_start_row, file_ext, delimiter_out, time_tuple=(0, float('-inf'), float('inf'))):

    # Removes extension and possible copy number from the filename
    def getBaseName(filename):
        base_name = splitext(file)[0]
        base_name = re.split(r'\(\d\)', base_name)[0]
        return base_name

    # Increase index in the filename until the name doesn't conflict
    # By default no index is given.
    def getUniqueFilename(filename):
        i = 1
        base_name = getBaseName(filename)
        new_filename = base_name + '.csv'
        while isfile(new_filename):
            new_filename = base_name + '(' + str(i) + ')' + '.csv'
            i += 1
        return new_filename

    # Always written like: time [ms] OR Time(s)
    # Picks the unit inside brackets / parantheses
    def getTimeUnit(string):
        m = re.search(r'\[\w+\]|\(\w+\)', string)
        unit = m.group(0)[1:-1]
        return unit

    with open(file, mode='r') as input_data:
        new_filename = getUniqueFilename(file)
        csv_copy = open(new_filename, 'w')
    
        for idx, row in enumerate(input_data):
            row = splitData(row, file_ext)

            # Search time unit from the beginning of the file
            if "time" in row[time_tuple[0]].lower():
                time_unit = getTimeUnit(row[time_tuple[0]])

            # Start collecting data values
            if idx > data_start_row:
                time_seconds = convertToSeconds(float(row[time_tuple[0]]), time_unit)

                if time_tuple[1] <= time_seconds <= time_tuple[2]:
                    new_row = str(delimiter_out.join(row))
                    csv_copy.write(new_row)

        csv_copy.close()

        print("Processed '{}' ({} rows).".format(file, idx+1)) 
    return (file, new_filename)

if __name__ == '__main__':
    files = glob('*' + '.csv')

    # Use this for Composer monitor files
    # collectData(files, 8, '.dcexp' , ', ')

    # Use this for simulators csv-logs
    collectData(files, 2, '.csv', ',')