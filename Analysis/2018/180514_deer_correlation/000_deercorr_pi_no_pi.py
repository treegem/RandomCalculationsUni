import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180514_deer_correlation/' \
           '000_deercorr_pi_no_pi'
    names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    pi_differences = get_differences(names, path)[0]
    taus = get_taus(names, path)
    plt.close('all')
    plt.plot(taus, pi_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('000_with_pi.png', dpi=300)

    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180514_deer_correlation/' \
           '000_deercorr_pi_no_pi'
    names = relevant_filenames(name='mes_{:03}.mat', ind_min=1, ind_max=1)
    pure_differences = get_differences(names, path)[0]
    taus = get_taus(names, path)
    plt.close('all')
    plt.plot(taus, pure_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('000_no_pi.png', dpi=300)

    plt.close('all')
    plt.plot(taus, pure_differences - pi_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('000_difference.png', dpi=300)


if __name__ == '__main__':
    main()
