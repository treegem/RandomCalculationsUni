import matplotlib.pyplot as plt
import numpy as np


# WARNING
# This is only for single values in the Spectrogram. So for a single window that has been analyzed.

def main():
    folders = ['5_1000', '5000_6000', '10000_11000', '15000_16000', '20000_21000', '25000_26000']
    sxx = []
    for folder in folders:
        sxx.append(np.loadtxt('{}_sxx_tau.txt'.format(folder)))

    i_maxs = [[9, 11], [14, 16], [15, 17], [15, 17], [15, 17], [15, 17]]
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
