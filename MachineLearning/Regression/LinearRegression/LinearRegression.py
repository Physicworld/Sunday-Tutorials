# https://www.kaggle.com/vihansp/salary-data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class LinearRegression(object):

    def __init__(self):
        self.alpha = 0
        self.beta = 0
        self.r2 = 0

    def fit(self, X, Y):
        x_average = np.average(X)
        y_average = np.average(Y)

        sum_xy = np.sum(X * Y)
        sum_x = np.sum(X)
        sum_y = np.sum(Y)
        sum_x2 = np.sum(X*X)
        sum_y2 = np.sum(Y*Y)

        n = len(X)

        self.alpha = (sum_xy - n * x_average * y_average) / (sum_x2 - (1/n) * (sum_x ** 2))
        self.beta = (sum_x2 * sum_y - sum_xy * sum_x) / (n * sum_x2 - sum_x ** 2)
        self.r2 = (n * sum_xy - sum_x * sum_y)/(np.sqrt(n * sum_x2 - sum_x ** 2) * np.sqrt(n * sum_y2 - sum_y **2))


    def predict(self, X):
        return self.alpha * X + self.beta

def main():
    data = pd.read_csv("Salary_Data.csv")

    model = LinearRegression()
    x = data['YearsExperience'].values
    y = data['Salary'].values
    model.fit(x, y)

    x_test = np.linspace(start = 0, stop = 12, num = 50)
    y_test = model.predict(x_test)
    textstr = '\n'.join((
    r'$\rho = %.2f$' % (model.r2,),
    ))
    # print(x_test, y_test)

    plt.scatter(x, y, c = 'b')
    plt.text(2, 10 + model.beta, textstr)
    plt.plot(x_test, y_test)
    plt.show()


if __name__ == '__main__':
    main()
