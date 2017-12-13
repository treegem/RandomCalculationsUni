import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import physical_constants

from utility.tum_jet import tum_colors


def main():
    b = np.linspace(start=0, stop=0.01, num=500)
    splus = np.zeros_like(b)
    sminus = np.zeros_like(b)

    compute_energy_shift(b, sminus, splus)

    b = tesla_to_gauss(b)
    sminus, splus = hertz_to_megahertz(sminus, splus)

    x0, x1, y0, y1 = initialize_figure(b, sminus, splus)
    y1 += 10

    plot_resonance_condition(b, splus, x0, x1, splitting=200)

    plot_energy_shift(b, sminus, splus)

    format_plot(x0, x1, y0, y1)

    save_figure(path='//file/e24/Projects/ReinhardLab/Georg/Abstracts Anträge/'
                     'F-Praktikum/Latexnew/images/zeeman_splitting.png')


def format_plot(x0, x1, y0, y1):
    plt.ylim((y0, y1))
    plt.xlim((x0, x1))
    plt.legend()
    plt.xlabel(r'$B_0$ (G)')
    plt.ylabel('Energy shift (MHz)')
    plt.tight_layout()


def plot_energy_shift(b, sminus, splus):
    plt.plot(b, splus, color=tum_colors[0][1], label=r'$m_S =  $' + ' 1/2')
    plt.plot(b, sminus, color=tum_colors[5][1], label=r'$m_S = -1/2$')


def plot_resonance_condition(b, splus, x0, x1, splitting=100):
    plt.plot([x0, x1], [splitting / 2, splitting / 2], '--', color='grey')
    plt.plot([x0, x1], [-splitting / 2, -splitting / 2], '--', color='grey')

    target_index = np.where(splus >= splitting / 2)[0][0]
    target_b = b[target_index]
    two_headed_arrow(splitting, target_b, alpha=1)
    two_headed_arrow(splitting, 40, alpha=0.5)
    two_headed_arrow(splitting, 100, alpha=0.5)


def two_headed_arrow(splitting, target_b, alpha):
    plt.arrow(target_b, 0, 0, splitting / 2, width=0.8, head_width=2, head_length=8, overhang=0.2,
              length_includes_head=True, color=tum_colors[2][1], linewidth=0, alpha=alpha)
    plt.arrow(target_b, 0, 0, -splitting / 2, width=0.8, head_width=2, head_length=8, overhang=0.2,
              length_includes_head=True, color=tum_colors[2][1], linewidth=0, alpha=alpha)


def initialize_figure(b, sminus, splus):
    plt.figure(figsize=(19 / 2.54, 10 / 2.54))
    plt.plot(b, splus, color=tum_colors[0][1], label=r'$m_S =  $' + ' 1/2')
    plt.plot(b, sminus, color=tum_colors[5][1], label=r'$m_S = -1/2$')
    y0, y1 = plt.ylim()
    x0, x1 = plt.xlim()
    plt.clf()
    return x0, x1, y0, y1


def compute_energy_shift(b, sminus, splus):
    mu_b = physical_constants['Bohr magneton in Hz/T'][0]
    g = 2
    mz = 0.5
    for i, b_val in enumerate(b):
        splus[i] = g * mu_b * mz * b_val
        sminus[i] = g * mu_b * (-mz) * b_val


def save_figure(path=None):
    if path is None:
        par_folder = os.path.dirname(__file__)
        path = os.path.join(par_folder, 'zeeman_splitting.png')
    plt.savefig(path, dpi=200)


def hertz_to_megahertz(sminus, splus):
    splus, sminus = (splus * 1e-6, sminus * 1e-6)
    return sminus, splus


def tesla_to_gauss(b):
    b = b * 10000
    return b


if __name__ == '__main__':
    main()
