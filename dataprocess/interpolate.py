from dataprocess.datautil import getUniqueFilename
from dataprocess.mathutil import interpolate
from dataprocess.datautil import splitData
from os.path import splitext, isfile
from os import remove, rename

def interpolateMissingData(file, col_idx):
    searching_end = False
    prev_row = []
    faulty_lines = []

    with open(file, mode='r') as input_data:
        new_filename = getUniqueFilename(file)
        csv_copy = open(new_filename, 'w')
    
        for _, line in enumerate(input_data):
            row = splitData(line, '.csv')

            if row[col_idx] == ' \n' and not searching_end:
                start_value = float(prev_row[col_idx]) # prev still has the start value
                searching_end = True
            if searching_end and row[col_idx] != ' \n':
                end_value = float(row[col_idx])
                interp_values = interpolate(start_value, end_value, len(faulty_lines))
                for i in range(len(faulty_lines)):
                    row = faulty_lines[i]
                    row[col_idx] = str(interp_values[i])
                    if col_idx + 1 == len(row):
                        csv_copy.write(', '.join(row) + '\n')
                    else:
                        csv_copy.write(', '.join(row))
                
                faulty_lines.clear()
                searching_end = False

            if not searching_end:
                csv_copy.write(line)
            else:
                faulty_lines.append(row)

            prev_row = row

    csv_copy.close()
    remove(file)
    rename(new_filename, file)
