"""
Comparing 181001/002 and 181004/001
"""

import os

import numpy as np
import matplotlib.pyplot as plt


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181001_d36_osci_plus_deer_sweep/002_deer_sweep'
    last_sweep = os.path.join(path, 'last_sweep.txt')
    data_no_curr = np.loadtxt(last_sweep)

    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181004_d36_deer_sweep_20mA/001_deer_sweep_20mA'
    last_sweep = os.path.join(path, 'last_sweep.txt')
    data_with_curr = np.loadtxt(last_sweep)

    fig = plt.figure()
    plt.plot(data_no_curr[:, 0] * 1e-9, data_no_curr[:, 1] - data_no_curr[:, 2], label='No Current')
    plt.plot(data_with_curr[:, 0] * 1e-9, data_with_curr[:, 1] - data_with_curr[:, 2], label='20 mA')
    plt.xlabel('RF frequency (GHz)')
    plt.ylabel('Contrast')
    plt.legend()
    plt.axes().set_aspect(3)
    fig.savefig('deer_comparison.png', dpi=300, bbox_inches='tight')
    np.savetxt('data_no_curr.txt', data_no_curr)
    np.savetxt('data_with_curr.txt', data_with_curr)


if __name__ == '__main__':
    main()
