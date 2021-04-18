import os

import numpy as np
import matplotlib.pyplot as plt


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181001_d36_osci_plus_deer_sweep/002_deer_sweep'
    last_sweep = os.path.join(path, 'last_sweep.txt')
    data = np.loadtxt(last_sweep)
    fig = plt.figure()
    plt.plot(data[:, 0] * 1e-9, data[:, 1] - data[:, 2])
    plt.xlabel('RF frequency (GHz)')
    plt.ylabel('Contrast')
    plt.axes().set_aspect(3)
    fig.savefig('deer_sweep.png', dpi=300, bbox_inches='tight')
    processed_data = np.vstack((data[:, 0], data[:, 1] - data[:, 2])).T
    np.savetxt('no_current.txt', processed_data)


if __name__ == '__main__':
    main()
