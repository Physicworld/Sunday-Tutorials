import numpy as np

# y = 3*x + 1
dataset = [
    [0,1],
    [1,4],
    [2,7],
    [3,10],
    [4,13],
    [5,16]
]


def coste(w, b):
    N = len(dataset)
    error = 0
    error_absoluto = 0
    for i in range(N):
        x = dataset[i][0]
        y = dataset[i][1]
        y_pred = w*x + b
        error = y - y_pred
        error_absoluto += error * error
        # print("Variable:", x, "REAL:", y, "MODELO:", y_pred, "ERROR: ", error)
    # print("ERROR ABSOLUTO: ", error_absoluto)
    return error_absoluto

def fit(w, b, n_iter=100, eps = 0.001, rate = 0.001):
    for i in range(n_iter):
        dw = (coste(w+eps,b) - coste(w,b))/eps
        db = (coste(w, b+eps) - coste(w, b))/eps
        w -= rate * dw
        b -= rate * db
    return w,b

np.random.seed(46)
w = np.random.random() * 10
b = np.random.random() * 10

print(f"W:{w}, B:{b}, COST:{coste(w=w, b=b)}")
w, b = fit(w=w,b=b, n_iter=1000, eps = 0.01, rate=0.01)
print(f"W:{w}, B:{b}, COST:{coste(w=w, b=b)}")