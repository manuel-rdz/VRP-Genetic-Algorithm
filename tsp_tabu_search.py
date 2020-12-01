import random
import math
import copy


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def calculate_cost(route, start_city):
    dist = start_city.calculate_distance(route[0])
    for idx, city in enumerate(route):
        if idx < len(route) - 1:
            dist += city.calculate_distance(route[idx + 1])
    dist += route[-1].calculate_distance(start_city)

    return dist


def start(city_list):
    inf = 100000000000000
    start_city = city_list[0]

    tabu = {}
    memory = {}

    current_solution = random.sample(city_list, len(city_list))
    current_cost = calculate_cost(current_solution, start_city)

    best_solution = copy.deepcopy(current_solution)
    best_cost = inf

    swap_i, swap_j = -1, -1

    # tabu phase
    for x in range(100):
        next_cost = inf
        is_best = False

        for i in range(len(current_solution)):
            for j in range(i + 1, len(current_solution)):
                current_solution[i], current_solution[j] = current_solution[j], current_solution[i]
                cost = calculate_cost(current_solution, start_city)
                if cost < best_cost:
                    best_cost = cost
                    next_cost = cost
                    swap_i, swap_j = i, j
                    is_best = True
                elif cost < next_cost and tabu.setdefault((i, j), 0) <= 0:
                    next_cost = cost
                    swap_i, swap_j = i, j

                current_solution[i], current_solution[j] = current_solution[j], current_solution[i]

        for k in tabu:
            tabu[k] -= 1

        tabu[(swap_i, swap_j)] = 3
        memory[(swap_i, swap_j)] = memory.setdefault((swap_i, swap_j), 0) + 1

        current_solution[swap_i], current_solution[swap_j] = current_solution[swap_j], current_solution[swap_i]

        if is_best:
            best_solution = copy.deepcopy(current_solution)

        #print(calculate_cost(best_solution, start_city))

    current_solution = copy.deepcopy(best_solution)

    print('start memory phase')

    # memory phase
    for x in range(100):
        next_cost = inf
        is_best = False

        for i in range(len(current_solution)):
            for j in range(i + 1, len(current_solution)):
                current_solution[i], current_solution[j] = current_solution[j], current_solution[i]
                cost = calculate_cost(current_solution, start_city)
                if cost < best_cost:
                    best_cost = cost
                    next_cost = cost + memory.setdefault((i, j), 0)
                    swap_i, swap_j = i, j
                    is_best = True
                else:
                    cost += memory.setdefault((i, j), 0)
                    if cost < next_cost:
                        next_cost = cost
                        swap_i, swap_j = i, j

                current_solution[i], current_solution[j] = current_solution[j], current_solution[i]

        memory[(swap_i, swap_j)] = memory.setdefault((swap_i, swap_j), 0) + 1

        current_solution[swap_i], current_solution[swap_j] = current_solution[swap_j], current_solution[swap_i]

        if is_best:
            best_solution = copy.deepcopy(current_solution)

        #print(calculate_cost(best_solution, start_city))

    return best_solution, best_cost
