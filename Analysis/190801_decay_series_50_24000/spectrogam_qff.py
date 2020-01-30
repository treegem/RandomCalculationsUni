import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    base_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190801_decay_series_50_24000/002_decay_series_50_24000'
    folders = ['50_250', '5000_5200', '10000_10200', '15000_15200', '20000_20200', '23800_24000']

    for folder in folders:
        zs = np.loadtxt('{}_zs.txt'.format(folder))[12:-13]
        bins = np.loadtxt(os.path.join(base_path, folder, '{}_0'.format(folder), 'bins.txt'))
        bin_steps = bins[1] - bins[0]
        fs = 1  # / bin_steps

        f, t, Sxx = signal.spectrogram(zs, fs=fs, nperseg=int(len(zs) / 1))
        plt.close('all')
        # plt.pcolormesh(t, f, Sxx)
        plt.imshow(Sxx)
        plt.savefig('{}_spectrogram_qff.jpg'.format(folder), dpi=300)
        np.savetxt('{}_sxx_qff.txt'.format(folder), Sxx)


if __name__ == '__main__':
    main()
