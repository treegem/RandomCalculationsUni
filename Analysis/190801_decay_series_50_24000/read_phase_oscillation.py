import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


def main():
    folders = ['50_250', '5000_5200', '10000_10200', '15000_15200', '20000_20200', '23800_24000']
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190801_decay_series_50_24000/002_decay_series_50_24000'

    for folder in folders:

        path = os.path.join(base_path, folder)

        sub_folders = os.listdir(path)
        if folder == '50_250':
            sub_folders.pop(1)
        phase_zs = None
        for i, sub_folder in enumerate(sub_folders):

            sub_folder_path = os.path.join(path, sub_folder)
            if phase_zs is None:
                phase_zs = np.loadtxt(os.path.join(sub_folder_path, 'zs.txt'))
            else:
                phase_zs += np.loadtxt(os.path.join(sub_folder_path, 'zs.txt'))
        phase_zs = phase_zs / len(sub_folders)

        plt.close('all')
        phase_start = None
        phase_end = None
        plt.plot(phase_zs[phase_start:phase_end])
        plt.savefig('{}_zs.jpg'.format(folder))

        tau_zs = None
        for sub_folder in sub_folders:
            sub_folder_path = os.path.join(path, sub_folder)
            taus = np.loadtxt(os.path.join(sub_folder_path, 'taus.txt'))[:-1]
            if tau_zs is None:
                tau_zs = np.zeros_like(taus)
            pulsed_index = 0
            file_count = 0
            pulsed_name = combine_pulsed_name(sub_folder_path, pulsed_index)
            while os.path.isfile(pulsed_name):
                if file_count % 100 == 0:
                    print(file_count)
                file_count += 1
                data = sio.loadmat(pulsed_name)
                tau_zs += data['z'][0][:-1]
                pulsed_index += 1
                pulsed_name = combine_pulsed_name(sub_folder_path, pulsed_index)
        tau_zs /= (file_count * len(sub_folders))
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
