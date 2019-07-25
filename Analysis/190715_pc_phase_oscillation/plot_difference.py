import os

import matplotlib.pyplot as plt
import numpy as np


def main():
    times = ['0', '2500', '5000', '7500', '10000', '13000', '16000', '19000', '24500', '30000']

    for time in times:

        # tau reconstruction
        taus = np.loadtxt('{}_pi2_taus.txt'.format(time))
        pi2 = np.loadtxt('{}_pi2_tau_zs.txt'.format(time))
        pi32 = np.loadtxt('{}_3pi2_tau_zs.txt'.format(time))

        pi2_avg = np.average(pi2)
        pi32_avg = np.average(pi32)

        pi32 = pi32 - pi32_avg + pi2_avg

        plt.close('all')
        plt.plot(taus, pi2)
        plt.plot(taus, pi32)
        plt.savefig('{}_both.jpg'.format(time))

        plt.close('all')
        plt.plot(taus, pi2 - pi32)
        plt.savefig('{}_difference.jpg'.format(time))

        # qff

        start = 10
        end = -10

        pi2_qff = np.loadtxt('{}_pi2_zs.txt'.format(time))[start:end]
        pi32_qff = np.loadtxt('{}_3pi2_zs.txt'.format(time))[start:end]

        pi2_qff_avg = np.average(pi2_qff)
        pi32_qff_avg = np.average(pi32_qff)

        pi32_qff = pi32_qff - pi32_qff_avg + pi2_qff_avg

        plt.close('all')
        plt.plot(pi2_qff)
        plt.plot(pi32_qff)
        plt.savefig('{}_both_qff.jpg'.format(time))

        plt.close('all')
        plt.plot(pi2_qff - pi32_qff)
        plt.savefig('{}_difference_qff.jpg'.format(time))


def combine_pulsed_name(path, pulsed_index):
    return os.path.join(path, 'pulsed.{:03}.mat'.format(pulsed_index))


if __name__ == '__main__':
    main()
