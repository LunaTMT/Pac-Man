


GRID_HEIGHT = 465
TOP_EXCESS = 50

SCREEN_WIDTH = 420
SCREEN_HEIGHT = GRID_HEIGHT + TOP_EXCESS

SCREEN_SIZE = (SCREEN_WIDTH , SCREEN_HEIGHT)


SCORE_BOARD_BOTTOM_OFFSET = 45

ROWS = 31 
COLUMNS = 28   

TILE_WIDTH  = SCREEN_WIDTH  / COLUMNS  #420/28 = 15 (must be whole division)
TILE_HEIGHT = GRID_HEIGHT / ROWS   #465/31 = 15 (must be whole division)

#COLUMNS += 2 #We add two because of the secret passage

PLAYER_SPEED = 40 #16
ENEMY_SPEED = 120

SMALL_DOTS = 10
ENERGISERS = 50

MONSTER_KILL = 200
# 200, 400, 800, 1600 (2^(0-4) * 100)

"""
if all ghosts are eaten by using all the energisers + 12,000

Ghosts are eatable for several seconds on early rounds
then only a few seconds
by level 19 the ghosts stop turning blue altogether
"""

"""
#fruit) that appear directly below the monster pen twice each round for additional points.


The first bonus fruit appears after 70 dots have been cleared from the maze; 
the second one appears after 170 dots are cleared. 
Each fruit is worth anywhere from 100 to 5,000 points, depending on what level the player is currently on.
Whenever a fruit appears, 
the amount of time it stays on the screen before disappearing is always between nine and ten seconds

"""

BASE_GRID = '''
_############################_
_#............##............#_
_#.####.#####.##.#####.####.#_
_#o####.#####.##.#####.####o#_
_#.####.#####.##.#####.####.#_
_#..........................#_
_#.####.##.########.##.####.#_
_#.####.##.########.##.####.#_
_#......##....##....##......#_
_######.#####.##.#####.######_
_     #.#####.##.#####.#     _
_     #.##..........##.#     _
_     #.##.###  ###.##.#     _
_######.##.#      #.##.######_
...........#      #...........
_######.##.#      #.##.######_
_     #.##.########.##.#     _
_     #.##..........##.#     _
_     #.##.########.##.#     _
_######.##.########.##.######_
_#............##............#_
_#.####.#####.##.#####.####.#_
_#.####.#####.##.#####.####.#_
_#o..##................##..o#_
_###.##.##.########.##.##.###_
_###.##.##.########.##.##.###_
_#......##....##....##......#_
_#.##########.##.##########.#_
_#.##########.##.##########.#_
_#..........................#_
_############################_
'''




