import random
from Neural_Network import *
import numpy as np

def fitness_function(model, game):
    game.model = model
    score = game.run_with_model()
    print(f"Score: {score}")
    return score

def initialize_population(size, input_size, output_size):
    return [SimpleNN(input_size, output_size) for _ in range(size)]

def evaluate_population(population, game, num_trials=3):
    fitness_scores = []
    for model in population:
        scores = [fitness_function(model, game) for _ in range(num_trials)]
        fitness_scores.append(sum(scores) / num_trials)
    return fitness_scores

def select_top_individuals(population, fitness_scores, num_selected):
    sorted_indices = np.argsort(fitness_scores)[::-1]
    return [population[i] for i in sorted_indices[:num_selected]]

def tournament_selection(population, fitness_scores, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])
        selected.append(winner[0])
    return selected

def weighted_crossover(parent1, parent2, alpha=0.7):
    child1, child2 = (
        SimpleNN(parent1.fc1.in_features, parent2.fc3.out_features),
        SimpleNN(parent2.fc1.in_features, parent1.fc3.out_features),
    )
    for p1, p2, c1, c2 in zip(parent1.parameters(), parent2.parameters(), child1.parameters(), child2.parameters()):
        c1.data.copy_(alpha * p1.data + (1 - alpha) * p2.data)
        c2.data.copy_((1 - alpha) * p1.data + alpha * p2.data)
    return child1, child2

def mutate(model, mutation_rate=0.02, strong_mutation_rate=0.1):
    with torch.no_grad():
        for param in model.parameters():
            if random.random() < mutation_rate:
                param.add_(torch.clamp(torch.randn(param.size()) * 0.2, -0.5, 0.5))
            if random.random() < strong_mutation_rate:
                param.add_(torch.clamp(torch.randn(param.size()) * 0.7, -1.0, 1.0))
    return model

def inverted_mutation(model):
    with torch.no_grad():
        for param in model.parameters():
            param.mul_(-1)
    return model

def hybrid_optimization(elites, game, learning_rate=0.001, steps=5):
    for elite in elites:
        optimizer = torch.optim.Adam(elite.parameters(), lr=learning_rate)
        for _ in range(steps):
            state = torch.tensor(game.get_state(), dtype=torch.float32)
            
            # Ejecutar el modelo con el estado actual
            predicted_action = elite(state)
            
            # Fitness como negativo para optimizarlo directamente
            score = fitness_function(elite, game)
            loss = -torch.tensor(score, dtype=torch.float32, requires_grad=True)  # Convertir a tensor
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

def genetic_algorithm_optimized(game, input_size, output_size, generations=100, population_size=20, 
                                elitism_rate=0.05, tournament_size=3, mutation_rate=0.02, 
                                strong_mutation_rate=0.05):
    population = initialize_population(population_size, input_size, output_size)
    elite_size = max(1, int(elitism_rate * population_size))

    for generation in range(generations):
        print(f"Generation {generation + 1}")
        game.generation = generation

        # Evaluación
        fitness_scores = evaluate_population(population, game)
        print(f"Fitness Scores: {fitness_scores}")

        # Selección de élite
        elites = select_top_individuals(population, fitness_scores, elite_size)
        
        # Selección (torneo)
        parents = tournament_selection(population, fitness_scores, tournament_size)

        # Reproducción
        next_population = elites[:]
        for i in range(0, len(parents) - elite_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1, child2 = weighted_crossover(parent1, parent2)
            next_population.append(mutate(child1, mutation_rate, strong_mutation_rate))
            if len(next_population) < population_size:
                next_population.append(mutate(child2, mutation_rate, strong_mutation_rate))

        # Diversificación periódica
        if generation % 10 == 0:
            num_random = population_size // 5
            random_models = initialize_population(num_random, input_size, output_size)
            inverted_models = [inverted_mutation(model) for model in elites]
            next_population = next_population[:population_size - num_random] + random_models + inverted_models

        # Optimización híbrida
        hybrid_optimization(elites, game)

        population = next_population[:population_size]

    # Selección del mejor modelo
    fitness_scores = evaluate_population(population, game)
    best_model = population[fitness_scores.index(max(fitness_scores))]
    game.model = best_model
    return best_model

def save_model(model, optimizer, path):
    print("save model")
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, path)

def load_model(path, input_size, output_size, optimizer=None):
    try:
        print("load model")
        model = SimpleNN(input_size, output_size)
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint['model_state_dict'])
        if optimizer:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model
    except FileNotFoundError:
        print(f"The file {path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None