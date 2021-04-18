import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    folders = ['50_250_0', '5000_5200_0', '10000_10200_0', '15000_15200_0', '20000_20200_0', '25000_25200_0']
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190813_artificial_noise/000_50_25000_artificial_noise'

    for folder in folders:
        zs = np.loadtxt('{}_tau_zs.txt'.format(folder))[10:-5]
        taus = np.loadtxt('{}_taus.txt'.format(folder))
        tau_steps = taus[1] - taus[0]
        fs = 1 #/ tau_steps

        f, t, Sxx = signal.spectrogram(zs, fs=fs, nperseg=int(len(zs) / 1))
        plt.close('all')
        plt.imshow(Sxx, aspect='auto')
        plt.savefig('{}_spectrogram_tau.jpg'.format(folder), dpi=300)
        np.savetxt('{}_sxx_tau.txt'.format(folder), Sxx)


if __name__ == '__main__':
    main()
