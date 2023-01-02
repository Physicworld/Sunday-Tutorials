import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
import random

def moving_average_crossover(df, short_window, long_window):
  # Calculamos los promedios móviles
  short_rolling = df.close.rolling(window=short_window).mean()
  long_rolling = df.close.rolling(window=long_window).mean()
  
  # Creamos un DataFrame con las dos medias móviles
  signals = pd.DataFrame({"short_rolling": short_rolling, "long_rolling": long_rolling})
  
  # Creamos una columna de señales que indica cuando debemos comprar (1) o vender (-1)
  signals["signal"] = np.where(signals["short_rolling"] > signals["long_rolling"], 1, -1)
  
  # Creamos una columna de posición que indica cuándo debemos mantener una posición larga (1) o corta (-1)
#   signals["position"] = signals["signal"].diff()
  
  return signals


def plot_results(df, signals, title):
    #Calculamos el capital acumulado multiplicando las señales por el rendimiento de cada operación
    df["returns"] = df.close.pct_change()
    df["strategy"] = signals["signal"].shift(1) * df["returns"]
    df["cumulative"] = df["strategy"].cumsum()
    #Graficamos el capital acumulado y el precio del activo
    plt.plot(df.index, df["cumulative"], label="capital acumulado")
    #plt.plot(df.index, df["close"], label="precio del activo")
    plt.legend(loc="upper left")
    plt.title(title)
    plt.show()

df = pd.read_csv("bitcoin_price_data.csv")


def evaluate_strategy(individual):
    # Desempaquetamos el individuo (que consiste en dos valores: la longitud de la media móvil a corto plazo y la longitud de la media móvil a largo plazo)
    short_window, long_window = individual
    signals = moving_average_crossover(df, short_window=short_window, long_window=long_window)
    df["returns"] = df.close.pct_change()
    df["strategy"] = signals["signal"].shift(1) * df["returns"]
    returns = df["strategy"].cumsum()
    final_return = returns[-1]
    return (final_return, )

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("evaluate", evaluate_strategy)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=30, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
pop = toolbox.generate(n=50)

pop, log = algorithms.eaSimple(population = pop, toolbox = toolbox, cxpb=0.5, mutpb=0.2, ngen=50, verbose=True)
best_individual = tools.selBest(pop, 1)[0]

print(best_individual)