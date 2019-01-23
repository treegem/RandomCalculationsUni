import numpy as np


def main():
    focus_diameter = 0.1  # mm
    maximum_power_density = 5  # W / mm^2

    area = np.pi * np.power(focus_diameter / 2, 2)
    maximum_power = maximum_power_density * area

    print(maximum_power)


if __name__ == '__main__':
    main()
