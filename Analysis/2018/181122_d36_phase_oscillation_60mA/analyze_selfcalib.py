import os
import numpy as np


def main():
    dir = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181122_d36_phase_oscillation_60mA/007_selfcalibrated_60mA_50LP'
    zs = np.loadtxt(os.path.join(dir, 'zs_mat.txt'))
    zs_x = zs[:, 0::2]
    zs_y = zs[:, 1::2]

    plt.close('all')
    plt.imshow(zs_x, aspect='auto', vmin=0.9, vmax=1.05, cmap='coolwarm')
    plt.colorbar()
    plt.show()

    offset_x = calculate_offset(zs_x)
    offset_y = calculate_offset(zs_y)

    matrix_x = shifted_matrix(zs_x, offset_x)
    matrix_y = shifted_matrix(zs_y, offset_y)

    plt.close('all')
    plt.imshow(matrix_x, aspect='auto', vmin=0.9 - offset_x, vmax=1.05 - offset_x, cmap='coolwarm')
    plt.colorbar()
    plt.show()

    normalize_matrix(matrix_x)
    normalize_matrix(matrix_y)

    compressed_matrix_x = compress_matrix(matrix_x)
    compressed_matrix_y = compress_matrix(matrix_y)

    plt.close('all')
    plt.plot(compressed_matrix_x)
    plt.show()

    plt.close('all')
    plt.plot(compressed_matrix_y)
    plt.show()

    plt.close('all')
    plt.imshow(matrix_x, aspect='auto', vmin=0.9 - offset_x, vmax=1.05 - offset_x, cmap='coolwarm')
    plt.colorbar()
    plt.show()

    plt.close('all')
    plt.imshow(matrix_y, aspect='auto', vmin=0.9 - offset_y, vmax=1.05 - offset_y, cmap='coolwarm')
    plt.colorbar()
    plt.show()


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
    import matplotlib

    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    main()
