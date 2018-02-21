import matplotlib.pyplot as plt
import numpy as np

# given
sigma_delta = 1
tau = 6
t0 = 10


def p_delta(delta):
    return np.power(sigma_delta * np.sqrt(2 * np.pi), -1) * np.exp(-np.power(delta, 2) / (2 * np.power(sigma_delta, 2)))


# computations
def main():
    plot_detuning_distribution()
    # plot_phase_collection_time()
    # plot_phase_collection_time_squared()

    taus = np.linspace(0, tau, 10000)
    ys = np.zeros_like(taus)
    for taui, t in enumerate(taus):
        ys[taui] = phase_collection_time_2(t)
    plt.close('all')
    plt.plot(taus, ys)
    plt.show()


def phase_collection_time_2(starting_time):
    if 0 <= starting_time < (2 * tau - t0) / 2:
        return 2 * tau - t0 - 2 * starting_time
    elif (2 * tau - t0) / 2 <= starting_time < 2 * tau - t0:
        return 2 * (starting_time - (2 * tau - t0) / 2)
    else:
        return 2 * tau - t0


def plot_phase_collection_time():
    xs = np.linspace(0., t0, 100)
    ys = np.zeros_like(xs)
    for xi, x in enumerate(xs):
        ys[xi] = phase_collection_time(x)
    plt.close('all')
    plt.plot(xs, ys)
    plt.xlabel('starting time')
    plt.ylabel('phase collection time')
    plt.savefig('phase_collection_time.png')


def plot_phase_collection_time_squared():
    xs = np.linspace(0., t0, 100)
    ys = np.zeros_like(xs)
    for xi, x in enumerate(xs):
        ys[xi] = phase_collection_time(x)
    plt.close('all')
    plt.plot(xs, ys ** 2)
    plt.xlabel('starting time')
    plt.ylabel('phase collection time^2')
    plt.savefig('phase_collection_time_squared.png')


def phase_collection_time(starting_time):
    if 0 <= starting_time < t0 - 2 * tau:
        return 0
    if t0 - 2 * tau <= starting_time < t0 - tau:
        return starting_time - (t0 - 2 * tau)
    if t0 - tau <= starting_time <= t0:
        return t0 - starting_time


def plot_detuning_distribution():
    plt.close('all')
    xs = np.linspace(-5, 5, 100)
    ys = p_delta(xs)
    plt.plot(xs, ys)
    plt.xlabel('detuning')
    plt.ylabel('p(delta)')
    plt.savefig('detuning_distribution.png')


if __name__ == '__main__':
    main()
