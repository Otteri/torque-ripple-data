import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from os import remove, walk, getcwd
import matplotlib.patches as mpatches

BASE_PATH = ".\\processed\\SDM"

color1 = '#1d9bf0'
color2 = '#43ccd9'
color3 = '#a0eb9f'
color4 = '#e0ce75'
color5 = '#fa9e55'
color6 = '#ff4926'

#color2 = '#e15129'
#color1 = '#0896d3'

color1 = '#0896d3'
color2 = '#69c386'
color3 = '#e15129'

def plot(ilc_times, ilc_speeds, qlr_times, qlr_speeds, default_times, default_speeds):
    # plot the data
    fig = plt.figure()
    ax = fig.gca(projection='3d')


    ax.plot(ilc_times[0], np.full((500, 1), 1), ilc_speeds[0], label='parametric curve', linewidth=0.8, color=color2)
    ax.plot(ilc_times[1], np.full((500, 1), 2), ilc_speeds[1], label='parametric curve', linewidth=0.8, color=color2)
    ax.plot(ilc_times[2], np.full((500, 1), 3), ilc_speeds[2], label='parametric curve', linewidth=0.8, color=color2)
    ax.plot(ilc_times[3], np.full((500, 1), 4), ilc_speeds[3], label='parametric curve', linewidth=0.8, color=color2)
    ax.plot(ilc_times[4], np.full((500, 1), 5), ilc_speeds[4], label='parametric curve', linewidth=0.8, color=color2)

    ax.plot(qlr_times[0], np.full((500, 1), 1), qlr_speeds[0], label='parametric curve', linewidth=0.8, color=color3)
    ax.plot(qlr_times[1], np.full((500, 1), 2), qlr_speeds[1], label='parametric curve', linewidth=0.8, color=color3)
    ax.plot(qlr_times[2], np.full((500, 1), 3), qlr_speeds[2], label='parametric curve', linewidth=0.8, color=color3)
    ax.plot(qlr_times[3], np.full((500, 1), 4), qlr_speeds[3], label='parametric curve', linewidth=0.8, color=color3)
    ax.plot(qlr_times[4], np.full((500, 1), 5), qlr_speeds[4], label='parametric curve', linewidth=0.8, color=color3)

    ax.plot(default_times[0], np.full((500, 1), 1), default_speeds[0], label='parametric curve', linewidth=0.8, color=color1)
    ax.plot(default_times[1], np.full((500, 1), 2), default_speeds[1], label='parametric curve', linewidth=0.8, color=color1)
    ax.plot(default_times[2], np.full((500, 1), 3), default_speeds[2], label='parametric curve', linewidth=0.8, color=color1)
    ax.plot(default_times[3], np.full((500, 1), 4), default_speeds[3], label='parametric curve', linewidth=0.8, color=color1)
    ax.plot(default_times[4], np.full((500, 1), 5), default_speeds[4], label='parametric curve', linewidth=0.8, color=color1)

    ax.set_xlabel('Time [s]', labelpad=10, fontsize=14)
    ax.set_ylabel('Speed reference [rpm]', labelpad=10, fontsize=14)
    ax.set_zlabel('Speed error [rpm]', labelpad=10, fontsize=14)

    # make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    plt.yticks(np.arange(1, 6, step=1), ('60', '120', '240', '360', '480'), fontsize=14)
    ax.set_zlim(-50, 50)
    ax.set_xlim(0.5, 0.0)

    plt.tick_params(axis='both', labelsize=12)

    pi = mpatches.Patch(color=color1, label='PI')
    pi_ilc = mpatches.Patch(color=color2, label='ILC')
    pi_qlr = mpatches.Patch(color=color3, label='Q-learning')
    ax.legend(handles=[pi, pi_ilc, pi_qlr], ncol=1, loc='upper left', fancybox=True, bbox_to_anchor=(0.13, 0.85), fontsize=14)

    fig.tight_layout()
    plt.savefig("3d-pulsations.pdf", bbox_inches='tight', pad_inches=0)
    plt.show(block=True)

def main():

    ilc_times = []
    ilc_speeds = []
    qlr_times = []
    qlr_speeds = []
    default_times = []
    default_speeds = []

    (_, _, files) = next(walk(BASE_PATH))
    files = [BASE_PATH + '\\' + file for file in files]
    print("Files from '{}' will be processed.\n".format(getcwd()))

    for file in files:
        with open(file, mode='r') as datafile:

            # Load the data
            colnames = ['time', 'speed']
            df = pd.read_csv(datafile, names=colnames)
            df = df.apply(pd.to_numeric)

            # Convert pandas datacolumns to numpy arrays
            time_data = df['time'].to_numpy()[0:500]     # [s]
            speed_data = df['speed'].to_numpy()[0:500]   # [p.u.]
            speed_data = speed_data * 2000 # [rpm]

            # Shift to zero
            offset = np.mean(speed_data)
            speed_data = speed_data - offset

            if "ilc-on" in file.lower():
                print("file:", file)
                ilc_times.append(time_data)
                ilc_speeds.append(speed_data)
            elif "qlr-on" in file.lower():
                print("file:", file)
                qlr_times.append(time_data)
                qlr_speeds.append(speed_data)
            elif "off" in file.lower():
                print("file:", file)
                default_times.append(time_data)
                default_speeds.append(speed_data)

    plot(ilc_times, ilc_speeds, qlr_times, qlr_speeds, default_times, default_speeds)



if __name__ == '__main__':
    main()