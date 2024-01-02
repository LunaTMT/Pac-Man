import pygame
from pygame.sprite import _Group

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, start_position):
        super().__init__()

        self.game = game
        self.grid = game.grid
        self.x, self.y = start_position
    
        self.behaviour = ("CHASE", "SCATTER", "FRIGHTENED")
        """
           Blinky (red) is very aggressive and hard to shake once he gets behind you, 
           Pinky  (pink) tends to get in front of you and cut you off, 
           Inky   (light blue) is the least predictable of the bunch, 
           Clyde  (orange) seems to do his own thing and stay out of the way.
        """