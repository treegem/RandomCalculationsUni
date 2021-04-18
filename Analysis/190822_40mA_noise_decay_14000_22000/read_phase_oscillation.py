import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


def main():
    folders = ['14000_14400', '16000_16400', '18000_18400', '20000_20400', '22000_22400']
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190822_noise_decay_series_14000_22000/' \
                '000_noise_decay_series_14000_22000'

    for folder in folders:
        print(folder)

        path = os.path.join(base_path, folder)
        subfolders = os.listdir(path)

        phase_zs = None
        for subfolder in subfolders:
            print(subfolder)
            phase_zs_sub = np.loadtxt(os.path.join(path, subfolder, 'zs.txt'))

            if phase_zs is None:
                phase_zs = np.zeros(len(phase_zs_sub))

            phase_zs += phase_zs_sub
        phase_zs = phase_zs / len(subfolders)

        plt.close('all')
        phase_start = None
        phase_end = None
        plt.plot(phase_zs[phase_start:phase_end])
        plt.savefig('{}_zs.jpg'.format(folder))

        taus = np.loadtxt(os.path.join(path, subfolder, 'taus.txt'))[:-1]
        tau_zs = np.zeros_like(taus)

        for subfolder in subfolders:
            print(subfolder)
            tau_zs_sub = np.zeros_like(taus)
            pulsed_index = 0
            file_count = 0
            pulsed_name = combine_pulsed_name(os.path.join(path, subfolder), pulsed_index)
            while os.path.isfile(pulsed_name):
                if file_count % 100 == 0:
                    print('\r{}'.format(file_count), end='')
                file_count += 1
                data = sio.loadmat(pulsed_name)
                tau_zs_sub += data['z'][0][:-1]
                pulsed_index += 1
                pulsed_name = combine_pulsed_name(os.path.join(path, subfolder), pulsed_index)
            print('')
            tau_zs_sub /= file_count
            tau_zs += tau_zs_sub
        tau_zs /= len(subfolders)

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
