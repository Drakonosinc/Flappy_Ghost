import sys
from Flappy_Ghost import *
from Genetic_Algorithm import *
if __name__=="__main__":
    input_size = 6 
    output_size = 2 
    game=Game()
    best_model = genetic_algorithm(game, input_size, output_size)
    game.model = best_model
    if game.mode_game["Training AI"]:save_model(game.model, torch.optim.Adam(game.model.parameters(), lr=0.001),game.model_path)
pygame.quit()
sys.exit()