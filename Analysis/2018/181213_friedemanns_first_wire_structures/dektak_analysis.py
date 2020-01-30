import os
import numpy as np
import matplotlib.pyplot as plt

def main():
    path = '//file/e24/Projects/ReinhardLab/group_members/Georg/Documentation/' \
           '181213_friedemanns_first_in_situ_lithography'
    files = os.listdir(path)
    for f in files:
        data = np.loadtxt(os.path.join(path, f), skiprows=19, delimiter=',', usecols=[0, 1])
        plt.close('all')
        plt.plot(data[:, 0], data[:, 1])
        plt.xlabel('Lateral (um)')
        plt.ylabel('Height (nm)')
        plt.savefig('{}.png'.format(f.split('.')[0]))


if __name__ == '__main__':
    main()
