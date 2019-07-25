import os

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    base_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190715_pc_phase_oscillation_decay'
    folders = ['002_phase_oscillation_5_5000', '004_phase_oscillation_5000_15000', '15000_20000', '20000_25000',
               '25000_30000', '25000_30000_2']
    for folder in folders:
        zs = np.loadtxt('{}_tau_zs.txt'.format(folder))[12:-13]
        taus = np.loadtxt('{}_taus.txt'.format(folder))
        tau_steps = taus[1] - taus[0]
        fs = 1 #/ tau_steps

        f, t, Sxx = signal.spectrogram(zs, fs=fs, nperseg=25)
        plt.close('all')
        plt.pcolormesh(t, f, Sxx)
        plt.savefig('{}_spectrogram_tau.jpg'.format(folder), dpi=300)
        np.savetxt('{}_sxx_tau.txt'.format(folder), Sxx)


if __name__ == '__main__':
    main()
