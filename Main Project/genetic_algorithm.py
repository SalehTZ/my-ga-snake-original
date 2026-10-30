import random
from pysnake import *
from operator import attrgetter
import numpy as np
# import matplotlib.pyplot as plotting


class Directions:
    UP = 3
    DOWN = 2
    RIGHT = 1
    LEFT = 0


class DNA:
    shouldInitGenes = False
    crossoverRate = 0.5
    mutation_rate = 0.01

    def __init__(self, size, crossoverrate, mutation_rate, shouldInitGenes):
        self.shouldInitGenes = shouldInitGenes
        self.crossoverRate = crossoverrate
        self.mutation_rate = mutation_rate

        # generating first gene
        if self.shouldInitGenes:
            self.genes = []
            self.fitness = 0
            for i in range(0, size):
                self.genes.insert(i, self.getRandomGene())

    @staticmethod
    def getRandomGene():
        return random.randint(0, 3)

    def get_fitness(self):
        return self.fitness

    def crossover(self, other_parent):
        child = DNA(dna_size, self.crossoverRate, self.mutation_rate, shouldInitGenes=True)

        for i in range(0, dna_size):
            if random.uniform(0, 1) < self.crossoverRate:
                child.genes.insert(i, self.genes[i])
            else:
                child.genes.insert(i, other_parent.genes[i])

        return child

    def mutate(self):
        for i in range(0, dna_size):
            if random.uniform(0, 1) < self.mutation_rate:
                self.genes.insert(i, self.getRandomGene())


# Genetic algorithm class is here ##########
class GeneticAlgorithm:
    # population = []
    best_gene = []
    generation = 0
    best_fitness = 0
    fitness_sum = 0
    crossover_rate = 0.5
    mutation_rate = 0.01

    def __init__(self, population_size, dna_size, mutation_rate, crossover_rate):
        self.generation = 0
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = []

        for i in range(0, population_size):
            self.population.append(DNA(dna_size, self.crossover_rate, self.mutation_rate, shouldInitGenes=True))

    def new_generation(self):
        if len(self.population) <= 0:
            return

        self.calculate_best_fitness()

        new_population = []

        for i in range(0, population_size):
            parent1 = self.choose_parent()
            parent2 = self.choose_parent()

            child = parent1.crossover(parent2)

            child.mutate()

            new_population.append(child)
        self.population = new_population.copy()

        self.generation = self.generation + 1

    def calculate_best_fitness(self):
        self.set_fitnesses()

        self.fitness_sum = 0
        best = self.population[0]

        for p in range(0, len(self.population)):
            self.fitness_sum += self.population[p].get_fitness()
            if self.population[p].fitness > best.fitness:
                best = self.population[p]

        self.best_fitness = best.fitness
        self.best_gene = best.genes.copy()

    def set_fitnesses(self):
        fitness_list = all_fitnesses()
        s = 0
        for fitness in fitness_list:
            self.population[s].fitness = fitness
            s += 1

    def choose_parent(self):
        best = self.population
        # for pop in self.population:
        #     if pop.fitness > best:
        #         best = pop.fitness
        # # self.population.sort()
        # return self.population[0]
        best = self.sel_tournament(self.population, 1, 5)
        return best

    def sel_random(self, individuals, k):
        """Select *k* individuals at random from the input *individuals* with
        replacement. The list returned contains references to the input
        *individuals*.
        :param individuals: A list of individuals to select from.
        :param k: The number of individuals to select.
        :returns: A list of selected individuals.
        This function uses the :func:`~random.choice` function from the
        python base :mod:`random` module.
        """
        return [random.choice(individuals) for i in range(k)]

    def sel_tournament(self, individuals, k, tournsize, fit_attr="fitness"):
        """Select the best individual among *tournsize* randomly chosen
        individuals, *k* times. The list returned contains
        references to the input *individuals*.
        :param individuals: A list of individuals to select from.
        :param k: The number of individuals to select.
        :param tournsize: The number of individuals participating in each tournament.
        :param fit_attr: The attribute of individuals to use as selection criterion
        :returns: A list of selected individuals.
        This function uses the :func:`~random.choice` function from the python base
        :mod:`random` module.
        """
        chosen = []
        for i in range(k):
            aspirants = self.sel_random(individuals, tournsize)
            chosen.append(max(aspirants, key=attrgetter(fit_attr)))
        return chosen

# main program initialization and core
population_size = 50
mutation_rate = 0.01
crossover_rate = 0.5
dna_size = 500  # Moving Directions
itter = 100
best_generation = 0
best_of_best_fitness = 0
# plot_fitness = []
# plot_generation = []

# game options
game_speed = 10
random_seed = 9000  # 9000 fits best


def getRandomGene():
    return random.randint(0, 3)


def all_fitnesses():
    game = SnakeGame(random_seed, population_size)
    # returning list of fitnesses
    return game.play_game(ga.population, game_speed)


if __name__ == '__main__':

    ga = GeneticAlgorithm(population_size, dna_size, mutation_rate, crossover_rate)
    ga.new_generation()

    best_of_best_fitness = ga.best_fitness

    for i in range(0, itter):
        print("========== Generation " + str(ga.generation) + " ============")
        print("> Best Fitness : " + str(ga.best_fitness))
        if ga.best_fitness > best_of_best_fitness:
            best_of_best_fitness = ga.best_fitness
            best_generation = ga.generation
        # plot_generation.append(ga.generation)
        # plot_fitness.append(ga.best_fitness)

        print("> best gene : ", end=" ")
        for j in range(0, dna_size):
            print(str(ga.best_gene[j]) + " ,", end=" ")

        print(" ")
        print("> translated gene : ", end=" ")
        for j in range(0, dna_size):
            if ga.best_gene[j] == Directions.LEFT:
                print("L ,", end=" ")
            if ga.best_gene[j] == Directions.RIGHT:
                print("R ,", end=" ")
            if ga.best_gene[j] == Directions.UP:
                print("U ,", end=" ")
            if ga.best_gene[j] == Directions.DOWN:
                print("D ,", end=" ")

        print(" ")
        ga.new_generation()

    print("result : best fitness = " + str(best_of_best_fitness) + " in generation = " + str(best_generation))

    # print("also generations = ", end=" ")
    # for var in best_repeated_generations:
    #     print(str(var) + " ,", end=" ")

    # plotting.plot(plot_generation, plot_fitness)
    # plotting.xlabel("Generation")
    # plotting.ylabel("Fitness")
    # plotting.title("Algorithm graph")
    # plotting.show()


