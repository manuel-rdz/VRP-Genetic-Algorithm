import tsp_ga
import tsp_tabu_search
import random
from tsp_ga import City as CityGA
from tsp_tabu_search import City as CityTabu

no_cities = 50


city_list_ga = []
city_list_tabu = []
for i in range(0, no_cities):
    x = int(random.random()*200)
    y = int(random.random()*200)
    city_list_ga.append(CityGA(x=x, y=y))
    city_list_tabu.append(CityTabu(x=x, y=y))


ga_best = tsp_ga.start(city_list_ga)
print(ga_best.calculate_route_cost())

tabu_best, tabu_cost = tsp_tabu_search.start(city_list_tabu)
print(tabu_cost)