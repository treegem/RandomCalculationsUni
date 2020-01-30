import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


def main():
    folders = ['50_250_0', '800_1000_0', '1500_1700_0', '2200_2400_0', '2900_3100_0', '3600_3800_0']
    base_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190819_noise_serieses/001_50_4000_arti_noise'

    for folder in folders:

        path = os.path.join(base_path, folder)

        phase_zs = np.loadtxt(os.path.join(path, 'zs.txt'))

        plt.close('all')
        phase_start = None
        phase_end = None
        plt.plot(phase_zs[phase_start:phase_end])
        plt.savefig('{}_zs.jpg'.format(folder))

        taus = np.loadtxt(os.path.join(path, 'taus.txt'))[:-1]
        tau_zs = np.zeros_like(taus)
        pulsed_index = 0
        file_count = 0
        pulsed_name = combine_pulsed_name(path, pulsed_index)
        while os.path.isfile(pulsed_name):
            if file_count % 100 == 0:
                print(file_count)
            file_count += 1
            data = sio.loadmat(pulsed_name)
            tau_zs += data['z'][0][:-1]
            pulsed_index += 1
            pulsed_name = combine_pulsed_name(path, pulsed_index)
        tau_zs /= file_count
        plt.close('all')
        plt.plot(taus, tau_zs)
        plt.savefig('{}_reconstructed.jpg'.format(folder))
        np.savetxt('{}_tau_zs.txt'.format(folder), tau_zs)
        np.savetxt('{}_taus.txt'.format(folder), taus)
        np.savetxt('{}_zs.txt'.format(folder), phase_zs)


def combine_pulsed_name(path, pulsed_index):
    return os.path.join(path, 'pulsed.{:03}.mat'.format(pulsed_index))


if __name__ == '__main__':
    main()
