import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

color2 = '#e15129'
color1 = '#0896d3'
#color2 = '#69c386'

# Double y-axis (torque-speed plotter)
def lineChart2(times, signal1, signal2, ax=None, dpi=80, signal1_ylabel="signal1", signal2_ylabel="signal2"):
    
    if ax is None:
        fig, ax1 = plt.subplots(figsize=(16,10), dpi=dpi)
    else:
        ax1 = ax

    #color1 = 'royalblue'
    ax1.set_ylabel(signal1_ylabel, color=color1, fontsize=20, labelpad=30)
    ax1.set_xlabel("Time [s]", fontsize=20, labelpad=20)
    d1 = ax1.plot(times, signal1, linewidth=1.0, color=color1, alpha=0.8)
    #ax1.set(ylim=(110, 170))
    ax1.tick_params(axis='y', labelcolor=color1, labelsize=14)

    #color2 = 'indianred'
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel(signal2_ylabel, color=color2, fontsize=20, labelpad=30)  # we already handled the x-label with ax1
    #ax2.set(ylim=(199.4, 200.6))
    d3 = ax2.plot(times, signal2, linewidth=1.0, color=color2, alpha=0.8)
    ax2.tick_params(axis='y', labelcolor=color2, labelsize=14)
    #tick_spacing = 0.2
    #ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    #fig.tight_layout()  # otherwise the right y-label is slightly clipped    

    ax2.spines['right'].set_color(color2)
    ax2.spines['left'].set_color(color1)
    ax2.spines['top'].set_color('silver')
    ax2.spines['bottom'].set_color('silver')

    # Create legend
    #lns = d1+d3
    #labs = [l.get_label() for l in lns]
    #ax1.legend(lns, labs, loc='lower center', ncol=3, fontsize=14)
    return