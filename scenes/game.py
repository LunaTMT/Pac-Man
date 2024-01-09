import pygame
import const
import colours
import os


from entities.grid import Grid
from entities.player import Player
from entities.enemy import Enemy


class GameScene:
    def __init__(self):
        self.background = pygame.Surface(const.SCREEN_SIZE)
        self.background.fill((0, 0, 0))  # Black background for the game scene
        self.game_font = pygame.font.Font(None, 36)
        self.score = 0

        self.maze_image = pygame.image.load('assets/images/maze.jpeg') 
        self.grid = Grid.from_string(const.BASE_GRID)

        self.frame = 0
        self.prev_time = pygame.time.get_ticks()
        
        self.enemies_released = 0

        self.spawn_entities()        
        

    def spawn_entities(self):
        self.player = Player(self, (23, 14))
        enemy_spawn_positions = ((14, 12), (14, 13), (14, 14), (14, 15))
        self.enemies = pygame.sprite.Group((Enemy(self, enemy_spawn_positions[i], i) for i in range(4)))
        
    def check_if_release_from_pen(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - Enemy.SPAWN_TIMER
        
        if self.enemies_released < 4 and elapsed_time >= 4000:
            id = self.enemies_released

            self.enemies.sprites()[id].release = True
            Enemy.SPAWN_TIMER = pygame.time.get_ticks()
            self.enemies_released += 1

    def handle_events(self, event):
        self.player.handle_event(event)

    def update(self):
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.prev_time) / 1000.0  # Convert to seconds
        self.prev_time = current_time
        
        self.player.update(dt)
        self.player.collision = False

        self.enemies.update(dt)
        self.check_if_release_from_pen()

        os.system('clear')
        for enemy in self.enemies.sprites():
            print(enemy)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))  # Display the background
        screen.blit(self.maze_image, (0, 0))     
        
        self.grid.draw(screen)   
        self.player.draw(screen)
        self.enemies.draw(screen)

        pygame.display.flip()

   