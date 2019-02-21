import os

import matplotlib.pyplot as plt
import numpy as np


def bins_to_avg(bins):
    avgs = np.zeros(len(bins) - 1)
    for i, _ in enumerate(bins):
        if i == len(bins) - 1:
            break
        avgs[i] = (bins[i] + bins[i + 1]) / 2
    return avgs


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190221_d06_phase_oscillation/phase_oscillation_02'

    bins = np.loadtxt(os.path.join(path, 'bins.txt'))
    i_bins = bins_to_avg(bins)
    zs = np.loadtxt(os.path.join(path, 'zs.txt'))
    plt.close('all')
    plt.plot(i_bins, zs)
    plt.ylim((0.92, 0.96))
    plt.savefig('z_vs_i.jpg', dpi=300)

    freqs = np.fft.rfftfreq(len(bins), bins[-1] - bins[-2])
    ft_zs = np.fft.rfft(zs)

    plt.close('all')
    plt.plot(freqs[1:], abs(ft_zs[1:]))
    plt.savefig('z_vs_i_fft.jpg', dpi=300)


if __name__ == '__main__':
    main()
