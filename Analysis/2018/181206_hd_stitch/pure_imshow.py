import numpy as np

from utility.image_utility import plot_borderless


def main():
    a = np.ones((3, 3))
    a[1, 1] = 2
    a[0, 0] = 4
    name = 'pure_imshow'

    plot_borderless(a, name)


if __name__ == '__main__':
    main()
