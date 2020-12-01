import tsp_ga
import tsp_tabu_search
import random
import time
from tsp_ga import City as CityGA
from tsp_tabu_search import City as CityTabu

no_cities = [30, 60, 100]

for no_city in no_cities:
    genetic_time = 0
    genetic_route_cost = 0

    tabu_time = 0
    tabu_route_cost = 0

    for it in range(5):
        city_list_ga = []
        city_list_tabu = []
        for i in range(0, no_city):
            x = int(random.random()*200)
            y = int(random.random()*200)
            city_list_ga.append(CityGA(x=x, y=y))
            city_list_tabu.append(CityTabu(x=x, y=y))

        start = time.time()
        ga_best = tsp_ga.start(city_list_ga)
        end = time.time()

        genetic_time += end - start
        genetic_route_cost += ga_best.calculate_route_cost()

        start = time.time()
        _, tabu_cost = tsp_tabu_search.start(city_list_tabu)
        end = time.time()

        tabu_time += end - start
        tabu_route_cost += tabu_cost

        print('Finished iteration ', it)

    print('Avg genetic time for ', no_city, ' cities: ', genetic_time / 5.0)
    print('Avg genetic route cost for ', no_city, ' cities: ', genetic_route_cost / 5.0)
    print('')
    print('Avg tabu time for ', no_city, ' cities: ', tabu_time / 5.0)
    print('Avg tabu route cost for ', no_city, ' cities: ', tabu_route_cost / 5.0)
    print('')