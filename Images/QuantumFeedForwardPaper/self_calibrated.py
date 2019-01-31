import os

import matplotlib.pyplot as plt
import numpy as np

from utility.imperial_to_metric import cm_to_inch
from utility.tum_jet import tum_jet


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181115_d36_current_echo_20mA/008_rand_curr_selfcalib_20mA'
    taus = np.loadtxt(os.path.join(path, 'taus.txt'))
    zs = np.loadtxt(os.path.join(path, 'zs_mat.txt'))
    zs_x = zs[:, 0::2]
    zs_y = zs[:, 1::2]

    offset_x = calculate_offset(zs_x)
    offset_y = calculate_offset(zs_y)

    matrix_x = shifted_matrix(zs_x, offset_x)
    matrix_y = shifted_matrix(zs_y, offset_y)

    normalize_matrix(matrix_x)
    normalize_matrix(matrix_y)

    plt.close('all')
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.set_figwidth(cm_to_inch(8.6 * 1.))
    fig.set_figheight(cm_to_inch(5.5))
    imx = axes.flat[0].imshow(matrix_x + offset_x - 0.05, aspect='auto', vmin=0.85, vmax=1., cmap=tum_jet,
                              interpolation='bicubic', extent=[taus[0], taus[-1], 0, 1], origin='lower')
    imy = axes.flat[1].imshow(matrix_y + offset_y - 0.05, aspect='auto', vmin=0.85, vmax=1., cmap=tum_jet,
                              interpolation='bicubic', extent=[taus[0], taus[-1], 0, 1], origin='lower')
    axes.flat[0].set_ylabel(r'$\int I \cdot \mathrm{d}t$' + ' (arb. u.)')
    axes.flat[1].axes.get_yaxis().set_ticklabels([])
    for ax in axes.flat:
        ax.tick_params(axis='both', direction='in', top=True, right=True)
        ax.set_xlabel(r'$\tau$ (ns)')
    plt.tight_layout()
    fig.subplots_adjust(right=0.75, left=0.16, wspace=0.0)
    cbar_ax = fig.add_axes([0.82, 0.2, 0.05, 0.7])
    fig.colorbar(imy, cax=cbar_ax)

    plt.savefig('self_calibrated.jpg', dpi=300)


def compress_matrix(matrix):
    compressed_matrix = np.zeros(matrix.shape[0])
    last_appendix_length = 0
    for row in range(matrix.shape[1]):
        appendix_length = len(np.trim_zeros(matrix[:, row]))
        if appendix_length < last_appendix_length:
            continue
        compressed_matrix[last_appendix_length:appendix_length] = np.mean(
            matrix[last_appendix_length:appendix_length, row:], axis=1)
        last_appendix_length = appendix_length
    return compressed_matrix


def normalize_matrix(matrix):
    for row in range(matrix.shape[1]):
        trimmed = np.trim_zeros(matrix[:, row])
        std = np.std(trimmed)
        ampl = std * np.sqrt(2)
        matrix[:, row] /= ampl


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


def calculate_offset(matrix):
    offset = np.mean(np.trim_zeros(matrix[:, -1]))
    return offset


def trim_row(row, matrix):
    trimmed = matrix[:, row]
    while trimmed.min() == 0:
        t = -1
        trimmed = np.trim_zeros(trimmed[:t])
        t -= 1
    return trimmed


if __name__ == '__main__':
    main()
