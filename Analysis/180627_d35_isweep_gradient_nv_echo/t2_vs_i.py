import matplotlib.pyplot as plt
import numpy as np


def main():
    i_s = np.array([8, 12, 16, 19.4, 42])
    t2_s = np.array([4.44e-7, 3.40e-7, 2.56e-7, 2.02e-7, 1.42e-7]) * 1e9

    plt.close('all')
    plt.plot(i_s, t2_s, '.')
    plt.xlabel('current [mA]')
    plt.ylabel('T_2 (ns)')
    plt.savefig('t2_vs_i.png', dpi=300)


if __name__ == '__main__':
    main()