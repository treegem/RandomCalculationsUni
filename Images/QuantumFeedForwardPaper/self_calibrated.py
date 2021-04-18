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
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181115_d36_current_echo_20mA/008_rand_curr_selfcalib_20mA'
    taus = np.loadtxt(os.path.join(path, 'taus.txt'))
    zs = np.loadtxt(os.path.join(path, 'zs_mat.txt'))
    zs_x = zs[:, 0::2]
    zs_y = zs[:, 1::2]

    offset_x = calculate_offset(zs_x)
    offset_y = calculate_offset(zs_y)

    # rabi_amplitude = calc_rabi_amplitude()
    rabi_amplitude = 0.11

    matrix_x = shifted_matrix(zs_x, offset_x)
    matrix_y = shifted_matrix(zs_y, offset_y)

    # normalize_matrix(matrix_x)
    # normalize_matrix(matrix_y)
    # 1.00976657456

    save_triangle_plots(matrix_x, matrix_y, taus, rabi_amplitude)

    plt.close('all')
    # fig, axes = plt.subplots(nrows=1, ncols=1)
    fig = plt.figure()
    fig.set_figwidth(cm_to_inch(8.6 * 1.))
    fig.set_figheight(cm_to_inch(6.5))
    shown_row = 11
    matrix_x = np.trim_zeros(matrix_x.T[shown_row]) / rabi_amplitude + 0.5
    matrix_y = np.trim_zeros(matrix_y.T[shown_row]) / rabi_amplitude + 0.5
    x_axis_x = np.linspace(0, 1, len(matrix_x))
    x_axis_y = np.linspace(0, 1, len(matrix_y))
    x_params, y_params = fit_examples(matrix_x, matrix_y, x_axis_x, x_axis_y)
    ax1 = fig.add_subplot(211)
    ax1.plot(x_axis_x, matrix_x, '.', color=tum_color(0))
    ax1.plot(x_axis_x, fit_func(x_axis_x, *x_params), '--', color=tum_color(5))
    ax1.set_ylim([0, 1])
    ax1.tick_params(direction='in', right=True, top=True)
    ax2 = fig.add_subplot(212)
    ax2.plot(x_axis_y, matrix_y, '.', color=tum_color(0))
    ax2.plot(x_axis_y, fit_func(x_axis_y, *y_params), '--', color=tum_color(5))
    ax2.set_ylim([0, 1])
    ax2.set_xlabel(r'$\int I \cdot \mathrm{d}t$' + ' (arb. u.)')
    ax2.set_yticks([0, 0.5])
    ax2.tick_params(direction='in', right=True, top=True)
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.subplots_adjust(hspace=0)
    fig.subplots_adjust(bottom=0.22, top=0.95, left=0.15)
    plt.ylabel(r'                    $1-\left\langle S_z \right\rangle$')
    plt.savefig('self_calibrated_examples.jpg', dpi=300)


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
    path_rabi = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181105_d36_current_echo_60mA'
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


def save_triangle_plots(matrix_x, matrix_y, taus, rabi_amplitude):
    plt.close('all')
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.set_figwidth(cm_to_inch(8.6 * 1.))
    fig.set_figheight(cm_to_inch(5.5))
    vmin = -0.5 + 0.5
    vmax = 0.5 + 0.5
    imx = axes.flat[0].imshow(matrix_x / rabi_amplitude + 0.5, aspect='auto', vmin=vmin, vmax=vmax, cmap=tum_jet,
                              interpolation='bicubic', extent=[taus[0], taus[-1], 0, 1], origin='lower')
    imy = axes.flat[1].imshow(matrix_y / rabi_amplitude + 0.5, aspect='auto', vmin=vmin, vmax=vmax, cmap=tum_jet,
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
    plt.savefig('self_calibrated_wrong_colors.jpg', dpi=300)


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
