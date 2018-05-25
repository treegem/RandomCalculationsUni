import numpy

PI = numpy.pi

MU_0 = 4e-7 * PI  # Magnetic field constant: N / A^2
MU_B = 9.274009994e-24  # Bohr Magneton: J·T−1

H = 6.626070040e-34  # Planck constant: J⋅s
H_BAR = 1.0545718e-34  # Planck constant / 2 pi: J⋅s/rad

GYRO_FACT = {'nv': 2.8e6 / 1e-4}

G = {'nv': GYRO_FACT['nv'] * H / MU_B}


