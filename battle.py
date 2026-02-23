import random
import math
from pokemon import Pokemon
from move_data import moves
from stat_stages import stat_modifiers

class Battle:
    def __init__(self, pokemon1_name, pokemon2_name, trainer1, trainer2):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.pokemon1 = Pokemon(pokemon1_name, 5)
        self.pokemon2 = Pokemon(pokemon2_name, 5)
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
            if self.step(): break
            
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

    def reset(self, stat_reset=True):
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
        if stat_reset:
            self.pokemon1.regenerate_stats()
            self.pokemon2.regenerate_stats()
    
    def step(self, pokemon1_move=None):
        self.turn += 1
        if self.verbose:
            print(f"Turn {self.turn}:\n")

        # Pokemon 1 move selection
        if pokemon1_move is None:
            if self.trainer1 == "AI":
                pokemon1_move = self.pokemon1.random_move()
            elif self.trainer1 == "Physical":
                pokemon1_move = self.pokemon1.moveset[0]
            else:
                pokemon1_move = self.pokemon1.move_prompt()

        # Pokemon 2 move selection
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
            if self.execute_move(pokemon1_move, self.pokemon1, self.pokemon2): return True
            if self.execute_move(pokemon2_move, self.pokemon2, self.pokemon1): return True
        else:
            if self.execute_move(pokemon2_move, self.pokemon2, self.pokemon1): return True
            if self.execute_move(pokemon1_move, self.pokemon1, self.pokemon2): return True
        if self.verbose:
            print()
            print(f"After turn {self.turn}:")
            self.display_health_bars()
            print()
        return False