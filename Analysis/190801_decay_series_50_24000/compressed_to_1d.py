import matplotlib.pyplot as plt
import numpy as np


def main():
    compress_to_1d('50_250')
    compress_to_1d('5000_5200')
    compress_to_1d('10000_10200')
    compress_to_1d('15000_15200')
    compress_to_1d('20000_20200')
    compress_to_1d('23800_24000')


def compress_to_1d(folder):
    compress_qff(folder)
    compress_taus(folder)


def compress_taus(folder):
    zs = np.loadtxt('{}/{}_taus.txt'.format(folder, folder))[:, :-1]
    if folder == '50_250':
        zs = np.delete(zs, 1, axis=0)
    zs = np.average(zs, axis=0)
    np.savetxt('{}/{}_taus_compressed.txt'.format(folder, folder), zs)
    plt.close('all')
    plt.plot(zs)
    plt.savefig('{}/{}_taus_compressed.png'.format(folder, folder))


def compress_qff(folder):
    zs = np.loadtxt('{}/{}.txt'.format(folder, folder))[:, :]
    if folder == '50_250':
        zs = np.delete(zs, 1, axis=0)
    zs = np.average(zs, axis=0)
    zs = remove_outliers(zs)
    np.savetxt('{}/{}_compressed.txt'.format(folder, folder), zs)
    plt.close('all')
    plt.plot(zs)
    plt.savefig('{}/{}_compressed.png'.format(folder, folder))


def remove_outliers(zs):
    while is_out_of_range(zs):
        zs = zs[:-1]
    return zs


def is_out_of_range(zs):
    min_ = 0.8
    max_ = 1.
    out_of_range = True in (zs < min_) or True in (zs > max_)
    return out_of_range


if __name__ == '__main__':
    main()
