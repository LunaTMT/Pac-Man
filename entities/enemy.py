import pygame
from pygame.sprite import _Group

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, start_position):
        super().__init__()

        self.game = game
        self.grid = game.grid
        self.x, self.y = start_position
    
    