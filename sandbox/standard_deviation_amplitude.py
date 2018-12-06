import numpy as np


def main():
    xdata = np.linspace(0, 10000, 100000)
    a = 107.56
    ydata = a * np.sin(xdata)
    print(xdata)
    print(ydata)
    print(np.std(ydata) * np.sqrt(2))


if __name__ == '__main__':
    main()
