import copy
import time
import random
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt

class Individual:
    def __init__(self, gene_length):
        self.genes = [random.random() for _ in range(gene_length)]
        self.fitness = 0
    
    def compute_fitness(self, data_x, data_y):
        m, b = self.genes
        self.fitness = sum([(y - (m * x + b)) ** 2 for x, y in zip(data_x, data_y)])
    
    def mutate(self, mutation_rate):
        rand = random.random()
        if rand < mutation_rate:
            gene_to_mutate = random.randint(0, len(self.genes) - 1)
            self.genes[gene_to_mutate] += random.uniform(-1, 1)
    
    def crossover(self, other_, crossover_rate):
        rand = random.random()
        if rand < crossover_rate:
            other = copy.deepcopy(other_)
            gene_to_cross = random.randint(0, len(self.genes) - 1)
            # self.genes[gene_to_cross:] = other.genes[gene_to_cross:]
            self.genes[gene_to_cross] = other.genes[gene_to_cross]

    def __repr__(self) -> str:
        return f"y = {self.genes[0]}x + {self.genes[1]}"

def genetic_algorithm(
        data_x,
        data_y,
        gene_length,
        population_size,
        best_size,
        mutation_rate,
        crossover_rate,
        num_generations):
    
    historical_fitness = []
    fitness_map = []
    
    # Use interactive mode for plt
    plt.ion()
    global_best_individual = Individual(gene_length)
    global_best_individual.compute_fitness(data_x, data_y)
  
   # Crear la población inicial
    population = [Individual(gene_length) for _ in range(population_size)]

    # Plot
    fig, ax = plt.subplots(3, 1)

    for i in range(500):

        # Evaluar la población
        for individual in population:
            individual.compute_fitness(data_x, data_y)

        # Seleccionar los mejores individuos
        best_population = sorted(population, key=lambda x: x.fitness, reverse=False)[:best_size].copy()

        # Reproducir los mejores individuos
        for individual in population:
            father = random.choice(best_population)
            individual.crossover(father, crossover_rate)

        # Mutar los individuos
        for individual in population:
            individual.mutate(mutation_rate)

        # Select Best Individual
        best_individual = copy.deepcopy(sorted(best_population, key=lambda x: x.fitness, reverse=False)[0])
        print(best_individual.fitness , global_best_individual.fitness)
        if best_individual.fitness < global_best_individual.fitness:
            global_best_individual = best_individual

        historical_fitness.append(global_best_individual.fitness)
        
        for i in range(10):
            sample = [
                population[i].genes[0],
                population[i].genes[1],
                population[i].fitness
            ]
            fitness_map.append(sample)

        # Limpiar lienzo
        ax[0].cla()
        ax[1].cla()
        ax[2].cla()

        # Subplot 1: Fitness vs Generations
        ax[0].set_title("Fitness")
        ax[0].set_xlabel("Generations")
        ax[0].plot(historical_fitness)

        # Subplot 2: Data vs Best Individual
        ax[1].scatter(data_x, data_y)
        ax[1].plot(data_x, [global_best_individual.genes[0] * x + global_best_individual.genes[1] for x in data_x], color="red")
        for i in range(1, 10):
            ax[1].plot(data_x, [population[i].genes[0] * x + population[i].genes[1] for x in data_x], color="green", alpha=0.2)
        
        # Agregar parámetros del modelo como texto a la gráfica
        model_text = f"y = {global_best_individual.genes[0]:.2f}x + {global_best_individual.genes[1]:.2f}"
        ax[1].text(0.05, 0.95, model_text, transform=ax[1].transAxes, fontsize=14,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
        
        # Subplot 3: Fitness Map
        ax[2].set_title("Fitness Map")
        ax[2].set_xlabel("m")
        ax[2].set_ylabel("b")
        ax[2].scatter(
            [x[0] for x in fitness_map],
            [x[1] for x in fitness_map],
            c=[x[2] for x in fitness_map],
            cmap="viridis")
        
        ax[2].scatter(global_best_individual.genes[0], global_best_individual.genes[1], color="red")

        # Update the figure
        fig.canvas.draw()
        fig.canvas.flush_events()
    # Turn off the interactive mode
    plt.ioff()

    # Show the final figure after the loop
    plt.show()

       
    


X = np.linspace(-10, 10, 100)
Y = 2 * X + 3 + np.random.normal(0, 1, 100)

genetic_algorithm(
    data_x=X,
    data_y=Y,
    gene_length=2,
    population_size=1000,
    mutation_rate=0.5,
    crossover_rate=0.5,
    num_generations=1000,
    best_size=100
)
