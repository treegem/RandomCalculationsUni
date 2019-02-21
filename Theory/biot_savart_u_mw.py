import matplotlib.pyplot as plt
import numpy as np


def current_density(r: np.ndarray):
    if r[0] == 0 and r[1] == 0:
        return 1
    else:
        return 0


def main():
    pass


if __name__ == '__main__':
    main()
    plt.close('all')
