import sys
from Flappy_Ghost import *
from Genetic_Algorithm import *
if __name__=="__main__":
    best_model = genetic_algorithm_optimized(game:=Game(), input_size=len(game.get_state()), output_size=1)
    game.models[0] = best_model
    if game.config_AI["model_save"]:save_model(game.models[0], torch.optim.Adam(game.models[0].parameters(), lr=0.001),game.model_path)
pygame.quit(),sys.exit()