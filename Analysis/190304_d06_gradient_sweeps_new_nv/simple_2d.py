import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190304_d06_gradient_sweeps_new_nv'
    n_taus = 250
    n_files = 19
    zs_2d = np.zeros((n_files, n_taus))
    fft_2d = np.zeros((n_files, int(n_taus / 2) + 1))
    for i in range(n_files):
        print(i)
        pulsed_file = 'autopilot_pulsed/pulsed_{:06}.mat'.format(i)
        data = loadmat(os.path.join(path, pulsed_file))
        taus = data['taus'][0]
        zs = data['zs']

        save_folder = 'simple_2d'
        xs = np.linspace(taus[0], taus[-1], n_taus)
        interp_taus = np.array([np.interp(xs, taus, zs[0]), np.interp(xs, taus, zs[1])])
        fft_1d = fft_and_plots(xs, zs=interp_taus, name='taus', save_folder=save_folder, i=i)
        zs_2d[i] = zs[0] - zs[1]
        fft_2d[i] = abs(fft_1d)

        if not os.path.isfile('{}/integrated_currents_{}.txt'.format(save_folder, i)):
            pulse_form_files = [
                'current_pulses_001/analogue_data_ch1_{}.txt'.format(i),
                'current_pulses_001/analogue_data_ch2_{}.txt'.format(i)
            ]
            integrated_currents = integrate_currents(path, pulse_form_files, i, save_folder)
        else:
            integrated_currents = np.loadtxt('{}/integrated_currents_{}.txt'.format(save_folder, i))
            print('loaded integrated currents from file')

        plt.close('all')
        plt.plot(taus, integrated_currents)
        plt.savefig('taus_vs_is.jpg', dpi=300)

        xs = np.linspace(integrated_currents[0], integrated_currents[-1], n_taus)
        interp_zs = np.array([np.interp(xs, integrated_currents, zs[0]), np.interp(xs, integrated_currents, zs[1])])

        fft_and_plots(xs=xs, zs=interp_zs, name='interp_currents', i=i, save_folder=save_folder)

    plt.close('all')
    plt.imshow(zs_2d)
    plt.colorbar()
    plt.savefig('{}/zs2d_{}.jpg'.format(save_folder, 'taus'), dpi=300)

    plt.close('all')
    plt.imshow(fft_2d, vmax=0.25)
    plt.colorbar()
    plt.savefig('{}/fft2d_{}.jpg'.format(save_folder, 'taus'), dpi=300)

    np.savetxt('{}/zs2d_{}.txt'.format(save_folder, 'taus'), zs_2d)
    np.savetxt('{}/fft2d_{}.txt'.format(save_folder, 'taus'), fft_2d)

    # zs_2d = np.zeros((n_files, n_taus))
    # fft_2d = np.zeros((n_files, int(n_taus / 2) + 1))
    # for i in range(n_files):
    #     print(i)
    #     pulsed_file = 'autopilot_pulsed/pulsed_{:06}.mat'.format(i)
    #     data = loadmat(os.path.join(path, pulsed_file))
    #     taus = data['taus'][0]
    #     zs = data['zs']
    #
    #     save_folder = 'simple_2d'
    #     if not os.path.isfile('{}_integrated_currents_{}.txt'.format(save_folder, i)):
    #         pulse_form_files = [
    #             'current_pulses_001/analogue_data_ch1_{}.txt'.format(i),
    #             'current_pulses_001/analogue_data_ch2_{}.txt'.format(i)
    #         ]
    #         integrated_currents = integrate_currents(path, pulse_form_files, i, save_folder)
    #     else:
    #         integrated_currents = np.loadtxt('{}_integrated_currents_{}.txt'.format(save_folder, i))
    #         print('loaded integrated currents from file')
    #
    #     plt.close('all')
    #     plt.plot(taus, integrated_currents)
    #     plt.savefig('taus_vs_is.jpg', dpi=300)
    #
    #     xs = np.linspace(integrated_currents[0], integrated_currents[-1], n_taus)
    #     interp_zs = np.array([np.interp(xs, integrated_currents, zs[0]), np.interp(xs, integrated_currents, zs[1])])
    #
    #     fft_and_plots(xs=xs, zs=interp_zs, name='interp_currents', i=i, save_folder=save_folder)


def integrate_currents(path, pulse_form_files, i, save_folder):
    n_sweeps = 100
    data_ch1 = np.loadtxt(os.path.join(path, pulse_form_files[0])) / n_sweeps
    data_ch2 = np.loadtxt(os.path.join(path, pulse_form_files[1])) / n_sweeps
    window_length = 4096
    offset_ch1 = np.average(data_ch1[window_length - 100:window_length])
    offset_ch2 = np.average(data_ch2[window_length - 100:window_length])
    data_ch1 -= offset_ch1
    data_ch2 -= offset_ch2
    data = data_ch1 + data_ch2
    n_windows = int(len(data) / window_length)
    integrated_currents = np.zeros(n_windows)
    for i in range(n_windows):
        integrated_currents[i] = np.sum(data[i * window_length:(i + 1) * window_length])
    np.savetxt('{}/integrated_currents_{}.txt'.format(save_folder, i), integrated_currents)
    return integrated_currents


def fft_and_plots(xs, zs, name, save_folder, i):
    plt.close('all')
    plt.plot(xs, zs[0])
    plt.plot(xs, zs[1])
    plt.savefig('{}/both_{}_{}.jpg'.format(save_folder, name, i), dpi=300)
    plt.close('all')
    plt.plot(xs, zs[0] - zs[1])
    plt.savefig('{}/difference_{}_{}.jpg'.format(save_folder, name, i), dpi=300)
    freqs = np.fft.rfftfreq(len(xs), xs[-1] - xs[-2])
    fft_zs = np.fft.rfft(zs[0] - zs[1])
    plt.close('all')
    plt.plot(freqs[1:], abs(fft_zs[1:]))
    plt.savefig('{}/fft_{}_{}.jpg'.format(save_folder, name, i), dpi=300)
    return fft_zs


if __name__ == '__main__':
    main()
