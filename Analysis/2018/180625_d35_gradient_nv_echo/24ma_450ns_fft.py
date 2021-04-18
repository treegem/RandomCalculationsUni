import os

import matplotlib.pyplot as plt
import numpy.fft as nfft

import utility.mat_handling as mhand


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180625_d35_gradient_nv_echo'
    filename = '24ma_450ns.001.mat'
    full_path = os.path.join(path, filename)
    data = mhand.load_mat_file(full_path)
    taus = mhand.extract_taus(data) * 1e-9
    differences = mhand.extract_difference(data)

    plot_difference(differences, filename, taus)

    fft_differences = nfft.rfft(differences)
    freqs = nfft.rfftfreq(len(taus), taus[1] - taus[0])

    plot_fft_difference(fft_differences, filename, freqs)


def plot_fft_difference(fft_differences, filename, freqs):
    plt.close('all')
    plt.plot(freqs * 1e-6, abs(fft_differences))
    plt.xlabel('frequency (MHz)')
    plt.ylabel('abs(fft transform)')
    plt.savefig('{}_fft.png'.format(filename.split('.')[0]), dpi=300)


def plot_difference(differences, filename, taus):
    plt.close('all')
    plt.plot(taus * 1e9, differences)
    plt.xlabel('current duration (ns)')
    plt.ylabel('signal difference')
    plt.savefig('{}_diff.png'.format(filename.split('.')[0]), dpi=300)


if __name__ == '__main__':
    main()
