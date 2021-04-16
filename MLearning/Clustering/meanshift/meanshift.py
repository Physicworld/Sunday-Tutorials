'''
---------------------------------------------------------

Domingo Cajina 28/03/2021

---------------------------------------------------------

Mean Shifth Algorithm


Paso 1.-

Inicializacion de centroide -> Todos los datos son inicializados
como centroides, iniciamos con tantos clusters  como puntos
tengamos en nuestro dataset, y poco a poco apuntamos a la
cantidad optima de clusters.

Paso 2.-
Actualizacion de clusters -> Revisamos la vencindad alrededor
de cada centroide y agrupados.

'''


import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


def gaussian_kernel(distance, epsilon):
	return (1/(epsilon * np.sqrt(2*np.pi))) * np.exp(-0.5*((distance/epsilon))**2)

def euclidean_distance(x, center):
	return np.sqrt(np.sum((x-center)**2))


def neighbourhood(X, x_centroid, epsilon):
	in_neighbourhood = []

	for x in X:
		distance = euclidean_distance(x, x_centroid)

		if distance <= epsilon:
			in_neighbourhood.append(x)

	return in_neighbourhood

class MeanShift:
	"""Programando el metodo de aprendizaje no supervisado MeanShift"""

	def __init__(self, epsilon, iters = 100):
		self.epsilon = epsilon
		self.iters = iters
		self.centroids_ = []

	def fit(self, _X):

		# Inicialmente todos los puntos del conjunto se consideran centros
		X = np.copy(_X)

		for _ in range(self.iters):
			for i in range(len(X)):
				# Se calcula para cada punto su vecindad
				neighbours = neighbourhood(X, X[i], self.epsilon)

				m_num = 0
				m_den = 0
				# Para cada vecindad, se calcula el promedio ponderado.
				# En fisica se conoce como centro de masa.
				for neighbour in neighbours:
					distance = euclidean_distance(neighbour, X[i])
					weight = gaussian_kernel(distance, self.epsilon)
					m_num += (weight * neighbour)
					m_den += weight

				# new centroid
				X[i] = m_num/m_den
			self.centroids_ = np.copy(X)

	def predict(self, X):

		labels = []

		for x in X:
			distances = [euclidean_distance(x, center) for center in self.centroids_]
			labels.append(distances.index(min(distances)))

		return labels

def main():
	n_clusters = 3
	X, y_true = make_blobs(n_samples = 50, centers = n_clusters, cluster_std = 1.2, random_state = 7)

	model = MeanShift(epsilon = 5, iters = 25)
	model.fit(X)
	labels = model.predict(X)
	centroids = model.centroids_

	plt.style.use('classic')
	plt.scatter(X[:, 0], X[:,1], c = labels, s = 100)
	plt.scatter(centroids[:,0], centroids[:,1], c = 'r', s = 50, marker = 'x')
	plt.savefig('meanshiftexample.png')
	
	plt.show()



if __name__ == '__main__':
	main()
