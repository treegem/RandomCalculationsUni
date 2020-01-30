import matplotlib.pyplot as plt
import numpy as np


def main():
    i_s = np.array([8, 12, 16, 19.4, 42])
    b_s = np.array([15, 25, 35, 40, 68])

    plt.close('all')
    plt.plot(i_s, b_s, 'r--')
    plt.plot(i_s, b_s, '.')
    plt.xlabel('current [mA]')
    plt.ylabel('b (G)')
    plt.savefig('b_vs_i.png', dpi=300)


if __name__ == '__main__':
    main()