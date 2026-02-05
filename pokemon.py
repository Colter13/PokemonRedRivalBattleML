import random
import math
from pokemon_data import pokemon
from move_data import moves

class Pokemon:
    def __init__(self, name, level):
        self.name = name
        self.primary_type = pokemon[name]["primary_type"]
        self.secondary_type = pokemon[name]["secondary_type"]
        self.level = level
        self.moveset = pokemon[name]["moveset"]
        self.stats = pokemon[name]["stats"]
        self.max_hp = math.floor((self.stats["HP"] + random.uniform(0, 15)) * 2 * level / 100) + level + 10
        self.current_hp = self.max_hp
        self.attack_stat = math.floor((self.stats["Attack"] + random.uniform(0, 15)) * 2 * level / 100) + 5
        self.defense_stat = math.floor((self.stats["Defense"] + random.uniform(0, 15)) * 2 * level / 100) + 5
        self.special_stat = math.floor((self.stats["Special"] + random.uniform(0, 15)) * 2 * level / 100) + 5
        self.speed_stat = math.floor((self.stats["Speed"] + random.uniform(0, 15)) * 2 * level / 100) + 5
        self.stat_stages = {
            "Attack": 0,
            "Defense": 0,
            "Special Attack": 0,
            "Special Defense": 0,
            "Speed": 0
        }
        self.move_pp = {
            move: moves[move]["pp"] for move in self.moveset
        }
    
    def random_move(self):
        valid_moves = [move for move in self.moveset if self.move_pp[move] > 0]
        if not valid_moves:
            return "Struggle"
        move = random.choice(valid_moves)
        self.move_pp[move] -= 1
        return move
    
    def move_prompt(self):
        while True:
            valid_moves = [move for move in self.moveset if self.move_pp[move] > 0]
            for i, move in enumerate(valid_moves):
                print(f"{i+1}. {move} - {moves[move]['pp']} PP")
            move = int(input(f"Choose a move for {self.name}: "))
            if move in range(1, len(valid_moves) + 1):
                self.move_pp[valid_moves[move - 1]] -= 1
                print()
                return valid_moves[move - 1]
            else:
                print("Invalid move selection. Please try again.\n")