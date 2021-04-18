import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190723_pc_90mA_stability_test_new_ic'
    stability_check(base_path, '15000_15200_series_1')


def stability_check(base_path, folder):
    full_path = os.path.join(base_path, folder)
    sub_folders = os.listdir(full_path)
    for i, sub_folder in enumerate(sub_folders):
        if i % 5 == 0:
            print(i)
        recorded = np.loadtxt(os.path.join(full_path, sub_folder, 'recorded_bin.txt'))
        if i == 0:
            recorded_2ds = np.zeros((len(sub_folders), len(recorded)))
        recorded_2ds[i] = recorded

    plt.close('all')
    plt.imshow(recorded_2ds, aspect='auto')
    plt.colorbar()
    plt.savefig('recorded_{}.png'.format(folder), dpi=300)

    plt.close('all')
    high_values = recorded_2ds[np.where(recorded_2ds > -2e7)]
    vmin = high_values.min()
    vmax = recorded_2ds.max()
    plt.imshow(recorded_2ds, vmin=vmin, vmax=vmax, aspect='auto')
    plt.colorbar()
    plt.savefig('recorded_cropped_{}.png'.format(folder), dpi=300)


if __name__ == '__main__':
    main()
