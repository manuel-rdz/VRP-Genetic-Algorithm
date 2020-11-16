import random
import numpy as np
import copy

INF = 10000000
amount_states = 13
states = np.arange(amount_states)
'''
state_connections = {
    0: [1, 2, 4],
    1: [0, 3, 4],
    2: [0, 3, 5],
    3: [1, 2, 4, 5],
    4: [0, 1, 3, 5],
    5: [2, 3, 4]
}
'''

state_connections = {
    0: [3,2,4,1],
    1: [0,7],
    2: [0,4,5,6,10],
    3: [0,6,10],
    4: [0,2,8],
    5: [2,9,8,7],
    6: [2,3,11],
    7: [1,5,8],
    8: [4,5,7,9],
    9: [5,8,11],
    10: [2,3,12],
    11: [6,9,12],
    12: [10,11]
}

def selection(population):
    return population.get_fittest_individual(), population.get_second_fittest_individual()


def crossover(ind1, ind2):
    offspring = Individual()
    for k, v in ind1.routes.items():
        p = random.randint(1, 2)
        if p & 1:
            offspring.routes[k] = v
        else:
            offspring.routes[k] = ind2.routes[k]
    return offspring


def mutation(ind):
    mutation_prob = 40
    for k, v in ind.routes.items():
        p = random.randint(1, 100)
        if p <= mutation_prob:  # 40% probability to mutate
            if p <= mutation_prob * 0.5:
                if len(v) > amount_states + 2:
                    v = [0]
                else:
                    p = random.randint(0, len(state_connections[v[-1]]) - 1)
                    v.append(state_connections[v[-1]][p])
            else:  # p <= mutation_prob * 0.95:
                if len(v) > 1:
                    v.pop()
            #else:
            #    v = [0]


def get_fittest_offspring(ind1, ind2):
    return ind1 if ind1.fitness > ind2.fitness else ind2


def add_fittest_offspring_to_population(ind, population):
    ind.calculate_fitness()

    least_fittest_idx = population.get_least_fittest_individual_index()
    population.individuals[least_fittest_idx] = get_fittest_offspring(ind, population.individuals[least_fittest_idx])


class Population:
    def __init__(self, population_size=500):
        self.population_size = population_size
        self.individuals = []
        self.fittest = 0

        for i in range(population_size):
            self.individuals.append(Individual())

    def get_fittest_individual(self):
        fittest_idx = 0
        for idx, ind in enumerate(self.individuals):
            if ind.fitness > self.individuals[fittest_idx].fitness:
                fittest_idx = idx

        return self.individuals[fittest_idx]

    def get_second_fittest_individual(self):
        fittest_idx = 0
        second_fittest_idx = 0
        for idx, ind in enumerate(self.individuals):
            if ind.fitness > self.individuals[fittest_idx].fitness:
                second_fittest_idx = fittest_idx
                fittest_idx = idx
            elif ind.fitness > self.individuals[second_fittest_idx].fitness:
                second_fittest_idx = idx

        return self.individuals[second_fittest_idx]

    def get_least_fittest_individual_index(self):
        least_fittest_idx = 0
        for idx, ind in enumerate(self.individuals):
            if ind.fitness < self.individuals[least_fittest_idx].fitness:
                least_fittest_idx = idx
        return least_fittest_idx

    def calculate_fitness(self):
        for i in self.individuals:
            i.calculate_fitness()


class Individual:
    def __init__(self, vehicles=3):
        self.routes = {}
        self.fitness = 0
        self.vehicles = vehicles
        for i in range(vehicles):
            self.routes[i] = [0]  # always start on position 0

    def calculate_fitness(self):
        self.fitness = 0
        set_states = set(states)
        total_route = 0
        for k, v in self.routes.items():
            for idx, state in enumerate(v):
                if state in set_states:
                    set_states.discard(state)
                elif state != 0:
                    self.fitness -= 1

            self.fitness -= 3*abs(amount_states // self.vehicles + 2 - len(v))
            if v[-1] != 0:
                self.fitness -= INF  # must finish on 0
        self.fitness -= INF * len(set_states)  # must visit all nodes
        #self.fitness -= abs(amount_states + 2 * self.vehicles - 1 - total_route)


    def print_routes(self):
        for k, v in self.routes.items():
            print(k, v)


if __name__ == '__main__':
    population = Population()
    population.calculate_fitness()
    best = None
    i = 0
    for i in range(5000):
        print('step:', i)
        ind = population.get_fittest_individual()
        if best is None or ind.fitness > best.fitness:
            best = copy.deepcopy(ind)
            print(best.fitness)
            if best.fitness >= -5:
                break
        #print(ind.fitness)
        #ind.print_routes()
        ind1, ind2 = selection(population)

        offspring = crossover(ind1, ind2)

        mutation(offspring)

        add_fittest_offspring_to_population(offspring, population)

        population.calculate_fitness()
        i += 1

    best.print_routes()
    print(best.fitness)