import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def main():
    source_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190226_d06_gradient_sweep/002_gradient_sweep'
    n_pulses = 100
    n_files = 100
    final_matrix_zs = np.zeros((n_files, n_pulses))
    final_matrix_fft = np.zeros((n_files, int(n_pulses / 2) + 1))
    for i in range(1, n_files + 1):
        source_file = 'pulsed_{:06}.mat'.format(i)
        data = loadmat(os.path.join(source_path, source_file))
        zs = data['zs']
        integrated_currents = np.loadtxt('gradient_sweep/integrated_currents_ch1_{:03}.txt'.format(i))

        xs = np.linspace(integrated_currents[0], integrated_currents[-1], n_pulses)
        interp_zs = np.array([np.interp(xs, integrated_currents, zs[0]), np.interp(xs, integrated_currents, zs[1])])

        final_matrix_zs[i - 1] = interp_zs[0] - interp_zs[1]

        # freqs = np.fft.rfftfreq(len(xs), xs[-1] - xs[-2])
        fft_zs = np.fft.rfft(interp_zs[0] - interp_zs[1])
        final_matrix_fft[i - 1] = abs(fft_zs)

    plt.close('all')
    plt.imshow(final_matrix_zs, aspect='auto')
    plt.colorbar()
    plt.savefig('interp_curr_zs.png', dpi=300)

    plt.close('all')
    plt.imshow(final_matrix_fft, aspect='auto', vmax=0.15)
    plt.colorbar()
    plt.savefig('interp_curr_fft.png', dpi=300)


if __name__ == '__main__':
    main()
