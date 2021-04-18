import math
import os

import matplotlib.pyplot as plt
import numpy as np

import utility.fitting as fit
import utility.mat_handling as mhand


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180627_d35_isweep_gradient_nv_echo'
    name = 'windowed_echo_19p4mA.001.mat'
    full_path = os.path.join(path, name)

    current = 19
    save_dir = '{}mA'.format(current)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    os.chdir(save_dir)

    data = mhand.load_mat_file(full_path)
    taus = mhand.extract_taus(data) * 1e-9
    signal = mhand.extract_difference(data)
    fit_func = fit.gauss_decay

    # Initial guess
    T_0 = 200e-9
    f = 120e6
    phi = np.pi
    A = (signal.max() - signal.min()) / 2.
    C = 0
    p0 = [T_0, f, phi, A, C]

    # Bounds
    T_min = 80e-9
    T_max = 400e-9
    f_min = 100e6
    f_max = 250e6
    phi_min = 0
    phi_max = 2 * np.pi
    A_min = 0.8 * A
    A_max = 1.2 * A
    C_min = -0.01
    C_max = 0.01
    bound_lower = [T_min, f_min, phi_min, A_min, C_min]
    bound_upper = [T_max, f_max, phi_max, A_max, C_max]

    length = tau_window_length(taus)
    n_windows = len(taus) / length

    popts = []
    for n in range(int(n_windows)):
        window_end, window_start = compute_window_border(length, n)
        fitted_params = fit.fit_parameters(
            fit_func, signal[window_start:window_end], taus[window_start:window_end], p0,
            bounds=(bound_lower, bound_upper)
        )
        popts.append(fitted_params)
        plot_window_fit(current, fit_func, fitted_params, n, signal, taus, window_end, window_start)

    popts = np.array([np.array(popt) for popt in popts])

    np.savetxt('fit_{}mA_params.txt'.format(current), popts)

    avg_popt = np.average(popts, axis=0)
    interpolated_taus = interpolate_x(taus)

    plt.close('all')
    plt.plot(taus * 1e9, signal, 'b.')
    plt.plot(interpolated_taus * 1e9, fit_func(interpolated_taus, *avg_popt), 'r--')
    plt.text(interpolated_taus[int(0.7*len(interpolated_taus))] * 1e9, 0.7 * signal.max(), 'T_2 = {:.2e}'.format(avg_popt[0]))
    plt.savefig('fit_{}mA_averaged.png'.format(current))


def compute_window_border(length, n):
    window_start = n * length
    window_end = window_start + length
    return window_end, window_start


def plot_window_fit(current, fit_func, fitted_params, n, signal, taus, window_end, window_start):
    plt.close('all')
    plt.plot(taus[window_start:window_end], signal[window_start:window_end], 'b.')
    plt.plot(taus[window_start:window_end], fit_func(taus[window_start:window_end], *fitted_params), 'r-')
    plt.savefig('fit_{}mA_window{}.png'.format(current, n), dpi=300)


def tau_window_length(taus):
    tau_step = taus[1] - taus[0]
    for i, t in enumerate(taus):
        if i == 0:
            continue
        if not math.isclose(t - taus[i - 1], tau_step):
            break
    return i


def interpolate_x(xdata):
    tau_min = xdata[0]
    tau_max = xdata[-1]
    tau_step = xdata[1] - xdata[0]
    interpolated_taus = np.arange(tau_min, tau_max, tau_step)
    return interpolated_taus


if __name__ == '__main__':
    main()
