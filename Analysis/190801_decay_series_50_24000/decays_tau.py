import matplotlib.pyplot as plt
import numpy as np


# WARNING
# This is only for single values in the Spectrogram. So for a single window that has been analyzed.

def main():
    folders = ['50_250', '5000_5200', '10000_10200', '15000_15200', '20000_20200', '23800_24000']
    sxx = []
    for folder in folders:
        sxx.append(np.loadtxt('{}_sxx_tau.txt'.format(folder)))

    i_maxs = [[1, 2], [1, 2], [1, 2], [1, 2], [2, 3], [1, 2]]
    decay_signals = []
    for i_max, sx in zip(i_maxs, sxx):
        decay_signal = sx[i_max[0]:i_max[1] + 1]
        decay_signal = decay_signal.sum(axis=0)
        decay_signals.append(decay_signal)
    plt.close('all')
    plt.plot(decay_signals)
    plt.show()
    np.savetxt('decays_tau.txt', decay_signals)


if __name__ == '__main__':
    main()
