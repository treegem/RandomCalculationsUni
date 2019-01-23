import numpy as np
import matplotlib.pyplot as plt


def growth(taus):
    result = np.ones_like(taus)
    upgrade = 0.15
    rate = 1
    for i, tau in enumerate(taus):
        if tau == 0:
            old_selling_price = 1
            continue
        selling_price = old_selling_price + upgrade
        result[i] = result[i - 1] + rate * (selling_price)
        old_selling_price = selling_price
    return result


def main():
    taus = np.linspace(0, 1000, 1000)
    moneyz = growth(taus)
    plt.plot(taus, moneyz)
    plt.show()


if __name__ == '__main__':
    main()
