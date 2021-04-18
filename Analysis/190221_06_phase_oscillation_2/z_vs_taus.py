import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190221_d06_phase_oscillation_2/phase_oscillation_001'
    start_index = 0
    end_index = 2264

    taus = np.loadtxt(os.path.join(path, 'taus.txt'))
    zs = np.zeros_like(taus)

    for i in range(start_index, end_index + 1):
        if i % 100 == 0:
            print(i)
        full_path = os.path.join(path, 'pulsed.{:03}.mat'.format(i))
        data = loadmat(full_path)
        zs += data['zs'][0]

    zs /= end_index - start_index + 1

    plt.close('all')
    plt.plot(taus, zs)
    plt.savefig('z_vs_taus.jpg', dpi=300)

    freqs = np.fft.rfftfreq(len(taus), taus[-1] - taus[-2])
    ft_zs = np.fft.rfft(zs)
    plt.close('all')
    plt.plot(freqs[1:], abs(ft_zs[1:]))
    plt.savefig('z_vs_taus_fft.jpg', dpi=300)


if __name__ == '__main__':
    main()
