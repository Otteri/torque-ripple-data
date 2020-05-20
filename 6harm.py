from python_interface import Ilmarinen
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import gridspec

def runSimulator():
    N = 1000 # amount of samples
    sim = Ilmarinen.SandboxApi()

    # Preallocate space
    time = np.zeros(N)
    data = np.zeros((20, N), dtype=float)

    # Use ILC?
    sim.command.setSpeedReference(0.04)
    #sim.command.toggleILC(True)
    #sim.command.setFiiILC(10.0)
    #sim.command.setGammaILC(5.0)
    sim.command.setCompensationCurrentLimit(0.5)

    # Start sim and let it to settle
    sim.command.step(90)

    # Log data
    for i in range(N):
        FA2TC_data = sim.signal.gt_FA2TC_data_()
        time[i] = sim.status.getTimeStamp()
        data[0][i] = sim.signal.getCoggingTorque()
        data[1][i] = sim.signal.getSimActualTorqueFiltered()
        data[2][i] = sim.signal.getCompensationTorque() # getCompensationTorque / getCompensationCurrent
        data[3][i] = sim.signal.getRotorMechanicalAngle()
        data[4][i] = FA2TC_data.m_ref
        data[5][i] = sim.signal.getTripCode()
        data[6][i] = sim.signal.getCtrlActualTorqueAverage()
        data[7][i] = sim.signal.getMeasuredSpeed()
        data[8][i] = FA2TC_data.n_meas
        data[9][i] = sim.signal.getRotorElectricalAngleCtrl()
        data[10][i] = sim.signal.getRotorMechanicalAngleCtrl()
        data[11][i] = sim.signal.getSimActualTorque()
        data[12][i] = sim.signal.getStatorFluxes().x
        data[13][i] = sim.signal.getRotorFluxes().x
        sim.command.step(0.002) # sampling interval

        # To test if compensation can be applied
        #sim.signal.setCompensationCurrent(0.5)
        #sim.signal.setCompensationTorque(0.1)

    del sim # free resources

    return time, data



def plot(x, y1, y2, y3):


    def getFFT(signal):
        Y = np.fft.fft(signal)/L              # Transform
        P = np.abs(Y[0:len(Fv)]*2)            # get scaled one-sided FT
        return P
    
    T = x[1] - x[0]                   # sampling interval 
    L = x.size                            # data vector length
    Fn = (1/T)/2                              # calculate frequency
    Fv = np.linspace(0, 1, int(np.fix(L / 2)))*Fn  # frequency vector (one-sided)


    # plot it
    fig = plt.figure(figsize=(8, 6))
    plt.rc('grid', linestyle='dotted', color='silver')
    fig.canvas.set_window_title("6th harmonic") 
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1]) 
    ax0 = plt.subplot(gs[0])
    plt.xlabel('time [s]')
    plt.ylabel('Amplitude [pu.]')
    #ax0.legend()
    plt.grid(True)
    plt.margins(0, .05)
    #ax0.yaxis.set_major_locator(plt.MaxNLocator(6))
    ax0.set(ylim=(-0.3, 0.3))

    d1 = ax0.plot(x, y1, label='Compensation torque', linewidth=0.8, color='green')
    d2 = ax0.plot(x, y2, label='Pulsating torque', linewidth=0.8, color='blue')
    d3 = ax0.plot(x, y3, label='Total torque (filtered)', linewidth=0.8, color='red')
    ax0.legend([d1, d2, d3], ['Compensation torque', 'Pulsating torque', 'Total torque (filtered)'])

    ax1 = plt.subplot(gs[1])
    ax1.set(ylim=(0, 0.3))
    ax1.yaxis.tick_right()
    #ax1.yaxis.set_major_locator(plt.MaxNLocator(6))

    index = np.arange(1)
    bar_width = 0.10
    rects1 = ax1.bar(index, getFFT(y1), bar_width,
    color='g',
    label='data 1') 

    rects2 = ax1.bar(index + bar_width, getFFT(y2), bar_width*0.8,
    color='b',
    label='data 2')

    rects3 = ax1.bar(index + 2 * bar_width, getFFT(y3), bar_width*0.8,
    color='r',
    label='data 3')

    plt.xlabel('6th harmonic')
    ax1.set_xticks([], [])
    #plt.ylabel('Amplitude [pu.]')
    #plt.legend()

    plt.tight_layout()
    plt.savefig("picture2.svg", bbox_inches='tight', pad_inches=0)

def main():
    # Obtain data
    time, data = runSimulator()

    #x = np.arange(0, 10, 0.2)
    #y = np.sin(x)

    #x = time

    plot(time, data[2], data[0], data[1])
    
    # Wait user to close the plots
    plt.show(block=True)

if __name__ == '__main__':
    main()
