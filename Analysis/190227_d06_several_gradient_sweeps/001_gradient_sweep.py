import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    sub_folder = '001_gradient_sweep'
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190227_d06_several_gradient_sweeps/{}'.format(sub_folder)
    pulsed_file = 'pulsed.009.mat'
    data = loadmat(os.path.join(path, pulsed_file))
    taus = data['taus'][0]
    zs = data['zs']

    np.savetxt('{}/taus.txt'.format(sub_folder), taus)
    np.savetxt('{}/zs.txt'.format(sub_folder), zs)

    fft_and_plots(taus, zs, 'taus', sub_folder=sub_folder)

    pulse_form_files = [
        'analogue_data_ch1.txt',
        'analogue_data_ch2.txt'
    ]

    if not os.path.isfile('{}/integrated_currents.txt'.format(sub_folder)):
        window_length = 4096
        integrated_currents = integrate_currents(path, pulse_form_files, sub_folder, window_length)
    else:
        integrated_currents = np.loadtxt('{}/integrated_currents.txt'.format(sub_folder))
        print('loaded integrated currents from file')
    print(integrated_currents.shape)
    plt.close('all')
    plt.plot(taus, integrated_currents)
    plt.savefig('{}/taus_vs_is.jpg'.format(sub_folder), dpi=300)

    xs = np.linspace(integrated_currents[0], integrated_currents[-1], 250)
    interp_zs = np.array([np.interp(xs, integrated_currents, zs[0]), np.interp(xs, integrated_currents, zs[1])])
    np.savetxt('{}/interp_currents.txt'.format(sub_folder), xs)
    np.savetxt('{}/interp_zs.txt'.format(sub_folder), interp_zs)

    fft_and_plots(xs=xs, zs=interp_zs, name='interp_currents', sub_folder=sub_folder)


def integrate_currents(path, pulse_form_files, sub_folder='', window_length=4096):
    n_sweeps = 100
    data = []
    for i in range(len(pulse_form_files)):
        data.append(np.loadtxt(os.path.join(path, pulse_form_files[i])) / n_sweeps)
    ch1_data = data[0]
    ch2_data = data[1]
    ch1_offset = np.average(ch1_data[window_length - 100:window_length])
    ch2_offset = np.average(ch2_data[window_length - 100:window_length])
    ch1_data -= ch1_offset
    ch2_data -= ch2_offset
    data = ch1_data + ch2_data
    n_windows = int(len(data) / window_length)
    integrated_currents = np.zeros(n_windows)
    for i in range(n_windows):
        integrated_currents[i] = np.sum(data[i * window_length:(i + 1) * window_length])
    # averaged_currents = np.zeros(int(integrated_currents.shape[0] / 2))
    # for i in range(averaged_currents.shape[0]):
    #     averaged_currents[i] = np.average(integrated_currents[i * 2:(i + 1) * 2])
    np.savetxt('{}/integrated_currents.txt'.format(sub_folder), integrated_currents)
    return integrated_currents


def fft_and_plots(xs, zs, name, sub_folder=''):
    plt.close('all')
    plt.plot(xs, zs[0])
    plt.plot(xs, zs[1])
    plt.savefig('{}/both_{}.jpg'.format(sub_folder, name), dpi=300)
    plt.close('all')
    plt.plot(xs, zs[0] - zs[1])
    plt.savefig('{}/difference_{}.jpg'.format(sub_folder, name), dpi=300)
    freqs = np.fft.rfftfreq(len(xs), xs[-1] - xs[-2])
    fft_zs = np.fft.rfft(zs[0] - zs[1])
    plt.close('all')
    plt.plot(freqs[1:], abs(fft_zs[1:]))
    plt.savefig('{}/fft_{}.jpg'.format(sub_folder, name), dpi=300)
    np.savetxt('{}/fft_{}.txt'.format(sub_folder, name), fft_zs)
    np.savetxt('{}/freqs_{}.txt'.format(sub_folder, name), freqs)


if __name__ == '__main__':
    main()
