'''
---------------------------------------------------------

Domingo Cajina 28/03/2021

---------------------------------------------------------

'''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


def euclidean_distance(x, center):
	return np.sqrt(np.sum((x-center)**2))

class KMeans:
	def __init__(self, n_clusters, iters = 100):
		self.n_clusters = n_clusters
		self.iters = iters
		self.centroide = []
		self.labels_ = []

	def fit(self, X):

		self.centroide = np.random.choice(X.shape[0], size = self.n_clusters, replace = False)
		self.centroide = [X[i] for i in self.centroide]


		for i in range(self.iters):
			distances = []
			self.labels_ = []

			for x in X:
				distances = [euclidean_distance(x, center) for center in self.centroide]
				self.labels_.append(distances.index(min(distances)))

			labels = np.array(self.labels_)

			for k in range(self.n_clusters):

				cluster = X[labels == k]

				self.centroide[k] = np.average(cluster, axis = 0)
			del labels

	def predict(self, X):

		labels = []

		for x in X:
			distances = [euclidean_distance(x, center) for center in self.centroide]
			labels.append(distances.index(min(distances)))
		return labels


def main():

	n_clusters = 3

	X, y_true = make_blobs(n_samples = 500, centers = n_clusters, cluster_std = 0.95, random_state = 3)

	model = KMeans(n_clusters = n_clusters, iters = 250)

	model.fit(X)

	labels = model.labels_
	centroides = np.array(model.centroide)

	plt.style.use('classic')

	plt.scatter(X[:, 0], X[:,1], c = labels, s = 100)
	plt.scatter(centroides[:,0], centroides[:,1], c = 'r', s = 50, marker = 'x')
	plt.show()

if __name__ == '__main__':
	main()
