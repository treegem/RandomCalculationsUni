import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm


class DropoutVsNoisePlotter:
    def __init__(self):
        self.n_noises = 40
        self.n_dropouts = 40
        self.noise_angles = self.create_noise_angles()
        self.dropouts = self.create_dropouts()
        self.dropout_angles = self.create_dropout_angles()

    def plot(self):
        self.plot_1dgraph_time_needed()

        self.plot_2dimshow_noise_vs_dropout()

    def plot_2dimshow_noise_vs_dropout(self):
        plt.clf()
        times_needed = np.zeros((self.n_noises, self.n_dropouts))
        for row in range(times_needed.shape[0]):
            for column in range(times_needed.shape[1]):
                times_needed[row, column] = min(
                    self.calc_time_needed_with_dropout(self.dropout_angles[column], self.dropouts[column]),
                    self.calc_time_needed_without_dropout(self.noise_angles[row])
                )
        extent = [self.dropouts[0], self.dropouts[-1], self.noise_angles[0], self.noise_angles[-1]]
        plt.imshow(times_needed, origin='lower', extent=extent, aspect='auto', norm=LogNorm(), interpolation='bilinear')
        plt.xlabel('dropout percentage')
        plt.ylabel('delta angle of pure noise (degree)')
        colorbar = plt.colorbar()
        colorbar.set_label('time needed (arb. u.)')
        plt.savefig('noise_vs_dropout.png', dpi=300)

    def plot_1dgraph_time_needed(self):
        plt.clf()
        dropout_times = np.zeros(self.n_dropouts)
        for i in range(dropout_times.shape[0]):
            dropout_times[i] = self.calc_time_needed_with_dropout(self.dropout_angles[i], self.dropouts[i])
        plt.plot(self.dropout_angles, dropout_times, label='dropouts')
        noise_times = np.zeros(self.noise_angles.shape[0])
        for i, angle in enumerate(self.noise_angles):
            noise_times[i] = self.calc_time_needed_without_dropout(angle)
        plt.plot(self.noise_angles, noise_times, label='pure_noise')
        plt.xlabel('delta angle (degree)')
        plt.ylabel('time needed (arb. u.)')
        plt.legend()
        plt.savefig('times_needed.png', dpi=300)

    def calc_time_needed_with_dropout(self, delta_angle, dropout):
        average = self.average_signal(delta_angle)
        usable_percentage = 1 - dropout
        time_needed = np.power(1 / average, 2) * np.power(1 / usable_percentage, 1)
        return time_needed

    @staticmethod
    def average_signal(delta_angle, sample_points=1000):
        xs = np.linspace(0, delta_angle * np.pi / 180, sample_points)
        ys = np.cos(xs)
        return np.average(ys)

    def create_noise_angles(self):
        return np.linspace(90, 145, self.n_noises)

    def create_dropouts(self):
        # return np.array([1 - 1 / n for n in range(1, self.n_dropouts + 1)])[::-1]  # non-linear spaced dropouts
        return np.linspace(0, 1 - 1 / (self.n_dropouts + 1), self.n_dropouts)[::-1]  # linear spaced dropouts

    def create_dropout_angles(self):
        return 90 * (1 - self.dropouts)

    def calc_time_needed_without_dropout(self, delta_angle):
        return self.calc_time_needed_with_dropout(delta_angle, 0)


if __name__ == '__main__':
    plotter = DropoutVsNoisePlotter()
    plotter.plot()
