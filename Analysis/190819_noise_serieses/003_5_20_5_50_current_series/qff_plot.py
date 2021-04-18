import os

import numpy as np

from utility.current_series_shared_functions import calc_vmin_vmax, plot_2d


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190819_noise_serieses/003_5.20_5.50_current_series'
    subfolders = os.listdir(path)

    zs_2d = None

    for i, subfolder in enumerate(subfolders):
        start_index = 0
        end_index = None

        zs = load_zs_qff(start_index, end_index, path, subfolder)

        if zs_2d is None:
            zs_2d = np.zeros((len(subfolders), len(zs)))

        zs_2d[i] = zs

    vmax, vmin = calc_vmin_vmax(zs_2d)

    name = 'current_series_qff.jpg'
    plot_2d(name, vmax, vmin, zs_2d)


def load_zs_qff(start_index, end_index, path, subfolder):
    zs = np.loadtxt(os.path.join(path, subfolder, 'zs.txt'))[start_index:end_index]
    return zs


if __name__ == '__main__':
    main()
