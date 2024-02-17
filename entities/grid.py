import pygame
import const
import colours
from .player import Player
from .enemy import Enemy
from pygame import Vector2


"""The grid has power ups and pellets"""

class Grid(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_string(cls, str):
        lines = str.strip().split('\n')
        return cls([list(line) for line in lines]) #initialising the str to a grid object


    def get_screen_position(self, position):
        row, column = position
        return ((column) * const.TILE_WIDTH, (row) * const.TILE_HEIGHT)

    def get_array_position(self, position):
        x, y = position
        return (int(y // const.TILE_HEIGHT), int(x // const.TILE_WIDTH))

    def get_available_directions(self, actor, position):
        r, c = position

        available = []
    
        for dr, dc, direction in ((-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")):
            new_r = r + dr
            new_c = c + dc
            if self.in_borders((new_r, new_c)) and self[new_r][new_c] != '#':
                
                if isinstance(actor, Player) and not (new_r == 12 and (14 <= new_c <= 15)): 
                    available.append(direction)
                elif isinstance(actor, Enemy):
                    print(direction)
                    available.append(direction)

        return available

    def in_bounds(self, position):
        r, c = position
        return self[r][c] != "#" 

    def in_borders(self, position):
        r, c = position
        return (0 <= r < const.ROWS and 0 <= c < const.COLUMNS)

    
    def draw(self, screen):
        for r in range(const.ROWS):
            for c in range(const.COLUMNS+1):
                char = self[r][c]  
                rect_x = (c * const.TILE_WIDTH) -  const.TILE_WIDTH
                rect_y = (r * const.TILE_HEIGHT) + 50

                circle_x = rect_x + (const.TILE_WIDTH/2) 
                circle_y = rect_y + (const.TILE_HEIGHT/2) 


                if char == "p":
                    rect = pygame.Rect(rect_x, rect_y, const.TILE_WIDTH, const.TILE_HEIGHT)
                    #pygame.draw.rect(screen, colours.WHITE, rect)

                if char == '.': #Pellets
                    rect = pygame.Rect(rect_x, rect_y, const.TILE_WIDTH, const.TILE_HEIGHT)
                    #pygame.draw.rect(screen, colours.YELLOW, rect)

                    pygame.draw.circle(screen, colours.PELLETS, (circle_x, circle_y), const.TILE_WIDTH // 4)

                elif char == "o": #Power pellets
                    rect = pygame.Rect(rect_x , rect_y, const.TILE_WIDTH, const.TILE_HEIGHT)
                    #pygame.draw.rect(screen, colours.YELLOW, rect)

                    pygame.draw.circle(screen, colours.PELLETS, (circle_x, circle_y), const.TILE_WIDTH // 2)
                elif char == "#":
                    rect = pygame.Rect(rect_x, rect_y, const.TILE_WIDTH, const.TILE_HEIGHT)
                    #pygame.draw.rect(screen, colours.BLUE, rect)

                