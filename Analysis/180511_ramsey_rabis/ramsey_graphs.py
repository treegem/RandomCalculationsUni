import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    pure_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180511_ramsey_correlations_rabi/' \
                '002_ramsey_correlation_tcorr_sweep'
    pure_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    pure_differences = get_differences(pure_names, pure_path)[0]

    pi_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180511_ramsey_correlations_rabi/' \
              '003_ramsey_correlation_tcorr_sweep'
    pi_names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    pi_differences = get_differences(pi_names, pi_path)[0]

    # both graphs
    pure_taus = get_taus(pure_names, pure_path)
    pi_taus = get_taus(pi_names, pi_path)
    plt.close('all')
    plt.plot(pure_taus, pure_differences, label='pure')
    plt.plot(pi_taus, pi_differences, label='with pi')
    plt.xlabel('tau in sequence (ns)')
    plt.legend()
    plt.savefig('ramsey_graphs.png', dpi=300)

    # difference
    plt.close('all')
    print(pure_taus - pi_taus[::2])
    plt.plot(pure_taus, pure_differences - pi_differences[::2])
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('ramsey_graphs_difference.png', dpi=300)

if __name__ == '__main__':
    main()
