import sys
from Flappy_Ghost import *
from Genetic_Algorithm import *
if __name__=="__main__":
    while True:
        (game:=Game()).run()
        game.game_over=False
        match game.mode_game:
            case {"Training AI": True}:
                best_model = genetic_algorithm(game, input_size=len(game.get_state()), output_size=1, generations=game.config_AI["generation_value"], population_size=game.config_AI["population_value"], num_trials=game.config_AI["try_for_ai"])
                game.models[0] = best_model
                if game.config_AI["model_save"]:save_model(game.models[0], torch.optim.Adam(game.models[0].parameters(), lr=0.001),game.model_path)
            case {"Player": True} | {"AI": True}:game.run_with_models()
        if game.exit:break
pygame.quit(),sys.exit()