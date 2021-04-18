import matplotlib.pyplot as plt

from utility.deer_2d_plots import *


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180511_deer_2d_plot_ramsey/deer_ramsey_with_pi_008'
    names = relevant_filenames(name='mes_{:03}.mat', ind_min=0, ind_max=9)
    taus = get_taus(names, path)
    differences = get_differences(names, path)
    # plt.plot(taus, differences[-1, :])
    # plt.show()
    plt.close('all')
    plt.imshow(differences, extent=[taus[0], taus[-1], 270, 20000], origin='lower', aspect='auto', vmin=0.02, vmax=0.18)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('tau between sequences (ns)')
    plt.colorbar()
    plt.savefig('pi_ramsey_correlation.png', dpi=300)


if __name__ == '__main__':
    main()
