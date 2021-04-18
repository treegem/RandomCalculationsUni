import os

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import rfft, rfftfreq
import scipy.io as sio

from utility.integrate_currents import integrate_current


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190521_sample_N_90mA'
    fname = 'pulsed.004.mat'
    full_name = os.path.join(path, fname)

    mat_data = sio.loadmat(full_name)
    taus = mat_data['taus'][0]
    z = subtract_zs(mat_data, taus)
    np.savetxt('zs.txt', z)
    np.savetxt('taus.txt', taus)

    # TAU VS Z

    plt.close('all')
    plt.plot(taus, z)
    plt.savefig('{}.jpg'.format(fname[:-4]))

    # I VS Z

    current_file = 'currents_{}.txt'.format(fname[:-4])
    if not os.path.isfile(current_file):
        print('Integrating current...')
        integrate_current(
            fname='//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/190521_sample_N_90mA/new_analogue_004/analogue_data_ch1.txt',
            sweeps=2,
            samples_per_sweep=len(taus),
            outname=current_file
        )
        print('done.')
    integrated_currents = np.loadtxt(current_file)

    plt.close('all')
    plt.plot(integrated_currents, z)
    plt.savefig('{}.jpg'.format(current_file[:-4]))

    # TAU FFT

    fft_data = rfft(z)
    np.savetxt('fft_tau_data_{}.txt'.format(fname[:-4]), abs(fft_data))
    fft_freqs = rfftfreq(len(taus), (taus[1] - taus[0]) * 1e-9)
    np.savetxt('tau_freqs_{}.txt'.format(fname[:-4]), abs(fft_freqs))
    plt.close('all')
    plt.plot(fft_freqs, abs(fft_data))
    plt.savefig('fft_{}.jpg'.format(fname[:-4]))

    # I FFT
    equi_currents = np.linspace(integrated_currents[0], integrated_currents[-1], len(integrated_currents))
    interp_z = np.interp(equi_currents, integrated_currents, z)
    np.savetxt('interp_z_{}.txt'.format(fname[:-4]), interp_z)
    np.savetxt('interp_currents.txt'.format(fname[:-4]), equi_currents)
    plt.close('all')
    plt.plot(equi_currents, interp_z)
    plt.savefig('interp_{}.jpg'.format(current_file[:-4]))

    fft_data = rfft(interp_z)
    fft_freqs = rfftfreq(len(equi_currents), equi_currents[1] - equi_currents[0])
    np.savetxt('b_freqs_{}.txt'.format(fname[:-4]), abs(fft_freqs))
    np.savetxt('fft_data_{}.txt'.format(fname[:-4]), abs(fft_data))
    plt.close('all')
    plt.plot(fft_freqs, abs(fft_data))
    plt.savefig('fft_i_{}.jpg'.format(fname[:-4]))


def subtract_zs(mat_data, taus):
    zs = mat_data['z'][0]
    z = np.zeros_like(taus)
    for i in range(len(taus)):
        z[i] = zs[2 * i] - zs[2 * i + 1]
    return z


if __name__ == '__main__':
    main()
