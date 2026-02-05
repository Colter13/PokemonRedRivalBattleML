
from pokemon_data import pokemon
from move_data import moves
from stat_stages import stat_modifiers
import random
import math

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

class Battle:
    def __init__(self, pokemon1, pokemon2, trainer1, trainer2):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.turn = 0
        self.verbose = False

    def health_bar(self, current_hp, max_hp, bar_length=20):
        ratio = current_hp / max_hp
        filled_length = int(bar_length * ratio)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        # green if > 0.5, yellow if > 0.2, else red
        if ratio > 0.5:
            color = "\033[92m"  # Green
        elif ratio > 0.2:
            color = "\033[93m"  # Yellow
        else:
            color = "\033[91m"  # Red
        reset = "\033[0m"
        hp_display = f"{current_hp}/{max_hp} HP"
        return f"{color}[{bar}]{reset} {hp_display:>11}"

    def display_health_bars(self):
        name_width = max(len(self.pokemon1.name), len(self.pokemon2.name))
        print(f"{self.pokemon1.name:<{name_width}}: {self.health_bar(self.pokemon1.current_hp, self.pokemon1.max_hp)}")
        print(f"{self.pokemon2.name:<{name_width}}: {self.health_bar(self.pokemon2.current_hp, self.pokemon2.max_hp)}")

    def whole_battle(self, verbose=False):
        self.verbose = verbose
        if self.verbose:
            print(f"Battle started between {self.trainer1} and {self.trainer2}!\n")
            self.display_health_bars()
            print()
        while self.pokemon1.current_hp > 0 and self.pokemon2.current_hp > 0:
            self.turn += 1
            if self.verbose:
                print(f"Turn {self.turn}:\n")

            # Move selection
            if self.trainer1 == "AI":
                pokemon1_move = self.pokemon1.random_move()
            elif self.trainer1 == "Physical":
                pokemon1_move = self.pokemon1.moveset[0]
            else:
                pokemon1_move = self.pokemon1.move_prompt()
            if self.trainer2 == "AI":
                pokemon2_move = self.pokemon2.random_move()
            elif self.trainer2 == "Physical":
                pokemon2_move = self.pokemon2.moveset[0]
            else:
                pokemon2_move = self.pokemon2.move_prompt()

            # Determine which pokemon goes first
            if self.pokemon1.stats["Speed"] > self.pokemon2.stats["Speed"]:
                first = 1
            elif self.pokemon1.stats["Speed"] < self.pokemon2.stats["Speed"]:
                first = 2
            else:
                if random.random() < 0.5:
                    first = 1
                else:
                    first = 2

            # Move execution
            if first == 1:
                if self.execute_move(pokemon1_move, self.pokemon1, self.pokemon2): break
                if self.execute_move(pokemon2_move, self.pokemon2, self.pokemon1): break
            else:
                if self.execute_move(pokemon2_move, self.pokemon2, self.pokemon1): break
                if self.execute_move(pokemon1_move, self.pokemon1, self.pokemon2): break

            if self.verbose:
                print()
            if self.verbose:
                print(f"After turn {self.turn}:")
            if self.verbose:
                self.display_health_bars()
                print()
            
        if self.verbose:
            print("Final status:")
            self.display_health_bars()
            print()
        if self.pokemon1.current_hp > 0:
            if self.verbose:
                print(f"{self.pokemon1.name} wins!")
            return True
        else:
            if self.verbose:
                print(f"{self.pokemon2.name} wins!")
            return False
    
    def execute_move(self, move, attacker, defender):
        move_data = moves[move]
        if self.verbose:
            print(f"{attacker.name} used {move}!")
        if random.randint(0, 255) > move_data["accuracy"] * 255:
            if self.verbose:
                print(f"But, it failed!\n")
            return False
        if move_data["category"] == "Physical":
            # Separate calculation depending on whether a critical hit occurred
            crit_multiplier = self.crit(attacker)
            if crit_multiplier > 1:
                # Critical: ignore attacker's and defender's stat stage modifiers
                damage = math.floor(math.floor((((2 * attacker.level * crit_multiplier) / 5 + 2) * move_data["power"] * (attacker.attack_stat / defender.defense_stat) / 50) + 2) * random.randint(217, 255) / 255)
            else:
                # Non-critical: include stat modifiers as normal
                atk = attacker.attack_stat * stat_modifiers[attacker.stat_stages["Attack"]]
                deff = defender.defense_stat * stat_modifiers[defender.stat_stages["Defense"]]
                damage = math.floor(math.floor((((2 * attacker.level) / 5 + 2) * move_data["power"] * (atk / deff) / 50) + 2) * random.randint(217, 255) / 255)
            defender.current_hp = max(0, defender.current_hp - damage)
            if defender.current_hp <= 0:
                if self.verbose:
                    print(f"{defender.name} fainted!")
                return True
            if self.verbose:
                print(f"{defender.name} took {damage} damage and has {defender.current_hp} HP left.")
        elif move_data["category"] == "Status":
            affected_stat = move_data["effect"]["stat"]
            if defender.stat_stages[affected_stat] > -6:
                defender.stat_stages[affected_stat] += move_data["effect"]["stages"]
                if self.verbose:
                    print(f"{defender.name} {affected_stat} stage changed to {defender.stat_stages[affected_stat]}")
            else:
                if self.verbose:
                    print(f"Nothing happened.")
        return False

    def crit(self, attacker):
        if random.random() < attacker.stats["Speed"] / 512:
            if self.verbose:
                print(f"A critical hit!")
            return 2
        return 1

    def reset(self):
        self.pokemon1.current_hp = self.pokemon1.max_hp
        self.pokemon2.current_hp = self.pokemon2.max_hp
        self.pokemon1.stat_stages = {
            "Attack": 0,
            "Defense": 0,
            "Special Attack": 0,
            "Special Defense": 0,
            "Speed": 0
        }
        self.pokemon2.stat_stages = {
            "Attack": 0,
            "Defense": 0,
            "Special Attack": 0,
            "Special Defense": 0,
            "Speed": 0
        }
        self.pokemon1.move_pp = {
            move: moves[move]["pp"] for move in self.pokemon1.moveset
        }
        self.pokemon2.move_pp = {
            move: moves[move]["pp"] for move in self.pokemon2.moveset
        }
        self.turn = 0