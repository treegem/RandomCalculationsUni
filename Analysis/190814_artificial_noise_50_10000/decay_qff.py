import matplotlib.pyplot as plt
import numpy as np


# WARNING
# This is only for single values in the Spectrogram. So for a single window that has been analyzed.

def main():
    folders = ['50_250_0', '2000_2200_0', '4000_4200_0', '6000_6200_0', '8000_8200_0', '10000_10200_0']
    sxx = []
    for folder in folders:
        sxx.append(np.loadtxt('{}_sxx_qff.txt'.format(folder)))

    i_maxs = [[0, 3], [1, 4], [1, 4], [1, 4], [1, 4], [1, 4]]
    decay_signals = []
    for i_max, sx in zip(i_maxs, sxx):
        decay_signal = sx[i_max[0]:i_max[1] + 1]
        decay_signal = decay_signal.sum(axis=0)
        decay_signals.append(decay_signal)
    plt.close('all')
    plt.plot(decay_signals)
    plt.show()
    np.savetxt('decays_qff.txt', decay_signals)


if __name__ == '__main__':
    main()
