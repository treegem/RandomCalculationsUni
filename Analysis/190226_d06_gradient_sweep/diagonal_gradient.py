import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190226_d06_gradient_sweep'
    pulsed_file = '002_gradient_sweep/pulsed_000000.mat'
    data = loadmat(os.path.join(path, pulsed_file))
    taus = data['taus'][0]
    zs = data['zs']

    np.savetxt('diagonal_gradient/taus.txt', taus)
    np.savetxt('diagonal_gradient/zs.txt', zs)

    fft_and_plots(taus, zs, 'taus')

    pulse_form_files = [
        'current_pulses/analogue_data_ch1_0_part1.txt',
        'current_pulses/analogue_data_ch1_0_part2.txt',
        'current_pulses/analogue_data_ch2_0_part1.txt',
        'current_pulses/analogue_data_ch2_0_part2.txt'
    ]

    if not os.path.isfile('diagonal_gradient/integrated_currents.txt'):
        integrated_currents = integrate_currents(path, pulse_form_files)
    else:
        integrated_currents = np.loadtxt('diagonal_gradient/integrated_currents.txt')
        print('loaded integrated currents from file')
    print(integrated_currents.shape)
    plt.close('all')
    plt.plot(taus, integrated_currents)
    plt.savefig('diagonal_gradient/taus_vs_is.jpg', dpi=300)

    xs = np.linspace(integrated_currents[0], integrated_currents[-1], 250)
    interp_zs = np.array([np.interp(xs, integrated_currents, zs[0]), np.interp(xs, integrated_currents, zs[1])])
    np.savetxt('diagonal_gradient/interp_currents.txt', xs)
    np.savetxt('diagonal_gradient/interp_zs.txt', interp_zs)

    fft_and_plots(xs=xs, zs=interp_zs, name='interp_currents')


def integrate_currents(path, pulse_form_files):
    n_sweeps = 1000
    data = []
    for i in range(len(pulse_form_files)):
        data.append(np.loadtxt(os.path.join(path, pulse_form_files[i])) / n_sweeps)
    ch1_data = np.hstack((data[0], data[1]))
    ch2_data = np.hstack((data[2], data[3]))
    ch1_offset = np.average(ch1_data[4096 - 100:4096])
    ch2_offset = np.average(ch2_data[4096 - 100:4096])
    ch1_data -= ch1_offset
    ch2_data -= ch2_offset
    data = ch1_data + ch2_data
    window_length = 4096
    n_windows = int(len(data) / window_length)
    integrated_currents = np.zeros(n_windows)
    for i in range(n_windows):
        integrated_currents[i] = np.sum(data[i * window_length:(i + 1) * window_length])
    averaged_currents = np.zeros(int(integrated_currents.shape[0] / 2))
    for i in range(averaged_currents.shape[0]):
        averaged_currents[i] = np.average(integrated_currents[i * 2:(i + 1) * 2])
    np.savetxt('diagonal_gradient/integrated_currents.txt', averaged_currents)
    return averaged_currents


def fft_and_plots(xs, zs, name):
    plt.close('all')
    plt.plot(xs, zs[0])
    plt.plot(xs, zs[1])
    plt.savefig('diagonal_gradient/both_{}.jpg'.format(name), dpi=300)
    plt.close('all')
    plt.plot(xs, zs[0] - zs[1])
    plt.savefig('diagonal_gradient/difference_{}.jpg'.format(name), dpi=300)
    freqs = np.fft.rfftfreq(len(xs), xs[-1] - xs[-2])
    fft_zs = np.fft.rfft(zs[0] - zs[1])
    plt.close('all')
    plt.plot(freqs[1:], abs(fft_zs[1:]))
    plt.savefig('diagonal_gradient/fft_{}.jpg'.format(name), dpi=300)
    np.savetxt('diagonal_gradient/fft_{}.txt'.format(name), fft_zs)
    np.savetxt('diagonal_gradient/freqs_{}.txt'.format(name), freqs)


if __name__ == '__main__':
    main()
