from python_interface import Ilmarinen
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Approx rotate the rotor to beginning.
def runToStart(sim):
    theta = sim.signal.getRotorMechanicalAngleCtrl()
    while theta > 0.01:
        sim.command.step(0.001)
        theta = sim.signal.getRotorMechanicalAngleCtrl()
    return theta

def oneRotation():
    N = 1000 # Angle resolution max
    sim = Ilmarinen.SandboxApi()

    # Use ILC?
    speed = 0.02
    sim.command.setSpeedReference(speed)

    # Start sim and let it to settle
    sim.command.step(15)
    runToStart(sim)
    theta = sim.signal.getRotorMechanicalAngleCtrl()

    times = []
    speeds = []
    coggings = []
    thetas = []

    # Log data
    while theta < 0.99:
        times.append(sim.status.getTimeStamp())
        coggings.append(sim.signal.getCoggingTorque())
        speeds.append(sim.signal.getMeasuredSpeed())
        sim.command.step(0.001) # sampling interval
        theta = sim.signal.getRotorMechanicalAngleCtrl()
        thetas.append(theta)
    speed = speed + 0.01
    sim.command.setSpeedReference(speed)
    theta = runToStart(sim) # error non constant dt
    print("speed:", speed)

    del sim # free resources
    return times, speeds, coggings, thetas    

def anglePlot(X, Y):
    fig, ax = plt.subplots(figsize=(16,10), dpi=80)
    ax.plot(X, Y, '-o', label='Pulsating torque', linewidth=1.0, markersize=5, color='blue')
    plt.ylabel("Amplitude [pu.]")
    plt.xlabel(r"Rotor angle ($\theta_{m}$)")
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    # Replace [0, 1] angle as with [0, 2pi]
    labels = [0, 0, r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    ax.set_xticklabels(labels)
    plt.show()

def main():
    times, speeds, coggings, thetas = oneRotation()
    anglePlot(thetas, coggings)

if __name__ == '__main__':
    main()
