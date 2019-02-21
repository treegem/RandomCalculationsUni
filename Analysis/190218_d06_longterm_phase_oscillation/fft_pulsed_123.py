import os

import scipy.io as sio
import matplotlib.pyplot as plt
import numpy.fft as fft


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190218_d06_longterm_phase_oscillation'
    index = 123
    file = 'pulsed.{}.mat'.format(index)
    taus, zs = load_data(file, path)

    plot_pulsed(taus, zs, index)

    fft_taus, fft_zs = calc_fft(taus, zs)

    plot_fft(fft_taus, fft_zs, index)


def plot_fft(fft_taus, fft_zs, index):
    plt.close('all')
    plt.plot(fft_taus[1:], abs(fft_zs[1:]))
    plt.savefig('fft_pulsed_{}.jpg'.format(index))


def calc_fft(taus, zs):
    fft_zs = fft.rfft(zs)
    fft_taus = fft.rfftfreq(n=len(taus), d=(taus[-1] - taus[-2]) * 1e-9)
    return fft_taus, fft_zs


def plot_pulsed(taus, zs, index):
    plt.close('all')
    plt.plot(taus, zs)
    plt.savefig('pulsed_{}.jpg'.format(index), dpi=300)
    # plt.show()


def load_data(file, path):
    data = sio.loadmat(os.path.join(path, file))
    taus = data['taus'][0]
    zs = data['zs'][0]
    return taus, zs


if __name__ == '__main__':
    main()
