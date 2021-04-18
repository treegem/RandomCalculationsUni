import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190717_pc_phase_oscillation_90mA_stability_test'
    stability_check(base_path, '200e3_sweeps')
    stability_check(base_path, '500e3_sweeps')


def stability_check(base_path, folder):
    full_path = os.path.join(base_path, folder)
    sub_folders = os.listdir(full_path)
    for i, sub_folder in enumerate(sub_folders):
        zs = np.loadtxt(os.path.join(full_path, sub_folder, 'zs.txt'))
        if i == 0:
            zs_2d = np.zeros((len(sub_folders), len(zs)))
        zs_2d[i] = zs
    plt.close('all')
    plt.imshow(zs_2d, vmin=zs_2d[:, 10:-10].min(), vmax=zs_2d[:, 10:-10].max())
    plt.colorbar()
    plt.savefig('{}.png'.format(folder), dpi=300)


if __name__ == '__main__':
    main()
