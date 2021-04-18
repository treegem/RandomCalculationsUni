import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from Images.QuantumFeedForwardPaper.phi_oscillation import load_measurement
from Images.Rostock2019.phi_osci import scale_bins_to_taus


def fit(p0, xdata, ydata):
    fit_params, _ = curve_fit(easy_sin, xdata, ydata, p0=p0)
    return fit_params


def easy_sin(t, A, f, C, phi, T):
    return A * np.exp((-t / T)) * np.sin(t * 2 * np.pi * f + phi) + C


def main():
    fast_oscillation_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181220_036_phase_oscillation_deer/' \
                            '002_phase_oscillation_63mA'
    fast_bins, fast_zs = load_measurement(fast_oscillation_path)
    adjusted_fast_bins, adjusted_fast_bins = scale_bins_to_taus(fast_bins, fast_bins,
                                                                slow_max_tau=500, fast_max_tau=500)
    start = 0
    end = -100
    params = fit(p0=[0.02, 10 / 0.2, 0.84, 0, 0.5], xdata=adjusted_fast_bins[start:end], ydata=fast_zs[start:end])
    print(params[-1])
    plt.close('all')
    plt.plot(adjusted_fast_bins[start:end],
             easy_sin(adjusted_fast_bins[start:end], *params))
    plt.plot(adjusted_fast_bins, fast_zs)
    plt.show()
    print(adjusted_fast_bins)


if __name__ == '__main__':
    main()
