from battle import Battle, Pokemon

battle = Battle(Pokemon("Bulbasaur", 5), Pokemon("Charmander", 5), "AI", "Physical")

Bulbasaur_wins = 0
Charmander_wins = 0
for i in range(1000):
    result = battle.whole_battle(verbose=False)
    battle.reset()
    if result:
        Bulbasaur_wins += 1
    else:
        Charmander_wins += 1
print(f"Bulbasaur wins: {Bulbasaur_wins} times")
print(f"Charmander wins: {Charmander_wins} times")
print(f"Total battles: {Bulbasaur_wins + Charmander_wins}")
print(f"Win percentage: {Bulbasaur_wins / (Bulbasaur_wins + Charmander_wins) * 100}%")