#!python3
import sys
import numpy as np
from copy import deepcopy
import random

features = []
interactions = []

pop_size = 50
max_iterations = 1000


def main(features, interactions):
    population = initialize_population()
    best, best_fitness = optimize(population)
    print("best individual:")
    print("\t" + str(best) + " " + str(best_fitness))


def optimize(population):
    best = None
    best_fitness = None
    iterations = 1
    while iterations < max_iterations:
        for p in population:
            fitness = assess_fitness(p)
            if best is None or fitness > best_fitness:
                best = p
                best_fitness = fitness
                print(best)
                print(best_fitness)
        new_population = []
        for i in range(int(pop_size / 2)):
            # keep in mind - the functions are also able to get more than one individual this is why we index here
            # with 0
            # ## select
            parent_a = select(population, 1)[0]
            parent_b = select(population, 1)[0]
            ### breed
            children_a, children_b = crossover(copy(parent_a), copy(parent_b))
            ### mutate children
            new_population.append(tweak(children_a))
            new_population.append(tweak(children_b))
        population = np.array(new_population)
        iterations += 1
    return best, best_fitness


def initialize_population():
    # random initialization
    population = np.random.randint(2, size=(pop_size, len(features)))
    return population


def copy(solution):
    # simple deep copy of the given solution
    return deepcopy(solution)


def tweak(solution):
    p = 0.5
    for i in range(len(solution)):
        if random.uniform(0, 1) < p:
            solution[i] = (solution[i] + 1) % 2
    return solution


# select individuals
def select(population, count=2):
    # create a fitness score array
    fitness_array = np.empty([pop_size])
    for i in range(len(population)):
        score = assess_fitness(population[i])
        fitness_array[i] = score

    # negative fitness can be handled as 0 fitness
    for i in range(len(fitness_array)):
        if fitness_array[i] <= 0.0:
            fitness_array[i] = 1.0

    # span value range
    for i in range(1, len(fitness_array)):
        fitness_array[i] = fitness_array[i] + fitness_array[i - 1]

    # parents = selectParentFPS(population, fitness_array, count)
    parents = select_parent_sus(population, fitness_array, count)
    return parents


def select_parent_sus(population, fitness_array, count):
    individual_indices = []
    # build the offset = random number between 0 and f_l / n
    offset = random.uniform(0, fitness_array[-1] / count)
    # repeat for all selections (n)
    for _ in range(count):
        index = 0
        # increment the index until we reached the offset
        while fitness_array[index] < offset:
            index += 1
        # increment the offset to the next target
        offset = offset + fitness_array[-1] / count
        individual_indices.append(population[index])
    # return all selected individual indices
    return np.array(individual_indices)


# Fitness-Proportionate Selection (FPS)
def select_parent_fps(population, fitness_array, count):
    individuals = []
    for _ in range(count):
        # random number of interval
        n = random.uniform(0, fitness_array[-1])
        selected_something = False
        for i in range(1, len(fitness_array)):
            if fitness_array[i - 1] < n <= fitness_array[i]:
                individuals.append(population[i])
                selected_something = True
                break
        if not selected_something:
            individuals.append(population[0])
    return np.array(individuals)


def crossover(solution_a, solution_b):
    # one point crossover
    # return one_point_crossover(solution_a, solution_b)
    # two point crossover
    return two_point_crossover(solution_a, solution_b)
    # uniform crossover
    # return uniform_crossover(solution_a, solution_b)


def one_point_crossover(solution_a, solution_b):
    index = random.randint(0, len(solution_a) - 1)
    for i in range(index):
        tmp = solution_a[i]
        solution_a[i] = solution_b[i]
        solution_b[i] = tmp
    return solution_a, solution_b


def two_point_crossover(solution_a, solution_b):
    index1 = index2 = 0
    while index1 == index2:
        index1 = random.randint(0, len(solution_a) - 1)
        index2 = random.randint(0, len(solution_a) - 1)
    left = min(index1, index2)
    right = max(index1, index2)
    for i in range(left, right):
        tmp = solution_a[i]
        solution_a[i] = solution_b[i]
        solution_b[i] = tmp

    return solution_a, solution_b


def uniform_crossover(solution_a, solution_b):
    for i in range(len(solution_a)):
        if random.uniform(0, 1) < 0.5:
            tmp = solution_a[i]
            solution_a[i] = solution_b[i]
            solution_b[i] = tmp
    return solution_a, solution_b


def assess_fitness(solution):
    fitness = 0
    # solution = [0,0,1,0,0,...]
    # get the performance of all activated features
    for i in range(len(features)):
        if solution[i] == 1:
            fitness += features[i][1]
    # get all interactions and check if all are activated
    for i in interactions:
        interaction_features = i[0]
        interaction_performance = i[1]
        all_activated = True
        for f in interaction_features:
            # get the index of the feature
            index = get_feature_index(f)
            if solution[index] != 1:
                all_activated = False
                break
        # if all features of the interaction are activated: add the performance
        if all_activated:
            fitness += interaction_performance
    return fitness


def get_feature_index(feature):
    for i in range(len(features)):
        if features[i][0][0] == feature:
            return i


def readTXT(path):
    result = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        name = line.split(" ")[0][:-1]
        names = name.split("#")
        value = float(line.split(" ")[1].strip())
        configuration = [names, value]
        result.append(configuration)
    return result


def printData(data):
    for d in data:
        print(d)


if __name__ == "__main__":
    # input scheme: run_genetic_alg.py model_features.txt model_interactions.txt
    if len(sys.argv) != 3:
        print("Not a valid input! Please use:" + \
              "python3 run_genetic_alg.py model_features.txt model_interactions.txt")
        sys.exit(0)
    features = readTXT(sys.argv[1])
    interactions = readTXT(sys.argv[2])
    main(features, interactions)
