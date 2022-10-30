from decimal import MAX_EMAX
import random
import matplotlib.pyplot as plt

n = 5  # Individual 
m = 500  # Number of individuals in a population
cost = MAX_EMAX
n_generations = 1000

losses = []

map = [[0, 12, cost, 5, 7],
       [12, 0, 14, cost, 18],
       [cost, 14, 0, 6, 19],
       [5, cost, 6, 0, 2],
       [7, 18, 19, 4, 0]]


def create_individual():
    return [random.randint(1, n) for _ in range(n)]


def compute_loss(individual):
    i = 0
    price = 0
    while i < n - 1:
        a = individual[i] - 1
        b = individual[i + 1] - 1
        price += map[a][b]
        i += 1

    # Add path form last city to the first city
    start = individual[0] - 1
    finish = individual[n - 1] - 1
    price += map[finish][start]

    # Check if individual contain all citys
    s = set(individual)
    price += ((n - len(s)) * 1000)
    return price


def generate_random_value():
    return random.randint(1, 5)


def compute_fitness(indvididual):
    loss = compute_loss(indvididual)
    fitness = 1 / (loss + 1)
    return fitness


def crossover(individual1, individual2, crossover_rate=0.9):
    individual1_new = individual1.copy()
    individual2_new = individual2.copy()

    for i in range(n):
        if random.random() < crossover_rate:
            individual1_new[i] = individual2[i]
            individual2_new[i] = individual1[i]

    return individual1_new, individual2_new


def mutate(individual, mutation_rate=0.05):
    individual_m = individual.copy()

    for i in range(n):
        if random.random() < mutation_rate:
            individual_m[i] = generate_random_value()

    return individual_m


def selection(sorted_old_population):
    index1 = random.randint(0, m - 1)
    index2 = random.randint(0, m - 1)

    while index2 == index1:
        index2 = random.randint(0, m - 1)

    individual_s = sorted_old_population[index1]
    if index2 > index1:
        individual_s = sorted_old_population[index2]

    return individual_s


population = [create_individual() for _ in range(m)]
elitism = 2
for i in range(n_generations):
    sorted_population = sorted(population, key=compute_fitness)

    if i % 10 == 0:
        losses.append(compute_loss(sorted_population[m-1]))

    # Create new generation
    new_population = sorted_population[-elitism:]
    while len(new_population) < m:
        # selection
        individual_s1 = selection(sorted_population)
        individual_s2 = selection(sorted_population)  # duplication

        # crossover
        individual_c1, individual_c2 = crossover(individual_s1, individual_s2)

        # mutation
        individual_m1 = mutate(individual_c1)
        individual_m2 = mutate(individual_c2)

        new_population.append(individual_m1)
        new_population.append(individual_m2)

    # update population
    population = new_population

# result
print(population[0])

# Plot losses
plt.plot(losses)
plt.ylabel("value")
plt.xlabel("generation n")
plt.title("Losses")
plt.show()

