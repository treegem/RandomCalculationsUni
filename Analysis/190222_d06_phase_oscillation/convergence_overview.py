import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    source_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190222_d06_phase_oscillation/phase_oscillation_002'
    for i in range(30):
        pulsed_file = 'pulsed.{:03}.mat'.format(i)
        data = loadmat(os.path.join(source_path, pulsed_file))
        taus = data['taus'][0]
        zs = data['zs']

        fft_and_plots(taus, zs, i)


def fft_and_plots(xs, zs, name):
    plt.close('all')
    plt.plot(xs, zs[0])
    plt.plot(xs, zs[1])
    plt.savefig('convergence_overview/both_{:03}.jpg'.format(name), dpi=300)
    plt.close('all')
    plt.plot(xs, zs[0] - zs[1])
    plt.savefig('convergence_overview/difference_{:03}.jpg'.format(name), dpi=300)
    freqs = np.fft.rfftfreq(len(xs), xs[-1] - xs[-2])
    fft_zs = np.fft.rfft(zs[0] - zs[1])
    plt.close('all')
    plt.plot(freqs[1:], abs(fft_zs[1:]))
    plt.savefig('convergence_overview/fft_{:03}.jpg'.format(name), dpi=300)


if __name__ == '__main__':
    main()
