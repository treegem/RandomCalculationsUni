import os
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np


def normalization_factor(no_curr, curr):
    no_curr_avg = np.average(counts_of(no_curr)[:10])
    curr_avg = np.average(counts_of(curr)[:10])
    return no_curr_avg / curr_avg


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190122_mw_structure_test'
    no_current_files = ['odmr.007.mat', 'odmr.009.mat', 'odmr.011.mat']
    current_files = ['odmr.008.mat', 'odmr.010.mat', 'odmr.012.mat']

    for i, (no_curr, curr) in enumerate(zip(no_current_files, current_files)):
        no_curr = sio.loadmat(os.path.join(path, no_curr))
        curr = sio.loadmat(os.path.join(path, curr))
        norm_fac = normalization_factor(no_curr, curr)
        plt.close('all')
        plt.plot(frequency_of(no_curr), counts_of(no_curr), label='0 mA')
        plt.plot(frequency_of(curr), counts_of(curr) * norm_fac, label = '30 mA')
        plt.legend()
        plt.savefig('take_{}.jpg'.format(i), dpi=300)


def frequency_of(loaded_mat):
    return loaded_mat['fs'][0, 1:]


def counts_of(loaded_mat):
    return loaded_mat['ci'][0]


if __name__ == '__main__':
    main()
