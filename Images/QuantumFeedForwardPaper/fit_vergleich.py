import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

from utility.imperial_to_metric import cm_to_inch
from utility.tum_jet import tum_raw


def tum_color(index):
    color = tum_raw[index]
    norm_color = (color[0] / 256, color[1] / 256, color[2] / 256)
    return norm_color


def zs_to_probability(random_data, offset, save=False):
    rabi_amplitude = 0.0900362701808  # calculated in phi_oscillation.py
    rabi_amplitude = 0.11
    random_data -= offset
    random_data /= rabi_amplitude
    random_data = random_data / 2 + 0.5
    if save is True:
        np.savetxt('sine_fit_zs.txt', random_data)
    return random_data


def compose_final(path, taus):
    offset_x = np.loadtxt('offsets_x.txt')
    offset_y = np.loadtxt('offsets_y.txt')
    offset = np.average([offset_x, offset_y])

    sinus_fit_graph = np.loadtxt('amplitudes.txt')
    post_selected_graph = np.loadtxt('post_selected_in_one.txt')
    unprocessed = np.loadtxt(os.path.join(path, 'zs_regular.txt'))

    # total_max = max(sinus_fit_graph.max(), post_selected_graph.max(), unprocessed.max())

    sinus_fit_graph = zs_to_probability(sinus_fit_graph, offset, save=True)
    plot_exp_fit_graph(sinus_fit_graph, taus)
    post_selected_graph = zs_to_probability(post_selected_graph, offset)
    plot_exp_fit_graph(post_selected_graph, taus)
    unprocessed = zs_to_probability(unprocessed, offset)
    plot_exp_fit_graph(unprocessed, taus)

    plt.close('all')
    plt.figure(figsize=(cm_to_inch(1.5 * 8.6), cm_to_inch(6.5)))
    plt.plot(taus, unprocessed, label='unprocessed', color=tum_color(0))
    plt.plot(taus, post_selected_graph, label='feed forward decoupling', color=tum_color(3))
    plt.plot(taus, sinus_fit_graph, label='sine fit', color=tum_color(2))
    plt.legend()
    plt.xlabel(r'$\tau$ (ns)')
    plt.ylabel(r'$1-\left\langle S_z \right\rangle$')
    plt.tight_layout()
    plt.savefig('all_fits.svg')


def plot_exp_fit_graph(exp_fit_graph, taus):
    params = fit_exp(p0=[100, 0.3, 0.5], ydata=exp_fit_graph, xdata=taus)
    plt.close('all')
    plt.plot(taus, exp_fit_graph)
    plt.plot(taus, exp_func(taus, *params))
    plt.show()


def main():
    global offset_x, offset_y
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181115_d36_current_echo_20mA/008_rand_curr_selfcalib_20mA'
    taus = np.loadtxt(os.path.join(path, 'taus.txt'))

    zs = np.loadtxt(os.path.join(path, 'zs_mat.txt'))
    zs_x = zs[:, 0::2]
    zs_y = zs[:, 1::2]

    offset_x = calculate_offset(zs_x)
    offset_y = calculate_offset(zs_y)

    # matrix_x = shifted_matrix(zs_x, offset_x)
    # matrix_y = shifted_matrix(zs_y, offset_y)

    # plot_rows(matrix_x, 'x')

    # post_selected_plot(path, taus)
    # sinus_fit(matrix_x, matrix_y, taus, offset_x, offset_y)

    # fft_single_phase(matrix_x, 'x')
    # fft_single_phase(matrix_y, 'y')

    compose_final(path, taus)


def plot_rows(matrix, phase):
    for i, row in enumerate(matrix.T):
        plt.close('all')
        plt.plot(row)
        plt.savefig('rows/{}/row_{}.jpg'.format(phase, i), dpi=300)


def fft_fit_function_x(t, A):
    pass


def fft_single_phase(matrix, phase):
    n_rows = matrix.shape[1]
    ffts = np.zeros(151, dtype=np.cdouble)
    for i, row in enumerate(matrix.T):
        # trimmed = np.trim_zeros(row, trim='b')
        trimmed = row.copy()
        fft = np.fft.rfft(trimmed)
        ffts += fft
        fft_abs = abs(fft)
        fft[np.where(fft_abs < 1.0)] = 0
        inverse = np.fft.irfft(fft)
        fft_abs = abs(fft)
        freqs = np.fft.rfftfreq(len(trimmed))
        plt.close('all')
        plt.plot(freqs, fft_abs)
        plt.savefig('ffts/{}/fft_{:03}.jpg'.format(phase, i), dpi=300)
        plt.close('all')
        plt.plot(inverse)
        plt.savefig('ffts/{}/inverse_{:03}.jpg'.format(phase, i), dpi=300)
    plt.close('all')
    plt.plot(freqs, abs(ffts) / n_rows)
    plt.savefig('ffts/{}/average.jpg'.format(phase), dpi=300)
    np.savetxt('ffts/{}/average_real.txt'.format(phase), abs(ffts) / n_rows)
    inverse_fft = np.fft.irfft(ffts / n_rows)
    plt.close('all')
    plt.plot(inverse_fft)
    plt.savefig('ffts/{}/average_inverse.jpg'.format(phase), dpi=300)
    np.savetxt('ffts/{}/average_inverse.txt'.format(phase), inverse_fft)


def sinus_fit(matrix_x, matrix_y, taus, offset_x, offset_y):
    sinus_fit_single(matrix_x.T, '_x', [80 / 5, 0.05, 0, 0], offset_x)
    sinus_fit_single(matrix_y.T, '_y', [80 / 5, 0.05, np.pi / 2, 0], offset_y)
    sinus_fit_average(taus)


def sinus_fit_average(taus):
    global offset_x, offset_y
    amplitudes_x = np.loadtxt('amplitudes_x.txt') + offset_x
    amplitudes_y = np.loadtxt('amplitudes_y.txt') + offset_y
    amplitudes = (amplitudes_x + amplitudes_y) / 2
    np.savetxt('amplitudes.txt', amplitudes)
    plt.close('all')
    plt.plot(taus, amplitudes)
    plt.savefig('sinus_fit.jpg', dpi=300)


def sinus_fit_single(matrix, name_add, p0, offset):
    n_rows = matrix.shape[0]
    amplitudes = np.zeros(n_rows)
    offsets = np.zeros(n_rows)
    for i, row in enumerate(matrix):
        if i % 1 == 0:
            print(i)
            trimmed = np.trim_zeros(row, trim='b')
            xdata = np.array(range(len(trimmed)))
            remove_outliers(trimmed, mini=-0.11, maxi=0.11)
            popt = perform_fit(p0, trimmed, xdata)
            amplitudes[i] = popt[1]
            offsets[i] = popt[3] + offset
            plt.close('all')
            plt.plot(xdata, trimmed)
            plt.plot(xdata, fit_func(xdata, *popt))
            plt.savefig('fits/end_pulse_x/row_{:03}.jpg'.format(i), dpi=300)
    np.savetxt('amplitudes{}.txt'.format(name_add), amplitudes)
    np.savetxt('offsets{}.txt'.format(name_add), offsets)
    plt.close('all')
    plt.plot(amplitudes)
    plt.savefig('sinus_fit{}.jpg'.format(name_add), dpi=300)


def remove_outliers(row, mini, maxi):
    for j, val in enumerate(row):
        if val > maxi:
            row[j] = maxi
        elif val < mini:
            row[j] = mini


def exp_func(t, T, A, C):
    return A * np.exp(-t / T) + C


def fit_exp(p0, ydata, xdata, func=exp_func):
    popt, pcov = scipy.optimize.curve_fit(func, xdata, ydata, p0=p0)
    print(popt)
    return popt


def fit_func(t, T, A, phi, C):
    return A * np.cos(t * 2 * np.pi / T + phi) + C


def perform_fit(p0, trimmed, xdata, func=fit_func):
    popt, pcov = scipy.optimize.curve_fit(func, xdata, trimmed, p0=p0,
                                          bounds=(
                                              [p0[0] / 2, 0, -np.pi + p0[2], -0.2],
                                              [p0[0] * 2, 0.2, np.pi + p0[2], 0.2]))
    return popt


def normalize_matrix(matrix):
    for row in range(matrix.shape[1]):
        trimmed = np.trim_zeros(matrix[:, row])
        std = np.std(trimmed)
        ampl = std * np.sqrt(2)
        matrix[:, row] /= ampl


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


def post_selected_plot(path, taus):
    # y minus is the actual y plus
    zs_post_selected = np.loadtxt(os.path.join(path, 'zs_post_selected.txt'))
    xplus = zs_post_selected[0]
    yminus = zs_post_selected[1]
    xminus = zs_post_selected[2]
    yplus = zs_post_selected[3]
    skip = 3
    center = np.average((xplus + xminus + yplus + yminus)[skip:] / 4)
    x_color = tum_color(5)
    y_color = tum_color(2)
    plt.close('all')
    plt.plot(taus, xplus, color=x_color)
    plt.plot(taus, xminus, color=x_color)
    plt.plot(taus, yplus, color=y_color)
    plt.plot(taus, yminus, color=y_color)
    plt.savefig('post_selected.jpg', dpi=300)
    plt.close('all')
    xminus = 2 * center - xminus
    yplus = 2 * center - yplus
    plusses = (xplus + yminus) / 2
    minusses = (xminus + yplus) / 2
    for i in range(2, len(plusses)):
        plusses[i] = (plusses[i] + minusses[i]) / 2
    np.savetxt('post_selected_in_one.txt', plusses)
    # plt.plot(taus, xplus, color=x_color)
    # plt.plot(taus, xminus, color=x_color)
    # plt.plot(taus, yplus, color=y_color)
    # plt.plot(taus, yminus, color=y_color)
    plt.plot(taus, plusses, color=tum_color(0))
    plt.savefig('post_selected_in_one.jpg', dpi=300)


def tum_color(index):
    color = tum_raw[index]
    norm_color = (color[0] / 256, color[1] / 256, color[2] / 256)
    return norm_color


if __name__ == '__main__':
    main()
