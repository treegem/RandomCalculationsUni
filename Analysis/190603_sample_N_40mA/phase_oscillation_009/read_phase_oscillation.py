import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190603_sample_N_40mA/phase_oscillation_009'

    phase_zs = np.loadtxt(os.path.join(path, 'zs.txt'))

    plt.close('all')
    phase_start = 0
    phase_end = None
    plt.plot(phase_zs[phase_start:phase_end])
    plt.show()

    taus = np.loadtxt(os.path.join(path, 'taus.txt'))
    tau_zs = np.zeros_like(taus)
    pulsed_index = 46
    file_count = 0
    pulsed_name = combine_pulsed_name(path, pulsed_index)
    while os.path.isfile(pulsed_name):
        if file_count % 100 == 0:
            print(file_count)
        file_count += 1
        data = sio.loadmat(pulsed_name)
        tau_zs += data['z'][0]
        pulsed_index += 1
        pulsed_name = combine_pulsed_name(path, pulsed_index)
    tau_zs /= file_count
    plt.close('all')
    plt.plot(taus, tau_zs)
    plt.show()


def combine_pulsed_name(path, pulsed_index):
    return os.path.join(path, 'pulsed.{:03}.mat'.format(pulsed_index))


if __name__ == '__main__':
    main()
