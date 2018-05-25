import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    pure_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180511_deer_2d_plot_ramsey/deer_pure_ramsey_007'
    pure_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=9)
    pure_differences = get_differences(pure_names, pure_path)

    pi_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180511_deer_2d_plot_ramsey/deer_ramsey_with_pi_008'
    pi_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=9)
    pi_differences = get_differences(pi_names, pi_path)

    # relational
    taus = get_taus(pure_names, pure_path)
    relational_differences = pi_differences / pure_differences
    plt.close('all')
    plt.imshow(relational_differences, extent=[taus[0], taus[-1], 270, 20000], origin='lower', aspect='auto',
               vmin=0.5, vmax=1.1)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pi/pure')
    plt.colorbar()
    plt.savefig('ramsey_correlation_relation.png', dpi=300)

    # difference
    total_difference = pure_differences - pi_differences
    plt.close('all')
    plt.imshow(total_difference, extent=[taus[0], taus[-1], 270, 20000], origin='lower', aspect='auto',
               vmin=-0.01, vmax=0.038)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('pure - pi')
    plt.colorbar()
    plt.savefig('ramsey_correlation_difference.png', dpi=300)


if __name__ == '__main__':
    main()
