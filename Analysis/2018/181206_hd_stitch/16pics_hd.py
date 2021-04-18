import os

import scipy.io as sio

from utility.image_utility import plot_borderless


def main():
    path = '//nas.ads.mwn.de/TUZE/wsi/e24/ReinhardLab/data_setup_nv1/181206_hd_scans_pc/16pics_hd'
    mat_files = get_mat_filenames(path)
    for mat_file in mat_files:
        mes_data = load_result(path, mat_file)
        plot_borderless(mes_data, '16pics/{}_borderless.png'.format(mat_file.split('.mat')[0]), vmax=1e6, dpi=1000)


def load_result(dir, mat_file):
    full_data = sio.loadmat(os.path.join(dir, mat_file))
    mes_data = full_data['result']
    return mes_data


def get_mat_filenames(dir):
    all_files = os.listdir(dir)
    mat_files = []
    for f in all_files:
        if f.endswith('mat'):
            mat_files.append(f)
    return mat_files


if __name__ == '__main__':
    main()
