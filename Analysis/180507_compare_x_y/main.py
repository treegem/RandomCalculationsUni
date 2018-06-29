import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def main():
    volts = np.loadtxt('Newfile1890.csv', skiprows=2, delimiter=',', usecols=[1])
    stepsize = 1 / 4e9
    times = np.arange(start=0, stop=len(volts) * stepsize, step=stepsize)
    plt.plot(times, volts)
    plt.savefig('full_data.png', dpi=300)
    x_low, x_high = compute_conditional_indices(times, 1.49684e-7, 3.23493e-7)
    x_fit = calc_fit_parameters(times, volts, x_low, x_high, 'x_fit.png')
    y_low, y_high = compute_conditional_indices(times, 4.61609e-7, 6.21451e-7)
    y_fit = calc_fit_parameters(times, volts, y_low, y_high, 'y_fit.png')
    x_phi, y_phi = np.degrees(x_fit[1]), np.degrees(y_fit[1])
    print(x_phi, y_phi)
    print(np.abs(x_phi - y_phi))
    x_freq, y_freq = x_fit[0], y_fit[0]
    print(x_freq, y_freq)


def calc_fit_parameters(times, volts, x_low, x_high, name):
    x_data = times[x_low:x_high]
    y_data = volts[x_low:x_high]
    fit = curve_fit(cosine_function, x_data, y_data, p0=[100e6, np.pi, 0.015, 0.],
                    bounds=([90e6, 0, 0, -0.03], [110e6, 2 * np.pi, 0.03, 0.03]))[0]
    plt.close('all')
    plt.plot(x_data, y_data)
    plt.plot(x_data, cosine_function(x_data, *fit), '.')
    plt.savefig(name, dpi=300)
    return fit


def cosine_function(t, w, phi, a, c):
    return a * np.cos(t * 2 * np.pi * w + phi) + c


def compute_conditional_indices(times, lower_bound, upper_bound):
    times_x = np.where((lower_bound < times) & (times < upper_bound))[0]
    low_index = times_x[0]
    high_index = times_x[-1] + 1
    return low_index, high_index


if __name__ == '__main__':
    main()
#
