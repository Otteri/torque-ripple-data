from pathlib import Path
import numpy as np
import os
import re

# Functions that can be used in multiple files
# Functions cans have data related assumptions, so may be unusable
# with other kind of data.

# Various filetypes may require different data splitting schemes
# Collect only the values separated by the delimiter into array
# Data row: one line of data.
def splitDataRow(data_row, file_ext):
    # Composer data
    if(file_ext) == '.dcexp':
        new_row = re.split(r'\t+|\n', data_row)
    # Simulator data
    elif(file_ext) == '.csv':
        new_row = re.split(r',|\n', data_row)
    # Fem data
    elif(file_ext) == '.fem':
        new_row = re.split(r';|\n', data_row)
    # DT data
    elif(file_ext) == '.txt':
        new_row = re.split(r'\t|\n', data_row)
    else:
        raise ValueError('Unknown file extensions passed')    
    return new_row

# Removes preceding path, file extension and possible copy number
def getBaseName(filename):
    base_name = os.path.basename(filename)
    base_name = os.path.splitext(base_name)[0]
    base_name = re.split(r'\(\d\)', base_name)[0]
    return base_name
    
# Increase index in the filename until the name doesn't conflict
# By default no index is given.
def getUniqueFilename(file):
    i = 1
    p = Path(file)
    #print(p.parent)
    base_name = getBaseName(file)
    new_filename = os.path.join(str(p.parent), base_name + '(' + str(i) + ')' + '.csv')
    while os.path.isfile(new_filename):
        new_filename = os.path.join(str(p.parent), base_name + '(' + str(i) + ')' + '.csv')
        i += 1
    print("new filename:", new_filename)
    return new_filename

def convertToSeconds(value, original_unit):
    if original_unit == 's':
        return value
    elif original_unit == 'ms':
        return value * 1e-3
    elif original_unit == 'us':
        return value * 1e-6
    elif original_unit =='ns':
        return value * 1e-9
    else:
        raise ValueError("Unknown unit")

# Writes the data rows so that line endings go correctly
# Row: array of values
# Could possibly utilize csv-writer
def writeDataRow(file, row):
    if row[-1].isspace() or row[-1] == '':
        row = row[0:-1]
    file.write(', '.join(row) + '\n')
