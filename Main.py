import sys
from Flappy_Ghost import *
from Genetic_Algorithm import *
if __name__=="__main__":
    input_size = 6 
    output_size = 2 
    game=Game()
    best_model = genetic_algorithm(game, input_size, output_size)
    game.model = best_model
pygame.quit()
sys.exit()