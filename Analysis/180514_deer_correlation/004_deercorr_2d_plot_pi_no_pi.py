import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    pi_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180514_deer_correlation/004_deercorr_2d_plot_pi_no_pi'
    pi_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=19)
    pi_differences = get_differences(pi_names, pi_path)
    taus = get_taus(pi_names, pi_path)
    plt.close('all')
    plt.imshow(pi_differences, extent=[taus[0], taus[-1], 1000, 20000], origin='lower', aspect='auto')
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('tau between sequences (ns)')
    plt.colorbar()
    plt.savefig('004_pi_differences.png', dpi=300)

    pure_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180514_deer_correlation/004_deercorr_2d_plot_pi_no_pi'
    pure_names = relevant_filenames(name='mes_{:03}.mat', ind_min=20, ind_max=39)
    pure_differences = get_differences(pure_names, pure_path)
    plt.close('all')
    plt.imshow(pure_differences, extent=[taus[0], taus[-1], 1000, 20000], origin='lower', aspect='auto')
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('tau between sequences (ns)')
    plt.colorbar()
    plt.savefig('004_pure_differences.png', dpi=300)

    # difference
    total_difference = pure_differences - pi_differences
    plt.close('all')
    plt.imshow(total_difference, extent=[taus[0], taus[-1], 1000, 20000], origin='lower', aspect='auto')
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pure - pi')
    plt.colorbar()
    plt.savefig('004_difference.png', dpi=300)


if __name__ == '__main__':
    main()
