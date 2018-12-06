from utility.constants import *

b = 542  # Gauss
f = 2 * MU_B * b*1e-4 / H * 1e-9
print('P1:', f)
print('NV low:', 2.87 - f)
print('NV high: ', 2.87 + f)
