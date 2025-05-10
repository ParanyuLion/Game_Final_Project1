# Dungeon Hunter

This is an endless 2D action-adventure game by using Pygame to develop.
Players need to complete multiple levels, shooting enemies, using skills, collecting gold, and buying items from the shop.
Enemies will be stronger when level is higher. 
Players can use money that they get from shooting enemies to buy a weapon or upgrade it to make it easier to kill enemies.

## requirement
- Git
- python 3.12 (recommended)
- pygame==2.6.1
- matplotlib==3.10.1
- pandas==2.2.3
- numpy==2.2.4


## Installation and Running Instructions
1. Clone this repository:
```
git clone https://github.com/ParanyuLion/Game_Final_Project1.git
```

2. Change your directory
```
cd Game_Final_Project1
```

3. Activate virtual environment
```
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies

method 1:
```
# Windows
pip install -r requirements.txt

# if the above line not work, then do this line
python -m pip install -r requirements.txt
```

```
# macOS/Linux
python3 -m pip install -r requirements.txt
```
If method 1 is not work. Do method2

method 2:
```
# Windows
python -m pip install pygame
python -m pip install matplotlib
python -m pip install pandas
python -m pip install numpy

# macOS/Linux
python3 -m pip install pygame
python3 -m pip install matplotlib
python3 -m pip install pandas
python3 -m pip install numpy
```

5. Run the game
```
# Windows
python Run_game.py

# macOS/Linux
python3 Run_game.py
```

## How to Play
### Goal
- Defeated all enemies in levels then use money to buy items to make you stronger.
### Control
- Move: Press 'WASD' to move
- Attack: 'Left Click' to shoot (shooting direction follow a cursor)
- Drink Heal Potion: Press '1'
- Drink Mana Potion: Press '2'
- Use Fire Breathe skill: Press 'Q'
- Use Fire Breathe skill: Press 'R'
- Use Dash skill: Press 'SPACE BAR'
- Enter new level: Press 'E'


## Credits

Please see [CREDITS.md](./CREDITS.md) for full list of asset attributions.