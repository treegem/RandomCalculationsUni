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
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190221_d06_phase_oscillation/phase_oscillation_02'

    bins = np.loadtxt(os.path.join(path, 'bins.txt'))
    i_bins = bins_to_avg(bins)
    zs = np.loadtxt(os.path.join(path, 'zs.txt'))
    for i, entry in enumerate(zs):
        if entry > 0.955:
            zs[i] = 0.955
    plt.close('all')
    plt.plot(i_bins, zs)
    plt.ylim((0.92, 0.96))
    plt.savefig('z_vs_i.jpg', dpi=300)

    # freqs = np.fft.rfftfreq(len(bins), bins[-1] - bins[-2])
    ft_zs = np.fft.rfft(np.trim_zeros(zs))

    plt.close('all')
    plt.plot(abs(ft_zs[1:]))
    plt.savefig('z_vs_i_fft.jpg', dpi=300)


if __name__ == '__main__':
    main()
