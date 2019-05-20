import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190520_sample_N'
    fname = 'pulsed.028.mat'
    full_name = os.path.join(path, fname)

    mat_data = sio.loadmat(full_name)
    taus = mat_data['taus'][0]
    zs = mat_data['z'][0]
    z = np.zeros_like(taus)

    for i in range(len(taus)):
        z[i] = zs[2 * i] - zs[2 * i + 1]

    plt.close('all')
    plt.plot(taus, z)
    plt.savefig('{}.jpg'.format(fname[:-4]))


if __name__ == '__main__':
    main()
