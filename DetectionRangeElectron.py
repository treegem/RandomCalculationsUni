import numpy as np
from scipy.optimize import minimize_scalar

from utility.constants import *


def sensitivity_from_t2(t2):
    # return PI * H_BAR / (G['nv'] * MU_B * np.sqrt(t2))
    return 1 / (2 * GYRO_FACT['nv'] * t2)


def range_from_b_field(min_b_field):
    res = minimize_scalar(fun=lambda r: np.abs(min_b_field - static_magnetic_dipole_field(r*1e-5)),
                          bounds=(1e-15, 1))
    res.x *= 1e-5
    return res.x


def static_magnetic_dipole_field(r):
    return MU_0 * MU_B / (2 * PI * np.power(r, 3))


def detection_range(t2):
    min_b_field = sensitivity_from_t2(t2)
    return range_from_b_field(min_b_field)


if __name__ == '__main__':
    T2 = [10e-6, 1e-3, 30e-3]
    results = {}
    for t in T2:
        results[str(t)] = detection_range(t)
    for key in results:
        print(key, results[key])

