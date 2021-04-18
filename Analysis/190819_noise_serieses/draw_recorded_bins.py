import os

import numpy as np
import matplotlib.pyplot as plt


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190819_noise_serieses/003_5.20_5.50_current_series'
    subfolders = os.listdir(path)

    recorded_bins = np.zeros(len(subfolders))
    reference_bins = np.zeros(len(subfolders))

    for i, subfolder in enumerate(subfolders):
        print(subfolder)
        full_path = os.path.join(path, subfolder)

        recorded_bin = np.average(np.loadtxt(os.path.join(full_path, 'recorded_bin.txt')))
        reference_bin = np.average(np.loadtxt(os.path.join(full_path, 'reference_bin.txt')))

        recorded_bins[i] = recorded_bin
        reference_bins[i] = reference_bin

    plt.close('all')
    plt.plot(recorded_bins)
    plt.savefig('recorded_bins.jpg', dpi=300)

    plt.close('all')
    plt.plot(reference_bins)
    plt.savefig('reference_bins.jpg', dpi=300)


if __name__ == '__main__':
    main()
