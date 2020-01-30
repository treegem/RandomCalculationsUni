import os

import numpy as np
import scipy.io as sio

from utility.current_series_shared_functions import calc_vmin_vmax, plot_2d


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190819_noise_serieses/003_5.20_5.50_current_series'
    subfolders = os.listdir(path)

    zs_2d = None

    for i, subfolder in enumerate(subfolders):
        print(subfolder)
        start_index = 0
        end_index = -1

        zs = load_zs_taus(end_index, path, start_index, subfolder)

        if zs_2d is None:
            zs_2d = np.zeros((len(subfolders), len(zs)))

        zs_2d[i] = zs

    vmax, vmin = calc_vmin_vmax(zs_2d)

    name = 'current_series_taus.jpg'
    plot_2d(name, vmax, vmin, zs_2d)


def load_zs_taus(end_index, path, start_index, subfolder):
    j = 0
    zs = None
    while os.path.isfile(file_name(j, path, subfolder)):
        if j % 200 == 0:
            print('\r{:04}'.format(j), end='')
        mat_data_zs = sio.loadmat(file_name(j, path, subfolder))['zs'][0][start_index:end_index]
        if zs is None:
            zs = np.zeros(len(mat_data_zs))
        zs += mat_data_zs
        j += 1
    zs = zs / j
    print('')
    return zs


def file_name(j, path, subfolder):
    return os.path.join(path, subfolder, 'pulsed.{:03}.mat'.format(j))


if __name__ == '__main__':
    main()
