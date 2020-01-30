import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import scipy.optimize as soptimize

from utility.imperial_to_metric import cm_to_inch
from utility.tum_jet import tum_jet, tum_raw


def tum_color(index):
    color = tum_raw[index]
    norm_color = (color[0] / 256, color[1] / 256, color[2] / 256)
    return norm_color


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181115_d36_current_echo_20mA/008_rand_curr_selfcalib_20mA'
    taus = np.loadtxt(os.path.join(path, 'taus.txt'))
    zs = np.loadtxt(os.path.join(path, 'zs_mat.txt'))
    zs_x = zs[:, 0::2]
    zs_y = zs[:, 1::2]

    offset_x = calculate_offset(zs_x)
    offset_y = calculate_offset(zs_y)

    rabi_amplitude = 0.11

    matrix_x = shifted_matrix(zs_x, offset_x)
    matrix_y = shifted_matrix(zs_y, offset_y)

    save_triangle_plots(matrix_x, taus, rabi_amplitude)


def fit_examples(matrix_x, matrix_y, x_axis_x, x_axis_y):
    x_params = perform_fit(p0=[0.22, 0.5, 0.1, 0.5], trimmed=matrix_x, xdata=x_axis_x)
    print(x_params)
    y_params = perform_fit(p0=[0.2167, 0.5, -np.pi / 4, 0.5], trimmed=matrix_y, xdata=x_axis_y)
    print(y_params)
    return x_params, y_params


def zs_to_probability(random_data, offset):
    rabi_amplitude = 0.0900362701808  # calculated in phi_oscillation.py
    rabi_amplitude = 0.11
    random_data -= offset
    random_data /= rabi_amplitude
    random_data = random_data / 2 + 0.5
    return random_data


def calc_rabi_amplitude():
    path_rabi = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181105_d36_current_echo_60mA'
    rabi_file = 'pulsed.005.mat'
    rabi_data = sio.loadmat(os.path.join(path_rabi, rabi_file))
    rabi_zs = rabi_data['zs'][0]
    rabi_taus = rabi_data['taus'][0]
    popt = perform_fit(p0=[60., 0.01, 0, 0.96], trimmed=rabi_zs, xdata=rabi_taus)
    rabi_amplitude = popt[1]
    return rabi_amplitude


def perform_fit(p0, trimmed, xdata):
    popt, pcov = soptimize.curve_fit(fit_func, xdata, trimmed, p0=p0, bounds=(
        [p0[0] / 2, 0.35, -np.pi, 0.5], [p0[0] * 2, 2, 2.25 * np.pi, 1]))
    return popt


def fit_func(t, T, A, phi, C):
    return A * np.cos(t * 2 * np.pi / T + phi) + C


def compress_matrix_vertical(matrix_x):
    echo_decay = np.loadtxt('sine_fit_zs.txt')
    return echo_decay


def save_triangle_plots(matrix_x, taus, rabi_amplitude):
    plt.close('all')
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_figwidth(cm_to_inch(8.6 * 1.))
    fig.set_figheight(cm_to_inch(5.5 * 1.3))
    vmin = -0.5 + 0.5
    vmax = 0.5 + 0.5
    imone = axes.flat[0].imshow(matrix_x / rabi_amplitude + 0.5, aspect='auto', vmin=vmin, vmax=vmax, cmap=tum_jet,
                                interpolation='bicubic', extent=[taus[0], taus[-1], 0, 0.5], origin='lower')
    c_matrix_x = compress_matrix_horizontal(matrix_x) / rabi_amplitude + 0.5
    imtwo = axes.flat[1].plot(c_matrix_x, np.linspace(c_matrix_x.min(), c_matrix_x.max(), len(c_matrix_x)),
                              color=tum_color(0))

    echo_decay = compress_matrix_vertical(matrix_x)
    imthree = axes.flat[2].plot(taus, echo_decay, color=tum_color(0))

    axes.flat[0].set_ylabel(r'$\int I \cdot \mathrm{d}t$' + r' (20 mA$\cdot \mu$s)')
    axes.flat[0].tick_params(axis='both', direction='in', top=True, right=True)
    axes.flat[0].axes.get_yaxis().set_ticks(
        [0, 0.1, 0.2, 0.3, 0.4, 0.5])
    axes.flat[0].axes.get_xaxis().set_ticks([255])

    axes.flat[1].tick_params(axis='both', direction='in', top=True, right=True)
    axes.flat[1].axes.get_yaxis().set_ticklabels([])
    axes.flat[1].set_xlim([0, 1])
    axes.flat[1].set_ylim([c_matrix_x.min(), c_matrix_x.max()])
    axes.flat[1].axes.get_xaxis().set_ticks([0.5, 1])
    axes.flat[1].axes.get_xaxis().set_ticklabels([0.5, 1])
    amplitude = c_matrix_x.max() - c_matrix_x.min()
    axes.flat[1].axes.get_yaxis().set_ticks(
        [c_matrix_x.min(), c_matrix_x.min() + 0.2 * amplitude, c_matrix_x.min() + 0.4 * amplitude,
         c_matrix_x.min() + 0.6 * amplitude, c_matrix_x.min() + 0.8 * amplitude, c_matrix_x.min() + amplitude])
    axes.flat[1].set_xlabel(r'$1-\left\langle S_z \right\rangle$')

    axes.flat[2].set_xlabel(r'$\tau$ (ns)')
    axes.flat[2].set_ylabel(r'$1-\left\langle S_z \right\rangle$')
    axes.flat[2].set_xlim([0, 500])
    axes.flat[2].axes.get_xaxis().set_ticks([0, 250, 500])

    fig.delaxes(axes.flat[3])
    fig.subplots_adjust(right=0.75, left=0.2, bottom=0.15, top=0.95, wspace=0.0, hspace=0.0)
    cbar_ax = fig.add_axes([0.8, 0.55, 0.05, 0.4])
    fig.colorbar(imone, cax=cbar_ax, label=r'$1-\left\langle S_z \right\rangle$', ticks=[0, 0.5, 1])
    plt.savefig('self_calibrated_x_wrong_colors.jpg', dpi=500)


def compress_matrix_horizontal(matrix):
    compressed_matrix = np.zeros(matrix.shape[0])
    last_appendix_length = 0
    for row in range(matrix.shape[1]):
        appendix_length = len(np.trim_zeros(matrix[:, row])) - 5
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
    # offset = np.mean(np.trim_zeros(matrix[:, -1]))
    # avg = 0
    # matrix = trim_matrix(matrix)
    # for row in matrix.T:
    #     avg += np.mean(np.trim_zeros(row))
    # avg /= matrix.shape[1]
    offsets_x = np.loadtxt('offsets_x.txt')
    offsets_y = np.loadtxt('offsets_y.txt')
    offsets = (offsets_x + offsets_y) / 2
    offsets = np.average(offsets)
    print(offsets)
    return offsets


def trim_row(row, matrix):
    trimmed = matrix[:, row]
    while trimmed.min() == 0:
        t = -1
        trimmed = np.trim_zeros(trimmed[:t])
        t -= 1
    return trimmed


if __name__ == '__main__':
    main()
