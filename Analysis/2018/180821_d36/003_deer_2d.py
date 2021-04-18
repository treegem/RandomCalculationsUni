import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    mes_per_mode = 6
    pure_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180821_d36/003_deer_2d'
    pure_names = relevant_filenames(name='mes_{:03}.mat', ind_min=mes_per_mode, ind_max=2 * mes_per_mode - 1)
    pure_differences = get_differences(pure_names, pure_path)
    taus = get_taus(pure_names, pure_path)
    plt.close('all')
    plt.imshow(pure_differences, extent=[taus[0], taus[-1], 500, 5500], origin='lower', aspect='auto',
               vmin=None, vmax=None)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pure counts')
    plt.colorbar()
    plt.savefig('ramsey_correlation_pure.png', dpi=300)

    pi_path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180821_d36/003_deer_2d'
    pi_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=mes_per_mode - 1)
    pi_differences = get_differences(pi_names, pi_path)
    plt.close('all')
    plt.imshow(pi_differences, extent=[taus[0], taus[-1], 500, 3000], origin='lower', aspect='auto',
               vmin=None, vmax=None)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pi counts')
    plt.colorbar()
    plt.savefig('ramsey_correlation_pi.png', dpi=300)

    # difference
    total_difference = pure_differences - pi_differences
    plt.close('all')
    plt.imshow(total_difference, extent=[taus[0], taus[-1], 500, 3000], origin='lower', aspect='auto',
               vmin=None, vmax=None)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pure - pi')
    plt.colorbar()
    plt.savefig('ramsey_correlation_difference.png', dpi=300)


if __name__ == '__main__':
    main()
