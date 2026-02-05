from battle import Battle, Pokemon

battle = Battle(Pokemon("Bulbasaur", 5), Pokemon("Charmander", 5), "Physical", "Physical")

pokemon1_wins = 0
pokemon2_wins = 0
for i in range(1000):
    result = battle.whole_battle(verbose=False)
    battle.reset(stat_reset=False)
    if result:
        pokemon1_wins += 1
    else:
        pokemon2_wins += 1
print(f"{battle.pokemon1.name} wins: {pokemon1_wins} times")
print(f"{battle.pokemon2.name} wins: {pokemon2_wins} times")
print(f"Total battles: {pokemon1_wins + pokemon2_wins}")
print(f"Win percentage: {pokemon1_wins / (pokemon1_wins + pokemon2_wins) * 100}%")
