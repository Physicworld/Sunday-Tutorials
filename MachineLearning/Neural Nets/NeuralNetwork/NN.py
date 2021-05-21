import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_circles

def sigmoid(x, deriv = False):
    if deriv:
        return x * (1-x)
    return 1/(1+np.e**-x)

def tanh(x, deriv = False):
    if deriv:
        return (1 - (np.tanh(x))**2)
    return np.tanh(x)

def MSE(Yp, Yr, deriv = False):
    if deriv:
        return (Yp - Yr)
    return np.mean((Yp-Yr)**2)

class Layer:
    def __init__(self, con, neuron):
        self.b = np.random.rand(1, neuron) * 2 - 1
        self.W = np.random.rand(con, neuron) * 2 - 1

class NeuralNetwork:
    def __init__(self, top = [], act_fun = sigmoid):
        self.top = top
        self.act_fun = act_fun
        self.model = self.define_model()

    def define_model(self):

        NeuralNetwork = []

        for i in range(len(self.top[:-1])):
            NeuralNetwork.append(Layer(self.top[i], self.top[i+1]))
        return NeuralNetwork

    def predict(self, X = []):

        out = X

        for i in range(len(self.model)):
            z = self.act_fun( out @ self.model[i].W + self.model[i].b )
            out = z

        return out

    def fit(self, X = [], Y = [], epochs = 100, learning_rate = 0.5):

        for k in range(epochs):

            out = [(None, X)]

            for i in range(len(self.model)):
                z = out[-1][1] @ self.model[i].W + self.model[i].b
                a = sigmoid(z, deriv = False)
                out.append((z, a))

            deltas = []

            for i in reversed(range(len(self.model))):
                z = out[i + 1][0]
                a = out[i + 1][1]

                if i == len(self.model) - 1:
                    deltas.insert(0, MSE(a, Y, deriv = True) * sigmoid(a, deriv = True))
                else:

                    deltas.insert(0, deltas[0] @ _W.T * sigmoid(a, deriv = True))

                _W = self.model[i].W

                self.model[i].b = self.model[i].b - np.mean(deltas[0], axis = 0, keepdims = True) * learning_rate
                self.model[i].W = self.model[i].W - out[i][1].T @ deltas[0] * learning_rate

        print('NeuralNetwork Successfully Trained')


def random_points(n = 100):
	x = np.random.uniform(0.0, 1.0, n)
	y = np.random.uniform(0.0, 1.0, n)

	return np.array([x, y]).T

def main():
    brain_xor = NeuralNetwork(top = [2, 4, 1], act_fun = tanh)

    X = np.array([
        [0,0],
        [0,1],
        [1,0],
        [1,1],
    ])

    Y = np.array([
        [0],
        [1],
        [1],
        [0],
    ])

    brain_xor.fit(X = X, Y = Y, epochs = 10000, learning_rate = 0.08)

    x_test = random_points(n = 5000)
    y_test = brain_xor.predict(x_test)

    plt.scatter(x_test[:,0], x_test[:,1], c = y_test, s = 25, cmap='GnBu')
    plt.savefig('XOR_Fitted.jpg')
    # plt.show()

    # CIRCLES

    brain_circles = NeuralNetwork(top = [2, 4, 8, 1], act_fun = sigmoid)

    X, Y = make_circles(n_samples = 500, noise = 0.05, factor = 0.5)
    Y = Y.reshape(len(X), 1)


    # y_test = brain_circles.predict(X)
    # plt.scatter(X[:,0], X[:,1], c = y_test, cmap = 'winter', s = 25)
    # plt.show()

    brain_circles.fit(X = X, Y = Y, epochs = 10000, learning_rate = 0.05)

    y_test = brain_circles.predict(X)
    plt.scatter(X[:,0], X[:,1], c = y_test, cmap = 'winter', s = 25)
    plt.savefig('Circle_fitted.jpg')
    plt.show()

    brain_moon = NeuralNetwork(top = [2, 4, 8, 1], act_fun = sigmoid)

    X, Y = make_moons(n_samples = 500, noise = 0.05)
    Y = Y.reshape(len(X), 1)

    y_test = brain_moon.predict(X)
    # plt.scatter(X[:,0], X[:,1], c = y_test, cmap = 'winter')

    brain_moon.fit(X = X, Y = Y, epochs = 10000, learning_rate = 0.05)

    y_test = brain_moon.predict(X)
    plt.scatter(X[:,0], X[:,1], c = y_test, cmap = 'winter')
    plt.savefig('Moon_fitted.jpg')
    plt.show()


if __name__ == '__main__':
    main()
