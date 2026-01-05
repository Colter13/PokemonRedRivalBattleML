# PokemonRedRivalBattleML

## Main Idea
This project is an attempt to create an ai that can play the first rival battle from Pokemon Red optimally. The battle is very simple with one lvl. 5 starter vs. another lvl. 5 starter. Both pokemon have one attacking move and one stat-modifying move. 

In order to execute this project it is necessary to first build a simulation environment that matches the Pokemon Red mechanics exactly. After the simulation environment is set up, an AI will complete several iterations of battling the rival AI until an optimal strategy is found using reinforcement learning.

## Simulation Environment
There should be three potential functions of the environment:
1. User vs. User
2. User vs. Rival AI
3. Rival AI vs. Rival AI

For starters, the first function will be created.

### User vs. User Base Environment
A distinction can be made between static attributes and dynamic attributes for the purposes of this battle. Static attributes will stay the same throughout the battle. Dynamic attributes have the potential to change.

Static Attributes:
* Pokemon
* Typing
* IVs and EVs
* Moves

Dynamic Attributes:
* Health
* Stat stages
* Move PP