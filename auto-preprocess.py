from pathlib import Path
import subprocess
from os import remove

from dataprocess.interpolate import interpolateMissingData
from dataprocess.datacollect import collectData
from dataprocess.retime import reTime
from dataprocess.avgfilter import avgFilterData

process = [
    "./experimental-data/PI-ILC-MS4887",
    "./experimental-data/PI-ILC-SDM251-elec",
    "./experimental-data/PI-QLR-MS4887",
    "./experimental-data/PI-QLR-SDM251",
]

processed_files = []

for folder in process:
    source = folder.lstrip("./")
    dest = "./processed/"
    Path(dest).mkdir(parents=True, exist_ok=True)
    bashCommand = "cp -r {0} {1}".format(source, dest)
    print("Copying '{0}' to '{1}'".format(source, dest))
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

p = Path(dest)
subdirectories = list(Path(p).glob('**/*.txt'))

# Convert and scale
for path in subdirectories:
    path = path.resolve()
    file = str(path)

    if 'MS4887' in file and 'speed' in file:
        scale = 2000
    elif 'MS4887' in file and 'torque' in file:
        scale = -1
    elif 'SDM251' in file and 'speed' in file:
        scale = 3000
    else:
        scale = 1

    old_file, new_file = collectData(file, 0, '.txt', ', ', convert=[(1, scale)])
    print("old: ", old_file, "new:", new_file)
    interpolateMissingData(new_file, 1)
    reTime(new_file, 0)
    remove(old_file)

# copy certain SDM data to individual folder
copy_files = [
    "./processed/PI-QLR-SDM251/Qlr-OFF_0%-load_060rpm.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-OFF_0%-load_120rpm.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-OFF_0%-load_240rpm.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-OFF_0%-load_360rpm.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-OFF_0%-load_480rpm.Monitor(1).csv",
    "./processed/PI-ILC-SDM251-elec/ILC-ON_0%-load_1.5phi_0.9gamma_0.15alpha_060rpm_3filt.Monitor(1).csv",
    "./processed/PI-ILC-SDM251-elec/ILC-ON_0%-load_1.5phi_0.9gamma_0.15alpha_120rpm_3filt.Monitor(1).csv",
    "./processed/PI-ILC-SDM251-elec/ILC-ON_0%-load_1.5phi_0.9gamma_0.15alpha_240rpm_3filt.Monitor(1).csv",
    "./processed/PI-ILC-SDM251-elec/ILC-ON_0%-load_1.5phi_0.9gamma_0.15alpha_360rpm_3filt.Monitor(1).csv",
    "./processed/PI-ILC-SDM251-elec/ILC-ON_0%-load_1.5phi_0.9gamma_0.15alpha_480rpm_3filt.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-ON_060rpm_0.03T_0.3alpha_32lambda.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-ON_120rpm_0.03T_0.3alpha_32lambda.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-ON_240rpm_0.03T_0.3alpha_32lambda_trained120rpm.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-ON_360rpm_0.03T_0.3alpha_32lambda_trained60rpm.Monitor(1).csv",
    "./processed/PI-QLR-SDM251/Qlr-ON_480rpm_0.03T_0.3alpha_32lambda_trained60rpm.Monitor(1).csv",
]

for file in copy_files:
    source = file
    dest = "./processed/SDM/"
    Path(dest).mkdir(parents=True, exist_ok=True)
    bashCommand = "cp -r {0} {1}".format(source, dest)
    print("Copying '{0}' to '{1}'".format(source, dest))
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
