import os

import numpy as np

import utility.mat_handling as mat


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
