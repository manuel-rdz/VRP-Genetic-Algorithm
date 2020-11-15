import random
import numpy as np

amount_states = 5
states = np.arange(amount_states)

state_connections = {
    0: [1,2,3,4],
    1: [0,2,3,4],
    2: [0,1,3,4],
    3: [0,1,2,4],
    4: [0,1,2,3]
}


def selection(population):
    return population.get_fittest_individual(), population.get_second_fittest_individual()


def crossover(ind1, ind2):
    for k, v in ind1.routes.items():
        p = random.randint(0, len(v) - 1)
        v[0:p], ind2.routes[k][0:p] = ind2.routes[k][0:p], v[0:p]


def mutation(ind):
    for k, v in ind.routes.items():
        p = random.randint(1, 100)
        if p <= 10:  # 10% probability to mutate
            p = random.randint(0, len(v) - 1)
            v[p] = states[random.randint(0, len(states) - 1)]


def get_fittest_offspring(ind1, ind2):
    return ind1 if ind1.fitness > ind2.fitness else ind2


def add_fittest_offspring_to_population(ind1, ind2, population):
    ind1.calculate_fitness()
    ind2.calculate_fitness()

    least_fittest_idx = population.get_least_fittest_individual_index()
    population.individuals[least_fittest_idx] = get_fittest_offspring(ind1, ind2)


class Population:
    def __init__(self, population_size=10):
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
    def __init__(self, vehicles=1):
        self.routes = {}
        self.fitness = 0
        for i in range(vehicles):
            route_size = random.randint(1, amount_states)
            self.routes[i] = random.sample(range(amount_states), route_size)
            self.routes[i][0], self.routes[i][-1] = 0, 0  # always start and end on position 0

    def calculate_fitness(self):
        self.fitness = 0
        set_states = set(states)
        for k, v in self.routes.items():
            for idx, state in enumerate(v):
                set_states.discard(state)
                if idx != len(v) - 1:
                    next_state = v[idx + 1]
                    if next_state not in state_connections[state]:
                        self.fitness -= 1  # trying to go to a unreachable state
        self.fitness -= len(set_states)  # missing nodes

    def print_routes(self):
        for k, v in self.routes.items():
            print(k, v)


if __name__ == '__main__':
    population = Population()
    population.calculate_fitness()

    for i in range(100):
        print(i)
        population.get_fittest_individual().print_routes()
        ind1, ind2 = selection(population)

        crossover(ind1, ind2)

        mutation(ind1)
        mutation(ind2)

        add_fittest_offspring_to_population(ind1, ind2, population)

        population.calculate_fitness()