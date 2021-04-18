import os

import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as fft


def main(path, name):
    full_name = os.path.join(path, name)
    data = np.loadtxt(full_name).T

    fs = calculate_frequency_spacings(data)
    transform = fourier_transform(data)

    ylim = [None, None]
    save_name = path.split('/')[-1]

    plt.plot(fs[1:] / 2., transform[1:])
    plt.ylim(ylim)
    plt.savefig('{}.png'.format(save_name), dpi=300)


def fourier_transform(data):
    difference = data[1] - data[2]
    transform = abs(fft.rfft(difference))
    return transform


def calculate_frequency_spacings(data):
    times = data[0] * 1e-9
    fs = fft.rfftfreq(times.size, times[2] - times[1])
    return fs


if __name__ == '__main__':
    path_ = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180417_D17_deer_correlation_echo/deer_022'
    name_ = 'last_sweep.txt'
    main(path_, name_)
