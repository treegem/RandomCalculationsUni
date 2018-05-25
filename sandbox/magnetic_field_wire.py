import numpy as np

from utility.constants import *


def magnetic_field(I, r):
    return tesla_to_gauss(MU_0 * I / (2 * PI * r))


def magnetic_gradient(I, r):
    return tesla_to_gauss(- (MU_0 * I) / (2 * PI * np.power(r, 2)))


def tesla_to_gauss(b_tesla):
    return b_tesla * 1e4


def zeeman_shift(b):
    """
    :param b: gauss
    """
    return 2.8e6 * b


def zeeman_uncertainty(shift, dI):
    return shift * dI


def main():
    r = 500e-9
    # I = 100e-3
    I = 250e-6
    dI = 0.1e-2  # percent

    # calculations
    field = magnetic_field(I, r)
    print("Magnetic field: ", field, 'G')

    gradient = magnetic_gradient(I, r)
    print("Gradient field: ", gradient * 1e-9, 'G / nm')

    shift = zeeman_shift(field)
    print("P1 center frequency: ", shift * 1e-9, 'GHz')

    uncertainty = zeeman_uncertainty(shift, dI)
    print("P1 frequency uncertainty: +/-", uncertainty * 1e-6, 'MHz')

    print("dx: +/-", uncertainty / (2.8e6 * gradient) * 1e9, 'nm')


if __name__ == '__main__':
    main()
