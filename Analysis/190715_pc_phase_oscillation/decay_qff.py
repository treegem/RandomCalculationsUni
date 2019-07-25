import matplotlib.pyplot as plt
import numpy as np


def main():
    folders = ['002_phase_oscillation_5_5000', '004_phase_oscillation_5000_15000', '15000_20000', '20000_25000',
               '25000_30000']
    sxx = []
    for folder in folders:
        sxx.append(np.loadtxt('{}_sxx_qff.txt'.format(folder)))

    i_maxs = [[3, 4], [5, 6], [6, 7], [6, 7], [6, 7]]
    decay_signals = []
    for i_max, sx in zip(i_maxs, sxx):
        i_max = np.argmax(sx[:, 0])
        print(i_max)
        decay_signal = sx[i_max[0]:i_max[1] + 1, :]
        decay_signal = decay_signal.sum(axis=0)
        decay_signals.extend(decay_signal)
    plt.close('all')
    plt.plot(decay_signals)
    plt.show()
    np.savetxt('decays_qff.txt', decay_signals)


if __name__ == '__main__':
    main()
