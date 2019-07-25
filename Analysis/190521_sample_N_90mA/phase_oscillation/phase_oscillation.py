import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/190521_sample_N_90mA/phase_oscillation_001'
    zs = np.loadtxt(os.path.join(path, 'zs.txt'))

    start_index = 6
    end_index = -1

    plt.close('all')
    plt.plot(zs[start_index:end_index])
    plt.savefig('phase_oscillation.jpg', dpi=300)


if __name__ == '__main__':
    main()
