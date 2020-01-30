import os

import numpy as np
import matplotlib.pyplot as plt


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/181004_d36_deer_sweep_20mA/001_deer_sweep_20mA'
    last_sweep = os.path.join(path, 'last_sweep.txt')
    data = np.loadtxt(last_sweep)
    fig = plt.figure()
    plt.plot(data[:, 0] * 1e-9, data[:, 1] - data[:, 2])
    plt.xlabel('RF frequency (GHz)')
    plt.ylabel('Contrast')
    plt.axes().set_aspect(3)
    fig.savefig('deer_sweep.png', dpi=300, bbox_inches='tight')
    processed_data = np.vstack((data[:, 0], data[:, 1] - data[:, 2])).T
    np.savetxt('20mA_current.txt', processed_data)


if __name__ == '__main__':
    main()
