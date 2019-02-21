import os

import scipy.io as sio
import matplotlib.pyplot as plt


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190219_d06_longterm_windowed_phase'
    file_name = 'pulsed.007.mat'
    data = sio.loadmat(os.path.join(path, file_name))
    zs = data['zs'][0]
    taus = data['taus'][0]

    window_length = 20
    n_windows = len(taus) / window_length

    for i in range(int(n_windows)):
        taus_window = taus[i * window_length:(i + 1) * window_length]
        zs_window = zs[i * window_length:(i + 1) * window_length]
        plt.close('all')
        plt.plot(taus_window, zs_window)
        plt.savefig('window_{}.jpg'.format(taus_window[0]))


if __name__ == '__main__':
    main()
