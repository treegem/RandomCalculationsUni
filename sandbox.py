from constants import *

b = 1.5  # Gauss
f = 2 * MU_B * b*1e-4 / H * 1e-9
print('P1:', f)
print('NV:', 2.87 - f)
