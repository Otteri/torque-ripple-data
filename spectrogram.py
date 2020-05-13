import matplotlib.pyplot as plt
import numpy as np

def spectogram(X, Y):

    #Fs_step = X[1] - X[0]
    #time_step = (1/fs_step)
    dt = 0.000008
    Fs = 2000
    #t = np.linspace(0,0.003192, 400)
    #t = (1/X)
    #print("t:",)

    #X = X[0:75]
    #Y = Y[0:75]
    #X = X[0:-100]
    #Y = Y[0:-100]
    

    NFFT = 256  # the length of the windowing segments

    fig, (ax1, ax2) = plt.subplots(nrows=2)
    #ax1.plot(X, Y)
    ax1.plot(X, Y, '-o', label='Pulsating torque', linewidth=1.0, markersize=5, color='darkorange')
    Pxx, freqs, bins, im = ax2.specgram(Y, NFFT=NFFT, Fs=Fs, noverlap=128)
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the matplotlib.image.AxesImage instance representing the data in the plot

    #cbar = fig.colorbar(im)
    #cbar.set_label('Intensity')
    #ax1.axis("tight")

    plt.show()

def anglePlot(X, Y):
    fig, ax = plt.subplots(figsize=(16,10), dpi=80)
    ax.plot(X, Y, '-o', label='Pulsating torque', linewidth=1.0, markersize=5, color='blue')
    plt.ylabel("Amplitude [pu.]")
    plt.xlabel(r"Rotor angle ($\theta_{m}$)")
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    # Show [0, 2pi] instead of [0, 1] as pi is easier to understand
    labels = [0, 0, r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    ax.set_xticklabels(labels)

if __name__ == '__main__':

    data = np.load("captured_data.npy") # indices are shifted +1
    print("1", data[0][0:10])
    print("2", data[1][0:10])

    #data = data[:, 0:-100]
    #spectogram(data[0], data[1])
    anglePlot(data[0], data[1])
    plt.show()
