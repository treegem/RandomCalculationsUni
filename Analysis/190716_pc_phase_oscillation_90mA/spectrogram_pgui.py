import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    base_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190716_pc_phase_oscillation_90mA'
    folders = ['5_1000', '5000_6000', '10000_11000', '15000_16000', '20000_21000', '25000_26000']
    for folder in folders:
        zs = np.loadtxt('{}_tau_zs.txt'.format(folder))[12:-13]
        taus = np.loadtxt('{}_taus.txt'.format(folder))
        tau_steps = taus[1] - taus[0]
        fs = 1 #/ tau_steps

        f, t, Sxx = signal.spectrogram(zs, fs=fs, nperseg=int(len(zs) / 1))
        plt.close('all')
        # plt.pcolormesh(t, f, Sxx)
        plt.imshow(Sxx)
        plt.savefig('{}_spectrogram_tau.jpg'.format(folder), dpi=300)
        np.savetxt('{}_sxx_tau.txt'.format(folder), Sxx)


if __name__ == '__main__':
    main()
