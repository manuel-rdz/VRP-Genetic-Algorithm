import math
import random
import numpy as np

cityList = []


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Population:
    def __init__(self, size = 150):
        self.size = size
        self.population = []

        for _ in range(size):
            self.population.append(Individual())

    def get_best_by_roulette(self):
        weights = []
        for ind in self.population:
            weights.append(ind.calculate_fitness())

        weights = np.array(weights)
        weights = np.reciprocal(weights)
        weights = weights / np.sum(weights)

        return np.random.choice(self.population, size=2, p=weights, replace=False)

    def get_idx_worst_individual(self):
        worst_idx = 0
        for idx, ind in enumerate(self.population):
            fit = ind.calculate_fitness()
            if fit < self.population[worst_idx].fitness:
                worst_idx = idx

        return worst_idx


class Individual:
    def __init__(self):
        self.route = random.sample(cityList, len(cityList))
        self.fitness = 0

    def calculate_fitness(self):
        dist = start_city.calculate_distance(self.route[0])
        for idx, city in enumerate(self.route):
            if idx < len(self.route) - 1:
                dist += city.calculate_distance(self.route[idx + 1])
        dist += self.route[-1].calculate_distance(start_city)

        self.fitness = 1.0 / dist
        return self.fitness

    def calculate_route_cost(self):
        self.calculate_fitness()
        return 1.0 / self.fitness


def selection(population):
    return population.get_best_by_roulette()


def breed(ind1, ind2):
    a = random.randint(0, len(ind1.route) - 1)
    b = random.randint(a, len(ind1.route) - 1)

    ind3 = Individual()
    for i in range(0, len(ind2.route)):
        if i >= a or i <= b:
            ind3.route[i] = ind1.route[i]
        else:
            ind3.route[i] = ind2.route[i]
    return ind3


def mutate(ind, mutation_rate):
    for i in range(0, len(ind.route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(ind.route) - 1)
            ind.route[i], ind.route[j] = ind.route[j], ind.route[i]
    return ind


def add_offspring(ind, pop):
    idx = pop.get_idx_worst_individual()
    pop.population[idx] = ind


start_city = City(random.random() * 200, random.random() * 200)

for i in range(0, 25):
    cityList.append(City(x=int(random.random() * 200), y=int(random.random() * 200)))

population = Population()

for i in range(10000):
    parent1, parent2 = selection(population)
    print(parent1.calculate_route_cost(), parent2.calculate_route_cost())
    offspring = breed(parent1, parent2)
    offspring = mutate(offspring, 0.1)
    add_offspring(offspring, population)
