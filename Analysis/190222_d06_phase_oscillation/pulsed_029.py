import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190222_d06_phase_oscillation'
    pulsed_file = 'phase_oscillation_002/pulsed.029.mat'
    data = loadmat(os.path.join(path, pulsed_file))
    taus = data['taus'][0]
    zs = data['zs']

    fft_and_plots(taus, zs, 'taus')

    pulse_form_file = 'analogue_data_1000.txt'
    if not os.path.isfile('integrated_currents.txt'):
        integrated_currents = integrate_currents(path, pulse_form_file)
    else:
        integrated_currents = np.loadtxt('integrated_currents.txt')
        print('loaded integrated currents from file')

    plt.close('all')
    plt.plot(taus, integrated_currents)
    plt.savefig('taus_vs_is.jpg', dpi=300)

    xs = np.linspace(integrated_currents[0], integrated_currents[-1], 500)
    interp_zs = np.array([np.interp(xs, integrated_currents, zs[0]), np.interp(xs, integrated_currents, zs[1])])

    fft_and_plots(xs=xs, zs=interp_zs, name='interp_currents')


def integrate_currents(path, pulse_form_file):
    n_sweeps = 1000
    data = np.loadtxt(os.path.join(path, pulse_form_file)) / n_sweeps
    window_length = 4096
    offset = np.average(data[window_length - 100:window_length])
    data -= offset
    n_windows = int(len(data) / window_length)
    integrated_currents = np.zeros(n_windows)
    for i in range(n_windows):
        integrated_currents[i] = np.sum(data[i * window_length:(i + 1) * window_length])
    np.savetxt('integrated_currents.txt', integrated_currents)
    return integrated_currents


def fft_and_plots(xs, zs, name):
    plt.close('all')
    plt.plot(xs, zs[0])
    plt.plot(xs, zs[1])
    plt.savefig('both_{}.jpg'.format(name), dpi=300)
    plt.close('all')
    plt.plot(xs, zs[0] - zs[1])
    plt.savefig('difference_{}.jpg'.format(name), dpi=300)
    freqs = np.fft.rfftfreq(len(xs), xs[-1] - xs[-2])
    fft_zs = np.fft.rfft(zs[0] - zs[1])
    plt.close('all')
    plt.plot(freqs[1:], abs(fft_zs[1:]))
    plt.savefig('fft_{}.jpg'.format(name), dpi=300)


if __name__ == '__main__':
    main()
