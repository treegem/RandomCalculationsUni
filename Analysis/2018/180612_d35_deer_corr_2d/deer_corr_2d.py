import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    pure_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180612_d35_deer_corr_2d/001_deer_corr_2d'
    pure_names = relevant_filenames(name='mes_{:03}.mat', ind_min=10, ind_max=19)
    pure_differences = get_differences(pure_names, pure_path)
    taus = get_taus(pure_names, pure_path)
    plt.close('all')
    plt.imshow(pure_differences, extent=[taus[0], taus[-1], 500, 10000], origin='lower', aspect='auto',
               vmin=None, vmax=None)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pure counts')
    plt.colorbar()
    plt.savefig('ramsey_correlation_pure.png', dpi=300)

    pi_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180612_d35_deer_corr_2d/001_deer_corr_2d'
    pi_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=9)
    pi_differences = get_differences(pi_names, pi_path)
    plt.close('all')
    plt.imshow(pi_differences, extent=[taus[0], taus[-1], 500, 10000], origin='lower', aspect='auto',
               vmin=None, vmax=None)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pi counts')
    plt.colorbar()
    plt.savefig('ramsey_correlation_pi.png', dpi=300)

    # difference
    total_difference = pure_differences - pi_differences
    plt.close('all')
    plt.imshow(total_difference, extent=[taus[0], taus[-1], 500, 10000], origin='lower', aspect='auto',
               vmin=None, vmax=None)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pure - pi')
    plt.colorbar()
    plt.savefig('ramsey_correlation_difference.png', dpi=300)


if __name__ == '__main__':
    main()
