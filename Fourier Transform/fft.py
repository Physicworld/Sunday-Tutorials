import numpy as np

import matplotlib.pyplot as plt
plt.style.use('classic')

class Wave:
    def __init__(self):
        # Amplitud Desfase Freq. Angular
        self.params = [np.random.rand(), np.random.rand(), np.random.rand()]

    def evaluate(self, x):
        return self.params[0] * np.sin(self.params[1] + 2 * np.pi * x * self.params[2])


def main():
    n_waves = 50

    waves = [Wave() for i in range(n_waves)]

    x = np.linspace(-10, 10, 500)
    y = np.zeros_like(x)

    for wave in waves:
        y += wave.evaluate(x)

    # TRANFORMADA RAPIDA DE FOURIER

    f = np.fft.fft(y)
    freq = np.fft.fftfreq(len(y), d = x[1] - x[0])

    fig, ax = plt.subplots(2)

    for wave in waves:
        ax[0].plot(wave.evaluate(x), color = 'black', alpha = 0.3)

    ax[0].plot(y, color = 'blue')
    ax[1].plot(freq, abs(f)**2)
    plt.show()


if __name__ == '__main__':
    main()
