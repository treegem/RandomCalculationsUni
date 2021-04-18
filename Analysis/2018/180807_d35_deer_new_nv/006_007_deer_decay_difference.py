import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path_res = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180807_d35_deer_new_nv/' \
               '006_deer_decay_on'
    names_res = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    res_differences = get_differences(names_res, path_res)[0]
    taus = get_taus(names_res, path_res)
    plt.close('all')
    plt.plot(taus, res_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('006_deer_echo_with_pi.png', dpi=300)

    path_nonres = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180807_d35_deer_new_nv/' \
                  '007_deer_decay_off'
    names_nonres = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=0)
    nonres_differences = get_differences(names_nonres, path_nonres)[0]
    taus = get_taus(names_nonres, path_nonres)
    plt.close('all')
    plt.plot(taus, nonres_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('007_deer_echo_without_pi.png', dpi=300)

    plt.close('all')
    plt.plot(taus, nonres_differences - res_differences)
    plt.xlabel('tau in sequence (ns)')
    plt.savefig('006_007_deer_decay_difference.png', dpi=300)

    plt.close('all')
    plt.plot(taus, nonres_differences, label='nonres')
    plt.plot(taus, res_differences, label='res')
    plt.xlabel('tau in sequence (ns)')
    plt.legend()
    plt.savefig('006_007_both_decays.png', dpi=300)


if __name__ == '__main__':
    main()
