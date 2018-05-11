import os

import matplotlib.pyplot as plt
import numpy as np

import utility.mat_handling as mat


def main():
    pure_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180508_deer_2d_plot/deer_2d_plot'
    pure_names = relevant_filenames(name='mes_{:03}.mat', ind_min=10, ind_max=19)
    pure_differences = get_differences(pure_names, pure_path)

    pi_path = '//file/e24/Projects/ReinhardLab/data_setup_nv1/180508_deer_2d_plot/deer_2d_plot'
    pi_names = relevant_filenames(name='mes_{:03}.mat', ind_min=20, ind_max=29)
    pi_differences = get_differences(pi_names, pi_path)

    taus = get_taus(pure_names, pure_path)
    relational_differences = pi_differences / pure_differences

    plt.imshow(relational_differences, extent=[taus[0], taus[-1], 50, 20000], origin='lower', aspect=0.25,
               vmin=-1, vmax=1)
    plt.xlabel('tau in sequence (ns)')
    plt.ylabel('tau between sequences (ns)')
    plt.colorbar()
    plt.savefig('ramsey_correlation_relation.png', dpi=300)




def get_taus(names, path):
    fullname = os.path.join(path, names[0])
    mat_file = mat.load_mat_file(fullname)
    taus = mat.extract_property(mat_file, 'taus')
    return taus


def get_differences(names, path):
    differences = []
    for fname in names:
        fullname = os.path.join(path, fname)
        mat_file = mat.load_mat_file(fullname)
        difference = mat.extract_difference(mat_file)
        differences.append(difference)
    differences = np.array(differences)
    return differences


def relevant_filenames(name, ind_min, ind_max):
    names = []
    for i in range(ind_min, ind_max + 1):
        names.append(name.format(i))
    return names


if __name__ == '__main__':
    main()
