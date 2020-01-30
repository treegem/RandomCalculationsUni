import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from utility.tum_jet import tum_color


def stretched(t, T2, n, A, cons):
    return A * np.exp(-np.power(t / T2, n)) + cons


def main():
    qff1 = np.loadtxt('../190821_40mA_noise_decay/sin_decays_qff.txt')
    tau1 = np.loadtxt('../190821_40mA_noise_decay/sin_decays_taus.txt')
    qff2 = np.loadtxt('sin_decays_qff.txt')
    tau2 = np.loadtxt('sin_decays_taus.txt')

    # rescale qff2 and tau2 due to the different free evolution times fot the two measurements
    ampl_qff_1 = qff1[0]
    ampl_tau_1 = tau1[0]
    ampl_qff_2 = np.loadtxt('50_ns_reference/sin_decays_qff.txt')
    ampl_tau_2 = np.loadtxt('50_ns_reference/sin_decays_taus.txt')

    qff_factor = ampl_qff_1 / ampl_qff_2
    tau_factor = ampl_tau_1 / ampl_tau_2

    qff = np.hstack((qff1, qff2 * qff_factor))
    tau = np.hstack((tau1, tau2 * tau_factor))

    xs = list(range(len(qff)))
    popt_qff, _ = curve_fit(stretched, xdata=xs, ydata=qff, p0=[1, 1.75, 1, 0],
                            bounds=[[0, 0.1, 0, 0], [15, 2., 1.2, 0.005]])
    popt_tau, _ = curve_fit(stretched, xdata=xs, ydata=tau, p0=[1, 1.6, 1, 0],
                            bounds=[[0, 1.0, 0, 0], [15, 2., 1.2, 0.005]])

    plt.close('all')
    plt.plot(tau, label='no_qff, T2={:.1f}, n={:.1f}'.format(*popt_tau), color=tum_color(5))
    plt.plot(stretched(xs, *popt_tau), '.', color=tum_color(5))
    plt.plot(qff, label='qff, T2={:.1f}, n={:.1f}'.format(*popt_qff), color=tum_color(0))
    plt.plot(stretched(xs, *popt_qff), '.', color=tum_color(0))
    plt.legend()
    plt.savefig('sin_decays_comparison_combined.jpg', dpi=300)


if __name__ == '__main__':
    main()
