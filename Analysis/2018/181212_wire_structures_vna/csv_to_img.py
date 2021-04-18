import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/group_members/Georg/Documentation/18121_wire_structures'
    file_names = os.listdir(path)
    for f_name in file_names:
        f_path = os.path.join(path, f_name)
        data = np.loadtxt(f_path, delimiter=',', skiprows=8)
        plt.close('all')
        plt.plot(data[:, 0] * 1e-9, data[:, 1], label='S11')
        plt.plot(data[:, 0] * 1e-9, data[:, 2], label='S12')
        plt.plot(data[:, 0] * 1e-9, data[:, 3], label='S21')
        plt.plot(data[:, 0] * 1e-9, data[:, 4], label='S22')
        plt.legend()
        plt.xlabel('f (GHz)')
        plt.ylabel('S-parameters (dB)')
        plt.savefig('{}.png'.format(f_name.split('.csv')[0]), dpi=300)



if __name__ == '__main__':
    main()
