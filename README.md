# torque-ripple-data
Contains scripts, measurement, simulation and FEM data. Scripts can be used for processing and visualizing the data.
All FEM data was collected using a model of 160-kW PM motor. Experimental test data was collected using a resolver, torque transducer and two different PM motors: SDM251 (0.72 kW) and MS4887 (6 kW). The measured data in `experimental-data` must be converted to CSV-format before it can be plotted.

## Data preprocessing
Some data files must be converted to CSV-format and scaled. Preprocessing can be done fully automatically by calling:  
`$ python auto-preprocess.py`,   
which converts and scales the data using other scripts in the repository. The use of `auto-preprocess.py` script is encouraged, as it should do the scaling correctly and it moves the processed data into predetermined folder location, which allows the examples below to be executed as is.

## Examples calls
Examples showing how scripts can be used for plotting data.

#### barchart3d.py
Creates a 3D barchart showing cogging torque of the 160-kw motor used in the FEM simulations.  
`$ python barchart3d.py`

#### compare-harmonics.py
Produces four amplitude spectrums that are side to side.  
`$ python compare-harmonics.py --poles 8 --run_speed 60 --is_ilc 0 --is_torque 0 --folder ./processed/PI-QLR-MS4887/speed_60rpm/`
`$ python compare-harmonics.py --poles 8 --run_speed 60 --is_ilc 1 --is_torque 0 --folder ./processed/PI-ILC-MS4887/motoring/60rpm-speed/`

#### compare-speed-ripple.py
Produces four time domain speed graphs.  
`$ python compare-speed-ripple.py --is_ilc 0 --folder ./processed/PI-QLR-MS4887/speed_60rpm/`
`$ python compare-speed-ripple.py --is_ilc 1 --folder ./processed/PI-ILC-MS4887/motoring/60rpm-speed/`

#### compute-ripple.py
Calculates ripple factor using provided data (only prints).  
`$ python compute-ripple.py --run_speed 60 --nominal 2000 -f1 "./processed/PI-QLR-MS4887/speed_60rpm/Qlr-ON_80%-load_T0.04_lambda1.0.Monitor(1).csv" -f2 "./processed/PI-QLR-MS4887/speed_60rpm/Qlr-OFF_80%-load.Monitor(1).csv"`

#### plot.py
Current configuration generate the pulsation graph, but can be used for plotting various views:  
`$ python plot.py --file "./simulation-data/FEM/torque-speed-pulsations.csv"`

#### pulsations3d.py
Creates 3D plot showing speed pulsations with PI, ILC and Q-learning (15 measurements in total).  
`$ python pulsations3d.py`

#### sim-harmonics.py
Creates frequency domain plots that shows compensation and disturbance harmonics simultaneously.  
`$ python sim-harmonics.py --file1 "./simulation-data/MS4887-simulations/compensation/ilc_on_data_4.75phi_1.0gamma_0.15alpha_10%-noise.npy"`

#### simplot.py
Simulated speed and torque pulsations.  
`$ python simplot.py`  

#### compare.py
Plot three (or six) different measurements into same plot view. This plotting script was never used, as compensators should not be compared directly. Example call:  
`$ python compare.py --poles 8 --run_speed 60 --save 1 --file1 "./processed/PI-QLR-MS4887/speed_60rpm/Qlr-OFF_50%-load.Monitor(1).csv" --file2 "./processed/PI-ILC-MS4887/motoring/60rpm-speed/ILC-ON_50%-load_2.8phi_1.0gamma_0.15alpha.Monitor(1).csv" --file3 "./processed/PI-QLR-MS4887/speed_60rpm/Qlr-ON_10%-load_T0.02_lambda1.0.Monitor(1).csv"`

#### harmonics.py
Plots frequency spectrum of all files in a directory. Very convinient script for quickly checking the harmonics. Just call the script and then provide directory path when it is asked.  
`$ python harmonics.py`
