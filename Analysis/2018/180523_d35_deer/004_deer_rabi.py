import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180523_d35_deer/' \
           '004_deer_rabi'
    names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    pi_differences = get_differences(names, path)[0]
    taus = get_taus(names, path)
    plt.close('all')
    plt.plot(taus, pi_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('004_deer_rabi.png', dpi=300)


if __name__ == '__main__':
    main()
