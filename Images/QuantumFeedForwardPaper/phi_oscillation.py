import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.optimize import curve_fit

import utility.tum_jet as tum_jet
from utility.imperial_to_metric import cm_to_inch


def tum_color(index):
    color = tum_jet.tum_raw[index]
    norm_color = (color[0] / 256, color[1] / 256, color[2] / 256)
    return norm_color


def main():
    slow_oscillation_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181029_d36_current_echo_First/' \
                            '002_current_echo'
    fast_oscillation_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181220_036_phase_oscillation_deer/' \
                            '002_phase_oscillation_63mA'

    slow_bins, slow_zs = load_measurement(slow_oscillation_path)
    fast_bins, fast_zs = load_measurement(fast_oscillation_path)

    adjusted_fast_bins, adjusted_slow_bins = scale_bins_to_taus(slow_bins, fast_bins,
                                                                slow_max_tau=1, fast_max_tau=1)

    phi_amplitude = fit_amplitude(p0=[0.04, 1 / 0.4, 0.9, 0], xdata=adjusted_slow_bins, ydata=slow_zs)
    rabi_name = 'pulsed.001.mat'
    rabi_path = slow_oscillation_path + '/..'
    rabi_taus = loadmat(os.path.join(rabi_path, rabi_name))['taus'][0]
    rabi_zs = loadmat(os.path.join(rabi_path, rabi_name))['zs'][0]
    rabi_amplitude = fit_amplitude(p0=[0.2, 1 / 80., 0.85, 0], xdata=rabi_taus, ydata=rabi_zs)
    slow_zs = shift_and_normalize_zs(phi_amplitude, rabi_amplitude, zs=slow_zs)

    phi_amplitude = fit_amplitude(p0=[0.02, 10 / 0.2, 0.84, 0], xdata=adjusted_fast_bins, ydata=fast_zs)
    rabi_name = 'pulsed.009.mat'
    rabi_path = fast_oscillation_path + '/..'
    rabi_taus = loadmat(os.path.join(rabi_path, rabi_name))['taus'][0]
    rabi_zs = loadmat(os.path.join(rabi_path, rabi_name))['zs'][0]
    rabi_amplitude = fit_amplitude(p0=[0.1, 1 / 120., 0.85, 0], xdata=rabi_taus, ydata=rabi_zs)
    fast_zs = shift_and_normalize_zs(phi_amplitude, rabi_amplitude, zs=fast_zs)

    slow_lower, slow_upper = calc_y_limits('above', slow_zs)
    fast_lower, fast_upper = calc_y_limits('below', fast_zs)

    plt.close('all')
    fig, ax1 = plt.subplots()
    fig.set_figwidth(cm_to_inch(8.6 * 1.0))
    fig.set_figheight(cm_to_inch(6.5))
    slow_start = None
    slow_stop = None
    slow_color = tum_color(0)
    l1, = ax1.plot(adjusted_slow_bins[slow_start:slow_stop], slow_zs[slow_start:slow_stop], color=slow_color, label='1')
    ax1.tick_params('y', colors=slow_color)
    ax1.set_ylim(slow_lower - 0.2, slow_upper)
    ax1.set_ylabel(r'$\left\langle S_z \right\rangle$', color=slow_color)
    ax1.set_xlabel(r'$\int I \cdot \mathrm{d}t$' + ' (arb. u.)')

    ax2 = ax1.twinx()
    fast_start = None
    fast_stop = None
    fast_color = tum_color(5)
    l2, = ax2.plot(adjusted_fast_bins[fast_start:fast_stop], fast_zs[fast_start:fast_stop], color=fast_color, label='2')
    ax2.tick_params('y', colors=fast_color)
    ax2.set_ylim(fast_lower - 0.2, fast_upper)
    ax2.set_ylabel(r'$\left\langle S_z \right\rangle$', color=fast_color)
    plt.legend([l2, l1], ['high I', 'low I'], loc='lower right', ncol=2)
    fig.tight_layout()
    plt.savefig('phase_oscillation.png', dpi=300)


def shift_and_normalize_zs(phi_amplitude, rabi_amplitude, zs):
    zs -= np.average(zs)
    zs /= abs(phi_amplitude)
    zs /= 2.
    zs = zs * abs(phi_amplitude / rabi_amplitude) * -1
    zs += 0.5
    return zs


def fit_amplitude(p0, xdata, ydata):
    popt, _ = curve_fit(easy_sin, xdata, ydata, p0=p0)
    amplitude = popt[0]
    return amplitude


def easy_sin(t, A, f, C, phi):
    return A * np.sin(t * 2 * np.pi * f + phi) + C


def calc_y_limits(expansion_mode, zs):
    range_ = zs.max() - zs.min()
    if expansion_mode == 'above':
        lower = zs.min()
        upper = zs.max() + range_
    if expansion_mode == 'below':
        lower = zs.min() - range_
        upper = zs.max()
    return lower, upper


def scale_bins_to_taus(slow_bins, fast_bins, slow_max_tau, fast_max_tau):
    slow_bins -= slow_bins.min()
    fast_bins -= fast_bins.min()
    normalized_slow_bins = slow_bins / slow_bins.max()
    normalized_fast_bins = fast_bins / fast_bins.max()
    full_length = max(slow_max_tau, fast_max_tau)
    adjusted_slow_bins = normalized_slow_bins * slow_max_tau / full_length
    adjusted_fast_bins = normalized_fast_bins * fast_max_tau / full_length
    return adjusted_fast_bins, adjusted_slow_bins


def bins_to_avg(bins):
    avgs = np.zeros(len(bins) - 1)
    for i, _ in enumerate(bins):
        if i == len(bins) - 1:
            break
        avgs[i] = (bins[i] + bins[i + 1]) / 2
    return avgs


def load_measurement(path):
    bins = np.loadtxt(os.path.join(path, 'bins.txt'))
    bins = bins_to_avg(bins)
    zs = np.loadtxt(os.path.join(path, 'zs.txt'))
    zs = np.trim_zeros(zs)
    bins = bins[:len(zs)]
    return bins, zs


if __name__ == '__main__':
    main()
