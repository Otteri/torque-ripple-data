from os.path import splitext, isfile
import numpy as np
import re

# Functions that can be used in multiple files
# Functions cans have data related assumptions, so may be unusable
# with other kind of data.

# Various filetypes may require different data splitting schemes
def splitData(data_row, file_ext):
    if(file_ext) == '.dcexp':
        return re.split(r'\t+', data_row)
    elif(file_ext) == '.csv':
        return re.split(r',', data_row)

# Removes extension and possible copy number from the filename
def getBaseName(filename):
    base_name = splitext(filename)[0]
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