import pygame
import const
import colours


"""The grid has power ups and pellets"""

class Grid(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_string(cls, str):
        lines = str.strip().split('\n')
        return cls([list(line) for line in lines]) #initialising the str to a grid object

    
    def draw(self, screen):
        for r in range(const.ROWS):
            for c in range(const.COLUMNS):
                char = self[r][c]  
                circle_x = (c * const.TILE_WIDTH) + const.TILE_WIDTH/2
                circle_y = (r * const.TILE_WIDTH) + const.TILE_WIDTH/2

                if char == '.': #Pellets
                    pygame.draw.circle(screen, colours.PELLETS, (circle_x, circle_y), const.TILE_WIDTH // 4)
                elif char == "o": #Power pellets
                    pygame.draw.circle(screen, colours.PELLETS, (circle_x, circle_y), const.TILE_WIDTH // 2)