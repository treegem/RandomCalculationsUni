import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190716_pc_phase_oscillation_90mA'
    folders = ['5_1000', '5000_6000', '10000_11000', '15000_16000', '20000_21000', '25000_26000']

    for folder in folders:
        zs = np.loadtxt('{}_zs.txt'.format(folder))[12:-13]
        bins = np.loadtxt(os.path.join(base_path, folder, 'bins.txt'))
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
