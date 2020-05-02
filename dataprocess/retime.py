from dataprocess import datautil
from os import remove, rename
from glob import glob
import csv

###################################################################
# What the script does?
# Script removes the possible time offset from csv-files. 
# I.e. time starts from zero. Plots may look better after this.
# It is assumed that the sampling frequency is constant.
####################################################################

# files (list): provide filenames that should be processed, ext is still required
# time_idx (int): time data column index-number
# time_unit (str): unit used in the input file.
def reTime(file, time_idx, time_unit='s'):
    with open(file, mode='r') as csv_file:
        #copy = open(file + "_copy", 'w')
        csv_reader = csv.reader(csv_file, delimiter=',')
        #csv_copy = csv.writer(copy, delimiter=',', lineterminator = '\n',
        #    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        new_filename = datautil.getUniqueFilename(file)
        csv_copy = open(new_filename, 'w')

        original_start_time = None
        for line_count, row in enumerate(csv_reader):
            time = datautil.convertToSeconds(float(row[time_idx]), time_unit)
            if line_count == 0:
                # Do error checking for the first line
                # if time already starts at zero -> skip.
                if (row[time_idx]) == 0.0:
                    print("Skipping {}".format(file))
                    remove(copy)
                    return
                # Check that there is no titles or such.
                if isinstance(row, str):
                    raise ValueError('Data values must be numeric')

                original_start_time = time # store the time
                row[time_idx] = str(0.0) # We wanted the time to start at zero
                datautil.writeDataRow(csv_copy, row)
            else:
                row[time_idx] = str(time - original_start_time)
                datautil.writeDataRow(csv_copy, row)

        csv_copy.close()

    remove(file)
    rename(new_filename, file)
    print("Info: '{}' has been zero timed".format(file))

if __name__ == '__main__':
    file = input("Give file path:\n")
    reTime(file, 0, 'ms')
