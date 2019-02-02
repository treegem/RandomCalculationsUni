import os

import matplotlib.pyplot as plt
import numpy as np
import utility.tum_jet as tum_jet
import scipy.optimize


def compose_final(path):
    sinus_fit_graph = np.loadtxt('amplitudes.txt')
    post_selected_graph = np.loadtxt('post_selected_in_one.txt')
    unprocessed = np.loadtxt(os.path.join(path, 'zs_regular.txt'))

    plt.close('all')
    plt.plot(unprocessed, label='unprocessed')
    plt.plot(post_selected_graph, label='post_selected')
    plt.plot(sinus_fit_graph, label='sine fit')
    plt.legend()
    plt.show()


def main():
    global offset_x, offset_y
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181115_d36_current_echo_20mA/008_rand_curr_selfcalib_20mA'
    taus = np.loadtxt(os.path.join(path, 'taus.txt'))
    post_selected_plot(path, taus)

    zs = np.loadtxt(os.path.join(path, 'zs_mat.txt'))
    zs_x = zs[:, 0::2]
    zs_y = zs[:, 1::2]

    offset_x = calculate_offset(zs_x)
    offset_y = calculate_offset(zs_y)

    matrix_x = shifted_matrix(zs_x, offset_x)
    matrix_y = shifted_matrix(zs_y, offset_y)

    # sinus_fit(matrix_x, matrix_y, taus)

    compose_final(path)


def sinus_fit(matrix_x, matrix_y, taus):
    sinus_fit_single(matrix_x.T, '_x', [80 / 5, 0.05, 0, 0])
    sinus_fit_single(matrix_y.T, '_y', [80 / 5, 0.05, np.pi / 2, 0])
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


def sinus_fit_single(matrix, name_add, p0):
    n_rows = matrix.shape[0]
    amplitudes = np.zeros(n_rows)
    for i, row in enumerate(matrix):
        if i % 1 == 0:
            print(i)
            trimmed = np.trim_zeros(row, trim='b')
            xdata = np.array(range(len(trimmed)))
            remove_outliers(trimmed, mini=-0.11, maxi=0.11)
            popt = perform_fit(p0, trimmed, xdata)
            amplitudes[i] = popt[1]
            plt.close('all')
            plt.plot(xdata, trimmed)
            plt.plot(xdata, fit_func(xdata, *popt))
            plt.savefig('fits/end_pulse_x/row_{:03}.jpg'.format(i), dpi=300)
    np.savetxt('amplitudes{}.txt'.format(name_add), amplitudes)
    plt.close('all')
    plt.plot(amplitudes)
    plt.savefig('sinus_fit{}.jpg'.format(name_add), dpi=300)


def remove_outliers(row, mini, maxi):
    for j, val in enumerate(row):
        if val > maxi:
            row[j] = maxi
        elif val < mini:
            row[j] = mini


def perform_fit(p0, trimmed, xdata):
    popt, pcov = scipy.optimize.curve_fit(fit_func, xdata, trimmed, p0=p0,
                                          bounds=(
                                              [p0[0] / 2, 0, -np.pi + p0[2], -0.2],
                                              [p0[0] * 2, 0.2, np.pi + p0[2], 0.2]))
    return popt


def fit_func(t, T, A, phi, C):
    return A * np.cos(t * 2 * np.pi / T + phi) + C


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
    color = tum_jet.tum_raw[index]
    norm_color = (color[0] / 256, color[1] / 256, color[2] / 256)
    return norm_color


if __name__ == '__main__':
    main()
