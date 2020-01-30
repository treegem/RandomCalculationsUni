import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    folders = ['50_250_0', '5000_5200_0', '10000_10200_0', '15000_15200_0', '20000_20200_0', '25000_25200_0']
    base_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190813_artificial_noise/000_50_25000_artificial_noise'

    for folder in folders:
        zs = np.loadtxt('{}_zs.txt'.format(folder))[10:-5]
        bins = np.loadtxt(os.path.join(base_path, folder, 'bins.txt'))
        bin_steps = bins[1] - bins[0]
        fs = 1  # / bin_steps

        f, t, Sxx = signal.spectrogram(zs, fs=fs, nperseg=int(len(zs) / 1))
        plt.close('all')
        # plt.pcolormesh(t, f, Sxx)
        plt.imshow(Sxx, aspect='auto')
        plt.savefig('{}_spectrogram_qff.jpg'.format(folder), dpi=300)
        np.savetxt('{}_sxx_qff.txt'.format(folder), Sxx)


if __name__ == '__main__':
    main()
