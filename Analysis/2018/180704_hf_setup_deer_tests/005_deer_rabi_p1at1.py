import os

import matplotlib.pyplot as plt

import utility.mat_handling as mhand


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/180704_hf_setup_deer_tests/005_deer_rabi_p1at1'
    fname = 'mes_000.mat'
    full_path = os.path.join(path, fname)
    data = mhand.load_mat_file(full_path)
    diffs = mhand.extract_difference(data)
    taus = mhand.extract_taus(data)
    plt.plot(taus, diffs)
    plt.savefig('{}.png'.format(path.split('/')[-1]), dpi=300)


if __name__ == '__main__':
    main()
