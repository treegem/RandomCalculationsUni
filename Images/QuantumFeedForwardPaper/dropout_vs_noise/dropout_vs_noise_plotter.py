import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm


class DropoutVsNoisePlotter:
    def __init__(self):
        self.n_noises = 40
        self.n_dropouts = 16
        self.noise_angles = self.create_noise_angles()
        self.dropouts_linear = self.create_dropout_linearly_spaced()
        self.dropout_non_linear = self.create_dropout_non_linearly_spaced()
        self.dropout_angles = self.create_dropout_angles()
        self.sectors = self.create_sector_counts()

    def plot(self):
        self.plot_1d_graph_time_needed()

        self.plot_2d_imshow_noise_vs_dropout()

        self.plot_2d_imshow_noise_vs_sectors()

    def plot_2d_imshow_noise_vs_sectors(self):
        plt.clf()
        times_needed = np.zeros((self.n_noises, self.n_dropouts))
        for row in range(times_needed.shape[0]):
            for column in range(times_needed.shape[1]):
                times_needed[row, column] = min(
                    self.calc_sensitivity_with_dropout(column),
                    self.calc_sensitivity_without_dropout(row)
                )
        extent = [self.sectors[0], self.sectors[-1], self.noise_angles[0], self.noise_angles[-1]]
        plt.imshow(times_needed / times_needed.max(), origin='lower', extent=extent, aspect='auto', norm=LogNorm(),
                   interpolation='bilinear')
        plt.xlabel('sectors')
        plt.ylabel('delta angle of pure noise (degree)')
        colorbar = plt.colorbar()
        colorbar.set_label('sensitivity (arb. u.)')
        plt.savefig('noise_vs_sectors.png', dpi=300)

    def calc_sensitivity_without_dropout(self, row):
        average = self.average_signal(self.noise_angles[row])
        time_needed = np.power(1 / average, 2)
        return np.sqrt(time_needed)

    def calc_sensitivity_with_dropout(self, column):
        average = self.average_signal(self.dropout_angles[column])
        usable_percentage = 1 - self.dropout_non_linear[::-1][column]
        time_needed = np.sqrt(np.power(1 / average, 2) * np.power(1 / usable_percentage, 1))
        return np.sqrt(time_needed)

    def plot_2d_imshow_noise_vs_dropout(self):
        plt.clf()
        times_needed = np.zeros((self.n_noises, self.n_dropouts))
        for row in range(times_needed.shape[0]):
            for column in range(times_needed.shape[1]):
                times_needed[row, column] = min(
                    self.calc_time_needed_with_dropout(self.dropout_angles[column], self.dropouts_linear[column]),
                    self.calc_time_needed_without_dropout(self.noise_angles[row])
                )
        extent = [self.dropouts_linear[0], self.dropouts_linear[-1], self.noise_angles[0], self.noise_angles[-1]]
        plt.imshow(times_needed, origin='lower', extent=extent, aspect='auto', norm=LogNorm(), interpolation='bilinear')
        plt.xlabel('dropout percentage')
        plt.ylabel('delta angle of pure noise (degree)')
        colorbar = plt.colorbar()
        colorbar.set_label('time needed (arb. u.)')
        plt.savefig('noise_vs_dropout.png', dpi=300)

    def plot_1d_graph_time_needed(self):
        plt.clf()
        dropout_times = np.zeros(self.n_dropouts)
        for i in range(dropout_times.shape[0]):
            dropout_times[i] = self.calc_time_needed_with_dropout(self.dropout_angles[i], self.dropouts_linear[i])
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

    def create_dropout_linearly_spaced(self):
        return np.linspace(0, 1 - 1 / (self.n_dropouts + 1), self.n_dropouts)[::-1]  # linear spaced dropouts

    def create_dropout_non_linearly_spaced(self):
        return np.array([1 - 1 / n for n in range(1, self.n_dropouts + 1)])[::-1]  # non-linear spaced dropouts

    def create_dropout_angles(self):
        return 90 * (1 - self.dropouts_linear)

    def calc_time_needed_without_dropout(self, delta_angle):
        return self.calc_time_needed_with_dropout(delta_angle, 0)

    def create_sector_counts(self):
        return np.array([2 * n for n in range(1, self.n_dropouts + 1)])


if __name__ == '__main__':
    plotter = DropoutVsNoisePlotter()
    plotter.plot()
