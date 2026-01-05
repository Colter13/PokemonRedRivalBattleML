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
    
    def select_move(self):
        valid_moves = [move for move in self.moveset if self.move_pp[move] > 0]
        if not valid_moves:
            return "Struggle"
        move = random.choice(valid_moves)
        self.move_pp[move] -= 1
        return move

class Battle:
    def __init__(self, pokemon1, pokemon2, trainer1, trainer2):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.turn = 0

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

    def start(self):
        print(f"Battle started between {self.trainer1} and {self.trainer2}!\n")
        self.display_health_bars()
        print()
        while self.pokemon1.current_hp > 0 and self.pokemon2.current_hp > 0:
            self.turn += 1
            print(f"Turn {self.turn}:")
            if self.pokemon1.stats["Speed"] > self.pokemon2.stats["Speed"]:
                if self.execute_move(self.pokemon1.select_move(), self.pokemon1, self.pokemon2): break
                if self.execute_move(self.pokemon2.select_move(), self.pokemon2, self.pokemon1): break
            elif self.pokemon1.stats["Speed"] < self.pokemon2.stats["Speed"]:
                if self.execute_move(self.pokemon2.select_move(), self.pokemon2, self.pokemon1): break
                if self.execute_move(self.pokemon1.select_move(), self.pokemon1, self.pokemon2): break
            else:
                if random.random() < 0.5:
                    if self.execute_move(self.pokemon1.select_move(), self.pokemon1, self.pokemon2): break
                    if self.execute_move(self.pokemon2.select_move(), self.pokemon2, self.pokemon1): break
                else:
                    if self.execute_move(self.pokemon2.select_move(), self.pokemon2, self.pokemon1): break
                    if self.execute_move(self.pokemon1.select_move(), self.pokemon1, self.pokemon2): break
            print()
            print(f"After turn {self.turn}:")
            self.display_health_bars()
            print()
        print("Final status:")
        self.display_health_bars()
        print()
        if self.pokemon1.current_hp > 0:
            print(f"{self.pokemon1.name} wins!")
        else:
            print(f"{self.pokemon2.name} wins!")
    
    def execute_move(self, move, attacker, defender):
        move_data = moves[move]
        print(f"{attacker.name} used {move}!")
        if random.random() * 100 >= move_data["accuracy"]:
            print(f"The attack missed!\n")
            return False
        if move_data["category"] == "Physical":
            # Separate calculation depending on whether a critical hit occurred
            crit_multiplier = self.crit(attacker)
            if crit_multiplier > 1:
                # Critical: ignore attacker's and defender's stat stage modifiers
                damage = math.ceil((((2 * attacker.level * crit_multiplier) * move_data["power"] * (attacker.stats["Attack"] / defender.stats["Defense"]) / 50 + 2) * random.uniform(85, 100) / 100))
            else:
                # Non-critical: include stat modifiers as normal
                atk = attacker.stats["Attack"] * stat_modifiers[attacker.stat_stages["Attack"]]
                deff = defender.stats["Defense"] * stat_modifiers[defender.stat_stages["Defense"]]
                damage = math.ceil((((2 * attacker.level) * move_data["power"] * (atk / deff) / 50 + 2) * random.uniform(85, 100) / 100))
            defender.current_hp = max(0, defender.current_hp - damage)
            if defender.current_hp <= 0:
                print(f"{defender.name} fainted!")
                return True
            print(f"{defender.name} took {damage} damage and has {defender.current_hp} HP left.")
        elif move_data["category"] == "Status":
            affected_stat = move_data["effect"]["stat"]
            if defender.stat_stages[affected_stat] > -6:
                defender.stat_stages[affected_stat] += move_data["effect"]["stages"]
                print(f"{defender.name} {affected_stat} stage changed to {defender.stat_stages[affected_stat]}")
            else:
                print(f"Nothing happened.")
        return False

    def crit(self, attacker):
        if random.random() < attacker.stats["Speed"] / 512:
            print(f"A critical hit!")
            return 2
        return 1

battle = Battle(Pokemon("Bulbasaur", 5), Pokemon("Charmander", 5), "Ash", "Gary")
battle.start()