import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    base_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190717_pc_phase_oscillation_90mA_stability_test'
    stability_check(base_path, '200e3_sweeps')
    stability_check(base_path, '500e3_sweeps')


def stability_check(base_path, folder):
    full_path = os.path.join(base_path, folder)
    sub_folders = os.listdir(full_path)
    for i, sub_folder in enumerate(sub_folders):
        if i % 5 == 0:
            print(i)
        reference = np.loadtxt(os.path.join(full_path, sub_folder, 'reference_bin.txt'))
        if i == 0:
            reference_2ds = np.zeros((len(sub_folders), len(reference)))
        reference_2ds[i] = reference

    plt.close('all')
    plt.imshow(reference_2ds, aspect='auto')
    plt.colorbar()
    plt.savefig('reference_{}.png'.format(folder), dpi=300)
    
    plt.close('all')
    vmin = reference_2ds.min()
    low_values = reference_2ds[np.where(reference_2ds < -2e7)]
    vmax = low_values.max()
    plt.imshow(reference_2ds, vmin=vmin, vmax=vmax, aspect='auto')
    plt.colorbar()
    plt.savefig('reference_cropped_{}.png'.format(folder), dpi=300)


if __name__ == '__main__':
    main()
