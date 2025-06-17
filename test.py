import pandas as pd
import random

# Load the data
df = pd.read_csv('knapsack_items.csv')
items = df.to_dict('records')

# Knapsack constraints
MAX_WEIGHT = 10
MAX_VOLUME = 25

# Genetic Algorithm parameters - Increased for a more thorough search
POPULATION_SIZE = 200
NUM_GENERATIONS = 1000
MUTATION_RATE = 0.01
TOURNAMENT_SIZE = 5

def calculate_sack_properties(sack_items_indices, items_list):
    """Calculates the total weight, volume, and value of a sack."""
    total_weight = 0
    total_volume = 0
    total_value = 0

    # Get the IDs of items in the sack for combo checks
    sack_item_ids = {items_list[i]['id'] for i in sack_items_indices}

    for i in sack_items_indices:
        item = items_list[i]
        total_weight += item['weight_kg']
        total_volume += item['volume_L']

        # Start with the base value
        current_value = item['value']

        # Check for positive combo
        if item['positive_combo_id'] in sack_item_ids:
            current_value *= item['positive_combo_multiplier']

        # Check for negative combo
        if item['negative_combo_id'] in sack_item_ids:
            current_value *= item['negative_combo_multiplier']

        total_value += current_value

    return total_weight, total_volume, total_value

def fitness(chromosome, items_list):
    """Fitness function: calculates the value of a sack (chromosome)."""
    sack_items_indices = [i for i, gene in enumerate(chromosome) if gene == 1]
    weight, volume, value = calculate_sack_properties(sack_items_indices, items_list)

    # Penalize solutions that violate constraints
    if weight > MAX_WEIGHT or volume > MAX_VOLUME:
        return 0
    return value

def create_initial_population(size, num_items):
    """Creates an initial population of random valid solutions."""
    population = []
    attempts = 0 # to avoid infinite loop
    while len(population) < size and attempts < size * 10:
        chromosome = [random.randint(0, 1) for _ in range(num_items)]
        sack_items_indices = [i for i, gene in enumerate(chromosome) if gene == 1]
        weight, volume, _ = calculate_sack_properties(sack_items_indices, items)
        if weight <= MAX_WEIGHT and volume <= MAX_VOLUME:
            population.append(chromosome)
        attempts +=1

    # if we could not generate enough valid random solutions, fill with empty sacks
    while len(population) < size:
        population.append([0] * num_items)

    return population


def tournament_selection(population, fitnesses, k):
    """Selects a parent from the population using tournament selection."""
    selection_ix = random.randint(0, len(population) - 1)
    for _ in range(k - 1):
        ix = random.randint(0, len(population) - 1)
        if fitnesses[ix] > fitnesses[selection_ix]:
            selection_ix = ix
    return population[selection_ix]

def crossover(p1, p2):
    """Performs single-point crossover."""
    c1, c2 = p1[:], p2[:]
    pt = random.randint(1, len(p1) - 2)
    c1 = p1[:pt] + p2[pt:]
    c2 = p2[:pt] + p1[pt:]
    return c1, c2

def mutation(chromosome, rate):
    """Performs bit-flip mutation."""
    for i in range(len(chromosome)):
        if random.random() < rate:
            chromosome[i] = 1 - chromosome[i]

# --- Main Genetic Algorithm ---
num_items = len(items)
population = create_initial_population(POPULATION_SIZE, num_items)

best_chromosome = None
best_fitness = -1

# Previous best fitness from the last run, for comparison
previous_best_fitness = 2299.45

for gen in range(NUM_GENERATIONS):
    # Calculate fitness for each chromosome
    fitnesses = [fitness(chromo, items) for chromo in population]

    # Find the best solution in the current generation
    for i in range(len(population)):
        if fitnesses[i] > best_fitness:
            best_fitness = fitnesses[i]
            best_chromosome = population[i]

    # Create the next generation
    next_population = []
    for _ in range(POPULATION_SIZE // 2):
        # Selection
        parent1 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)
        parent2 = tournament_selection(population, fitnesses, TOURNAMENT_SIZE)

        # Crossover
        child1, child2 = crossover(parent1, parent2)

        # Mutation
        mutation(child1, MUTATION_RATE)
        mutation(child2, MUTATION_RATE)

        next_population.extend([child1, child2])

    population = next_population

# --- Results ---
best_sack_indices = [i for i, gene in enumerate(best_chromosome) if gene == 1]
best_weight, best_volume, best_value = calculate_sack_properties(best_sack_indices, items)

# Prepare the output
best_items_df = df.iloc[best_sack_indices]

print(f"Previous Best Value: {previous_best_fitness}")
if best_value > previous_best_fitness:
    print("Found a better solution!")
else:
    print("No better solution found in this run. The previous solution is still the best.")

print("\nBest Sack Found in this run:")
print(f"Total Value: {best_value:.2f}")
print(f"Total Weight: {best_weight:.2f} kg (Max: {MAX_WEIGHT} kg)")
print(f"Total Volume: {best_volume:.2f} L (Max: {MAX_VOLUME} L)")
print("\nItems in the Best Sack:")
print(best_items_df[['id', 'name', 'weight_kg', 'volume_L', 'value']])

# Create the submission file
submission_df = pd.DataFrame({'id': best_items_df['id']})
submission_df.to_csv('my_super_awesome_sack_v2.csv', index=False, header=False)
print("\nSubmission file 'my_super_awesome_sack_v2.csv' created with the new results.")
