import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split


def minkouwski_distance(x1, x2, p):
    '''
    La distancia de minkouwski es una metrica para un espacio vectorial
    y es una generalizacion de diferentes tipos de metricas.
    cuando p = 1, se le conoce como distancia de Manhattan,
    cuando p = 2, se le conoce como distancia euclideana.
    '''
    return (np.sum(x1-x2)**p)**(1/p)



class KnearestKneighbours:
    def __init__(self, kneighbours, minkouwski_space = 2):
        self.kneighbours = kneighbours
        self.minkouwski_space = minkouwski_space
        self.labels_ = []

    def voting_neighbours(self, dataset):
        data_count = dataset[:, 0]
        unique, counts = np.unique(data_count, return_counts = True)
        # Cada iterable es una tupla (key, value) una tupla es mayor
        # que otra si su primer elemento lo es.
        # queremos comparar el segundo valor y quedarnos con el key,
        # por que usamos lambda para indicarle a max que ordene por
        #  el valor y no por tupla.
        return (max(dict(zip(unique, counts)).items(), key = lambda x: x[1])[0])

    def predict(self, X, Y, x_predict):

        for x1 in x_predict:
            distances = []
            for x2 in X:
                distances.append(minkouwski_distance(x1, x2, self.minkouwski_space))

            #   Obtenemos las distancias y etiquetas
            dataset = np.vstack((Y, distances)).T

            #  Ordenamos dataset por distancia
            dataset = dataset[np.argsort(dataset[:, 1])]

            #   Enviamos a voting_neighbours los k vecinos mas cercanos
            #   y regresamos la etiqueta

            self.labels_.append(self.voting_neighbours(dataset[0:self.kneighbours]))

def main():
    n_clusters = 3

    X, y_true = make_blobs(n_samples = 100, centers = n_clusters, cluster_std = 1.2, random_state = 3)

    x_train, x_test, y_train, y_test = train_test_split(X, y_true, test_size = 0.25, random_state = 1)

    model = KnearestKneighbours(kneighbours = 5, minkouwski_space = 2)
    model.predict(x_train, y_train, x_test)
    labels = model.labels_

    plt.style.use('classic')
    plt.scatter(x_train[:, 0], x_train[:,1], s = 100, c = y_train)
    plt.scatter(x_test[:,0], x_test[:,1], c = labels, s = 100, marker = '*')
    plt.show()

if __name__ == '__main__':
    main()
