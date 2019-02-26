import os

import matplotlib.pyplot as plt
import numpy as np

import utility.tum_jet as tum_jet
from utility.imperial_to_metric import cm_to_inch


def tum_color(index):
    color = tum_jet.tum_raw[index]
    norm_color = (color[0] / 256, color[1] / 256, color[2] / 256)
    return norm_color


def mirror_y_graphs(estimated_middle, yminus, yplus):
    # mirroring yminus and yplus into each other
    # because average_plus_minus expects yplus to be longer

    newplus = 2 * estimated_middle - yminus
    newminus = 2 * estimated_middle - yplus

    return newplus, newminus


def main():
    path_random = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181029_d36_current_echo_First/007_random_current_echo'
    path_pure = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181029_d36_current_echo_First/008_pure_echo'

    random_data = np.loadtxt(os.path.join(path_random, 'zs_post_selected.txt'))
    regular_data = np.loadtxt(os.path.join(path_random, 'zs_regular.txt'))
    pure_data = np.loadtxt(os.path.join(path_pure, 'zs_regular.txt'))

    random_data = zs_to_probability(random_data)
    regular_data = zs_to_probability(regular_data)
    pure_data = zs_to_probability(pure_data)

    taus = np.loadtxt(os.path.join(path_random, 'taus.txt'))
    xplus = random_data[0]
    yminus = random_data[1]
    xminus = random_data[2]
    yplus = random_data[3]

    xplus_start, xplus_stop = None, None
    yminus_start, yminus_stop = 1, None
    xminus_start, xminus_stop = 6, None
    yplus_start, yplus_stop = 10, None

    estimated_middle = (xplus[-1] + xminus[-1] + yplus[-1] + yminus[-1]) / 4

    x_color = tum_color(5)
    y_color = tum_color(2)
    pure_color = tum_color(1)

    plt.close('all')
    fig = plt.figure(figsize=(cm_to_inch(1.0 * 8.6), cm_to_inch(7)))
    average_plus_minus(estimated_middle, minus=xminus, plus=xplus, start=xminus_start, stop=xminus_stop)
    yplus, yminus = mirror_y_graphs(estimated_middle, yminus, yplus)
    yminus_start, yminus_stop, yplus_start, yplus_stop = yplus_start, yplus_stop, yminus_start, yminus_stop
    average_plus_minus(estimated_middle, minus=yminus, plus=yplus, start=yminus_start, stop=yminus_stop)
    plt.plot(taus, pure_data, label='regular', color=pure_color)
    plt.plot(taus, regular_data, label='unprocessed', color=tum_color(0))
    plt.plot(taus[xplus_start:xplus_stop], xplus[xplus_start:xplus_stop], label='x', color=x_color)
    # plt.plot(taus[xminus_start:xminus_stop], xminus[xminus_start:xminus_stop], color=x_color)
    plt.plot(taus[yplus_start:yplus_stop], yplus[yplus_start:yplus_stop], label='y', color=y_color)
    # plt.plot(taus[yminus_start:yminus_stop], yminus[yminus_start:yminus_stop], color=y_color)
    plt.ylabel(r'$1-\left\langle S_z \right\rangle$')
    plt.xlabel(r'$\tau$ (ns)')
    plt.ylim(bottom=plt.ylim()[0] - 0.2)
    plt.legend(loc='lower center', ncol=2, frameon=False)
    fig.tight_layout()
    plt.savefig('echo_reconstruction_vector.svg')


def zs_to_probability(random_data):
    rabi_amplitude = 0.0900362701808  # calculated in phi_oscillation.py
    random_data -= 1 - rabi_amplitude * 2
    random_data /= 2 * rabi_amplitude
    return random_data


def average_plus_minus(estimated_middle, minus, plus, start, stop):
    for i, z in enumerate(minus[start:stop]):
        mirrored_z = 2 * estimated_middle - z
        plus[start + i] = (plus[start + i] + mirrored_z) / 2


if __name__ == '__main__':
    main()
