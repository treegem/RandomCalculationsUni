import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    folders = ['50_250_0', '2000_2200_0', '4000_4200_0', '6000_6200_0', '8000_8200_0', '10000_10200_0']
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190814_artificial_noise_50_10000/000_artificial_noise'

    for folder in folders:
        zs = np.loadtxt('{}_zs.txt'.format(folder))[5:-18]

        # ### REMOVE FOR NEW MEASUREMENT
        # if folder == '2000_2200_0':
        #     zs = np.loadtxt('{}_zs.txt'.format(folder))[5:-18]
        # ### REMOVE

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
