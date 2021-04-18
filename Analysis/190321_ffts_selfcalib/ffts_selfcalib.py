import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181115_d36_current_echo_20mA/008_rand_curr_selfcalib_20mA'
    zs = np.loadtxt(os.path.join(path, 'zs_mat.txt'))
    zs_x = zs[:, 0::2]
    offset_x = calculate_offset(zs_x)
    matrix_x = shifted_matrix(zs_x, offset_x)
    matrix_x = limit_matrix(matrix_x)
    plt.close('all')
    plt.imshow(matrix_x, aspect='auto')
    plt.show()
    # plot_rows_single_phase(matrix_x, 'x')
    fft_single_phase(matrix_x, 'x')


def limit_matrix(matrix, lower_bound=-0.05, upper_bound=0.1):
    limited_matrix = np.zeros_like(matrix)
    for l, line in enumerate(matrix):
        for e, entry in enumerate(line):
            if entry < lower_bound:
                output = lower_bound
            elif entry > upper_bound:
                output = upper_bound
            else:
                output = entry
            limited_matrix[l, e] = output
    return limited_matrix


def calculate_offset(matrix):
    offset = np.mean(np.trim_zeros(matrix[:, -1]))
    return offset


def shifted_matrix(matrix, offset):
    final = trim_matrix(matrix)
    zero_ind = np.where(final == 0)
    zero_ind = zip(zero_ind[0], zero_ind[1])
    matrix = final - offset
    for ind in zero_ind:
        matrix[ind] = 0
    return matrix


def trim_matrix(zs_x):
    max_len = len(np.trim_zeros(zs_x[:, -1]))
    final = np.zeros((max_len, zs_x.shape[1]))
    for row in range(zs_x.shape[1]):
        trimmed = trim_row(row, zs_x)
        final[:len(trimmed), row] = trimmed
    return final


def trim_row(row, matrix):
    trimmed = matrix[:, row]
    while trimmed.min() == 0:
        t = -1
        trimmed = np.trim_zeros(trimmed[:t])
        t -= 1
    return trimmed


def plot_rows_single_phase(matrix, phase):
    print('plotting forms...')
    for i, row in enumerate(matrix.T):
        if i % 10 == 0:
            print('i: ', i)
        trimmed = row.copy()
        plt.close('all')
        plt.plot(trimmed)
        plt.savefig('forms/{}/form_{:03}.jpg'.format(phase, i), dpi=300)


def fft_single_phase(matrix, phase):
    print('calculating ffts...')
    n_rows = matrix.shape[1]
    ffts = np.zeros(151, dtype=np.cdouble)
    maxs = np.zeros(n_rows)
    for i, row in enumerate(matrix.T):
        if i % 10 == 0:
            print('i: ', i)
        # trimmed = np.trim_zeros(row, trim='b')
        trimmed = row.copy()
        fft = np.fft.rfft(trimmed)
        ffts += fft
        fft_abs = abs(fft)
        maxs[i] = max(fft_abs[1:])
        inverse = np.fft.irfft(fft)
        freqs = np.fft.rfftfreq(len(trimmed))
        plt.close('all')
        plt.plot(freqs, fft_abs)
        plt.savefig('ffts/{}/fft_{:03}.jpg'.format(phase, i), dpi=300)
        plt.close('all')
        plt.plot(inverse)
        plt.savefig('ffts/{}/inverse_{:03}.jpg'.format(phase, i), dpi=300)
    plt.close('all')
    plt.plot(maxs)
    plt.show()
    plt.close('all')
    plt.plot(freqs, abs(ffts) / n_rows)
    plt.savefig('ffts/{}/average.jpg'.format(phase), dpi=300)
    np.savetxt('ffts/{}/average_real.txt'.format(phase), abs(ffts) / n_rows)
    inverse_fft = np.fft.irfft(ffts / n_rows)
    plt.close('all')
    plt.plot(inverse_fft)
    plt.savefig('ffts/{}/average_inverse.jpg'.format(phase), dpi=300)
    np.savetxt('ffts/{}/average_inverse.txt'.format(phase), inverse_fft)


if __name__ == '__main__':
    main()
