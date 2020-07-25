# torque-ripple-data
Contains measurement and simulation data as well as scripts for visualizing the data.

All FEM data was collected using a model of 160-kW PM motor. Experimental data was collected using two different PM motors: SDM251 and MS4887.
The experimental data must be first converted to CSV-format, before it can be plotted.

## Preprocess data
1. Convert measured data into csv-format:  
cd to data-analysis directory (repository root)
2. Copy data to preserve the original files and avoid mixing different formats:  
`cp -r ./experimental-data/PI-ILC-MS4887/motoring/60rpm-speed ./experimental-data/PI-ILC-MS4887/motoring/60rpm-speed/csv`
3. Process data. Convert it to csv format and scale values:  
if speed data, then:
python preprocess --convert 1,2000
Give directory path: ./experimental-data/PI-ILC-MS4887/motoring/60rpm-speed/csv
Since data is in .txt format, select 3
Because we already copeied the data, it is okay to delete the original files. Select y.
If torque data, then scale with:
python preprocess --convert 1,-1 and do the same as above.


## Examples calls
Examples showing how scripts can be used for plotting.

### barchart3d.py
`$ python barchart3d.py`

### compare-harmonics.py
Produces four amplitude spectrums that are side to side.  
`$ python compare-harmonics.py --poles 8 --run_speed 60 --is_ilc 0 --is_torque 0 --folder ./processed/PI-QLR-MS4887/speed_60rpm/`
`$ python compare-harmonics.py --poles 8 --run_speed 60 --is_ilc 1 --is_torque 0 --folder ./processed/PI-ILC-MS4887/motoring/60rpm-speed/`

### compare-speed-ripple.py
Produces four time domain speed graphs.  
`$ python compare-speed-ripple.py --is_ilc 0 --folder ./processed/PI-QLR-MS4887/speed_60rpm/`
`$ python compare-speed-ripple.py --is_ilc 1 --folder ./processed/PI-ILC-MS4887/motoring/60rpm-speed/`

### compute-ripple.py
Calculates ripple factor using provided data
`$ python compute-ripple.py --run_speed 60 --nominal 2000 -f1 "./processed/PI-QLR-MS4887/speed_60rpm/Qlr-ON_80%-load_T0.04_lambda1.0.Monitor(1).csv" -f2 "./processed/PI-QLR-MS4887/speed_60rpm/Qlr-OFF_80%-load.Monitor(1).csv"`

### plot.py
Current configuration can be used to generate the pulsation graph:  
`$ python plot.py --file "./simulation-data/FEM/torque-speed-pulsations.csv"`

### pulsations3d.py
The data needs to be processed first and then placed to: experimental-data\\SDM  
`$ python pulsations3d.py`

### sim-harmonics.py
Creates frequency domain plots that show compensation harmonics and disturbance harmonics.  
`$python sim-harmonics.py "<some .npy file>"`

### simplot.py
Simulated speed and torque pulsations.  
`$ python simplot.py`  
Then give path to simulation-data/MS4887-simulations/pulsations

### Unused scripts
These scripts are functional, but were never used for producing images to the thesis.

#### compare.py
Either plot only speed/torque measurements by providing only three paths.
It is also possible to plot torque and speed to same view providing three speed measurements and three torque measurements.
`$ python compare.py --poles 8 --run_speed 60 --save 1 --file1 "<file1 path>" --file2 "<file2 path>" --file3 "<file3 path>"`
`$ python compare.py --poles 8 --run_speed 60 --save 1 --file1 "<file1 path>" --file2 "<file2 path>" --file3 "<file3 path>" --file4 "<file4 path>" --file5 "<file5 path>" --file6 "<file6 path>"`

#### harmonics.py
Plots frequency spectrum of all files in a directory. Very convinient script for quickly checking the harmonics. Just call the script and then provide path when it is asked.  
`$ python harmonics.py`
