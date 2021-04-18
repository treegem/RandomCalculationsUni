import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190226_d06_gradient_sweep'
    n_pulses = 100
    ch2_currents = np.zeros(n_pulses)

    for i in range(1, 101):
        print('i :', i)
        pulsed_file = '002_gradient_sweep/pulsed_{:06}.mat'.format(i)
        data = loadmat(os.path.join(path, pulsed_file))
        taus = data['taus'][0]
        zs = data['zs']

        fft_and_plots(taus, zs, 'taus', i)

        pulse_form_files = [
            'current_pulses/analogue_data_ch1_{}.txt'.format(i),
            'current_pulses/analogue_data_ch2_{}.txt'.format(i)
        ]

        if not os.path.isfile('gradient_sweep/integrated_currents_ch1_{:03}.txt'.format(i)):
            integrated_currents, ch2_current = integrate_currents(path, pulse_form_files, i)
            ch2_currents[i - 1] = ch2_current
        else:
            integrated_currents = np.loadtxt('gradient_sweep/integrated_currents_ch1_{:03}.txt'.format(i))
            ch2_currents = np.loadtxt('gradient_sweep/ch2_currents.txt')
            print('loaded integrated currents from file')

        xs = np.linspace(integrated_currents[0], integrated_currents[-1], n_pulses)
        interp_zs = np.array([np.interp(xs, integrated_currents, zs[0]), np.interp(xs, integrated_currents, zs[1])])

        fft_and_plots(xs=xs, zs=interp_zs, name='interp_currents', i=i)
    np.savetxt('gradient_sweep/ch2_currents.txt', ch2_currents)


def integrate_currents(path, pulse_form_files, i):
    n_sweeps = 1000
    data = []
    for j in range(len(pulse_form_files)):
        data.append(np.loadtxt(os.path.join(path, pulse_form_files[j])) / n_sweeps)
    ch1_data = data[0]
    ch2_data = data[1]
    window_length = 4096
    ch1_offset = np.average(ch1_data[window_length - 100:window_length])
    ch2_offset = np.average(ch2_data[window_length - 100:window_length])
    ch1_data -= ch1_offset
    ch2_data -= ch2_offset
    n_windows = int(len(ch1_data) / window_length)
    integrated_currents_ch1 = np.zeros(n_windows)
    integrated_currents_ch2 = np.zeros(n_windows)
    for j in range(n_windows):
        integrated_currents_ch1[j] = np.sum(ch1_data[j * window_length:(j + 1) * window_length])
        integrated_currents_ch2[j] = np.sum(ch2_data[j * window_length:(j + 1) * window_length])
    averaged_currents = np.zeros(int(integrated_currents_ch1.shape[0] / 2))
    averaged_ch2 = np.average(integrated_currents_ch2)
    for j in range(averaged_currents.shape[0]):
        averaged_currents[j] = np.average(integrated_currents_ch1[j * 2:(j + 1) * 2])
    np.savetxt('gradient_sweep/integrated_currents_ch1_{:03}.txt'.format(i), averaged_currents)
    return averaged_currents, averaged_ch2


def fft_and_plots(xs, zs, name, i):
    plt.close('all')
    plt.plot(xs, zs[0])
    plt.plot(xs, zs[1])
    plt.savefig('gradient_sweep/both_{}_{}.jpg'.format(name, i), dpi=300)
    plt.close('all')
    plt.plot(xs, zs[0] - zs[1])
    np.savetxt('gradient_sweep/difference_{}_{}.txt'.format(name, i), zs[0] - zs[1])
    plt.savefig('gradient_sweep/difference_{}_{}.jpg'.format(name, i), dpi=300)
    freqs = np.fft.rfftfreq(len(xs), xs[-1] - xs[-2])
    fft_zs = np.fft.rfft(zs[0] - zs[1])
    plt.close('all')
    plt.plot(freqs[1:], abs(fft_zs[1:]))
    plt.savefig('gradient_sweep/fft_{}_{}.jpg'.format(name, i), dpi=300)


if __name__ == '__main__':
    main()
