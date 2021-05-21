
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
