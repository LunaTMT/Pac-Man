import pygame
import const
import colours

import const
from entities.grid import Grid
from entities.player import Player


class GameScene:
    def __init__(self):
        self.background = pygame.Surface(const.SCREEN_SIZE)
        self.background.fill((0, 0, 0))  # Black background for the game scene
        self.game_font = pygame.font.Font(None, 36)
        self.score = 0

        self.maze_image = pygame.image.load('assets/images/maze.jpeg') 
        self.grid = Grid.from_string(const.BASE_GRID)

        self.frame = 0
        
        self.player = Player(self, x=100, y=100)
        self.prev_time = pygame.time.get_ticks()


    def handle_events(self, event):
        self.player.handle_event(event)

    def update(self):
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.prev_time) / 1000.0  # Convert to seconds
        self.prev_time = current_time
        

        self.player.update(dt)
    
    def draw(self, screen):
        screen.blit(self.background, (0, 0))  # Display the background
        screen.blit(self.maze_image, (0, 0))     
        self.grid.draw(screen)   
        self.player.draw(screen)

        pygame.display.flip()

   