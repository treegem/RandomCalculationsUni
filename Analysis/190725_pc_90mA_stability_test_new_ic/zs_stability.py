import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    base_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190725_pc_90mA_stability_test_new_ic'
    stability_check(base_path, '20000_20200_series_0')


def stability_check(base_path, folder):
    full_path = os.path.join(base_path, folder)
    sub_folders = os.listdir(full_path)
    for i, sub_folder in enumerate(sub_folders):
        zs = np.loadtxt(os.path.join(full_path, sub_folder, 'zs.txt'))
        if i == 0:
            zs_2d = np.zeros((len(sub_folders), len(zs)))
        zs_2d[i] = zs
    plt.close('all')
    plt.imshow(zs_2d, vmin=zs_2d[:5, 10:-10].min(), vmax=zs_2d[:5, 10:-10].max())
    plt.colorbar()
    plt.savefig('{}.png'.format(folder), dpi=300)


if __name__ == '__main__':
    main()
