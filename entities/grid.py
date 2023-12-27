import pygame
import const
import colours

from pygame import Vector2


"""The grid has power ups and pellets"""

class Grid(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_string(cls, str):
        lines = str.strip().split('\n')
        return cls([list(line) for line in lines]) #initialising the str to a grid object

    def getScreenPosition(self, position):
        row, column = position
        return Vector2(column * const.TILE_WIDTH, row * const.TILE_HEIGHT)
        

    def getArrayPosition(self, position):
        x, y = position
        return (int(y // const.TILE_HEIGHT), int(x // const.TILE_WIDTH))

    def in_bounds(self, position):
        r, c = self.getArrayPosition(position)
        return self[r][c] != "#"

    
    def draw(self, screen):
        for r in range(const.ROWS):
            for c in range(const.COLUMNS):
                char = self[r][c]  
                rect_x = (c * const.TILE_WIDTH) #+ const.TILE_WIDTH/2
                rect_y = (r * const.TILE_WIDTH) #+ const.TILE_WIDTH/2

                circle_x = rect_x + (const.TILE_WIDTH/2)
                circle_y = rect_y + (const.TILE_HEIGHT/2)


                if char == '.': #Pellets
                    rect = pygame.Rect(rect_x, rect_y, const.TILE_WIDTH, const.TILE_HEIGHT)
                    pygame.draw.rect(screen, colours.YELLOW, rect)

                    pygame.draw.circle(screen, colours.PELLETS, (circle_x, circle_y), const.TILE_WIDTH // 4)
                elif char == "o": #Power pellets
                    rect = pygame.Rect(rect_x , rect_y, const.TILE_WIDTH, const.TILE_HEIGHT)
                    pygame.draw.rect(screen, colours.YELLOW, rect)

                    pygame.draw.circle(screen, colours.PELLETS, (circle_x, circle_y), const.TILE_WIDTH // 2)
                elif char == "#":
                    rect = pygame.Rect(rect_x, rect_y, const.TILE_WIDTH, const.TILE_HEIGHT)
                    pygame.draw.rect(screen, colours.BLUE, rect)