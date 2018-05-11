import os

import errno
import scipy.io as sio
import numpy as np


def load_mat_file(name):
    if os.path.isfile(name):
        return sio.loadmat(name)
    else:
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), name)


def extract_property(mat, prop):
    if prop in mat:
        if len(mat[prop]) == 1:
            return mat[prop][0]
        else:
            return mat[prop]
    else:
        raise NameError('mat file does not contain \'{}\''.format(prop))


def extract_zs(mat):
    return extract_property(mat, 'zs')


def extract_difference(mat):
    """
    For measurements with two sequences, this returns the difference between the two curves.
    """
    zs = extract_zs(mat)

    if len(zs) != 2:
        raise Exception('Lengths of \'zs\' not equal to two.')

    difference = np.zeros((len(zs[0])))
    for i, (z0, z1) in enumerate(zip(zs[0], zs[1])):
        difference[i] = z0 - z1

    return difference


def extract_taus(mat):
    return extract_property(mat, 'taus')
