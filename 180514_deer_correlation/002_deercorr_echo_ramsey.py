import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180514_deer_correlation/' \
           '002_deercorr_echo_ramsey'
    names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    echo_differences = get_differences(names, path)[0]
    taus = get_taus(names, path)
    plt.close('all')
    plt.plot(taus, echo_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('002_echo.png', dpi=300)

    path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180514_deer_correlation/' \
           '002_deercorr_echo_ramsey'
    names = relevant_filenames(name='mes_{:03}.mat', ind_min=1, ind_max=1)
    pure_differences = get_differences(names, path)[0]
    taus = get_taus(names, path)
    plt.close('all')
    plt.plot(taus, pure_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('002_ramsey.png', dpi=300)


if __name__ == '__main__':
    main()
