from dataprocess import datautil
from os.path import splitext, isfile
from os import remove, rename
import numpy as np

# By giving the same read and write column index, 
# the script replaces the original values with filtered ones.
# Call only to .csv data.
# n: how many values are averaged
# Averaged data is sparser, so should interpolate after.
# indices start from zero
# dtype: data producer. Information is used for splitting the datacolumns
def avgFilterData(file, read_col, write_col, dtype='.csv', n=10):
    value_history = []

    with open(file, mode='r') as input_data:
        new_filename = datautil.getUniqueFilename(file)
        csv_copy = open(new_filename, 'w')
    
        for line_idx, line in enumerate(input_data):
            row = datautil.splitDataRow(line, dtype)
            value_history.append(float(row[read_col]))
            avg = np.mean(value_history[-n:]) if line_idx > n else np.mean(value_history)

            # Overwrite an existing column
            try:
                row[write_col] = str(avg)
            # Crate new columns. (Provided index is bigger than the array)
            except IndexError:
                missing_columns_num = write_col - (len(row)-1)
                empty_columns = (',') * missing_columns_num
                row.extend(empty_columns)
                row[write_col] = str(avg)
            
            # Write to a file
            datautil.writeDataRow(csv_copy, row)

    csv_copy.close()
    remove(file)
    rename(new_filename, file)

if __name__ == '__main__':
    file = input("Give file path:\n")
    avgFilterData(file, 2, 3, n=100)
