import os

import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as fft


def main(path, name):
    full_name = os.path.join(path, name)
    data = np.loadtxt(full_name).T

    fs = calculate_frequency_spacings(data)

    transform_difference = fourier_transform(data[1] - data[2])
    save_name = path.split('/')[-1] + '_difference'
    plot_fft(fs[1:], save_name, transform_difference[1:], ylim=[None, None])

    transform = fourier_transform((data[1] + data[2]) / 2.)
    save_name = path.split('/')[-1]
    plot_fft(fs[1:], save_name, transform[1:], ylim=[None, None])


def plot_fft(fs, save_name, transform_difference, ylim):
    plt.close('all')
    plt.plot(fs[1:], transform_difference[1:])
    plt.ylim(ylim)
    plt.savefig('{}.png'.format(save_name), dpi=300)


def fourier_transform(data):
    transform = abs(fft.rfft(data))
    return transform


def calculate_frequency_spacings(data):
    times = data[0] * 1e-9
    fs = fft.rfftfreq(times.size, times[2] - times[1])
    return fs


if __name__ == '__main__':
    for i in range(8, 17 + 1):
        path_ = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180420_D17_deer_correlation_echo_ramsey/deer_{:03}'\
            .format(i)
        name_ = 'last_sweep.txt'
        main(path_, name_)
