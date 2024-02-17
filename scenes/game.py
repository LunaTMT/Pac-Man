import pygame
import const
import colours
import os
import random

from entities.grid import Grid
from entities.player import Player
from entities.enemy import Enemy, Blinky, Pinky, Inky, Clyde

pygame.mixer.init()

class GameScene:
    def __init__(self):
        pygame.mixer.init()
        self.background = pygame.Surface(const.SCREEN_SIZE)
        self.background.fill((0, 0, 0))  # Black background for the game scene
        
        self.score = 0
        self.highscore = 0
        self.lives = 1

        self.maze_image = pygame.image.load('assets/images/maze.jpeg') 
        self.life_image = pygame.image.load("assets/images/player/lives.png")

        self.grid = Grid.from_string(const.BASE_GRID)

        self.enemies_released = 0
        self.frame = 0
        self.prev_time = pygame.time.get_ticks()
        
        self.game_over = False
        self.started = False
        
        self.intro_sound = pygame.mixer.Sound("assets/sounds/pacman_beginning.wav")
        self.intro_sound.set_volume(0.15)

        self.siren_sound = pygame.mixer.Sound("assets/sounds/siren_1.wav")
        self.siren_sound.set_volume(0.15)

        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
        self.game_over_sound.set_volume(0.15)


        self.spawn_entities()        

        self.font = pygame.font.Font("assets/fonts/CrackMan.TTF", 32)
        self.title_font = pygame.font.Font("assets/fonts/CrackMan.TTF", 22)

        self.score_text_surface = self.font.render(str(self.score), True, colours.WHITE)  
        self.score_text =  self.score_text_surface.get_rect()
        self.score_text.center = (const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT // 2)
        
        

        print("reinit")

    def spawn_entities(self):
        
        self.player = Player(self, (23, 14))
        enemy_spawn_positions = ((14, 12), (14, 13), (14, 14), (14, 15))
        self.enemies = pygame.sprite.Group((cls(self, enemy_spawn_positions[i], i) for i, cls in enumerate((Blinky, Pinky, Inky, Clyde))))

    def check_if_release_from_pen(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - Enemy.SPAWN_TIMER
        
        if self.enemies_released < 4 and elapsed_time >= 2000:
            id = self.enemies_released
            enemy = self.enemies.sprites()[id]
            enemy.released = True
            
            Enemy.SPAWN_TIMER = pygame.time.get_ticks()
            
            self.enemies_released += 1

    def make_enemies_frightened(self):
        for enemy in self.enemies:
            enemy.set_mode('FRIGHTENED')

    def stop_enemies(self):
        for enemy in self.enemies:
            enemy.stopped = True


    def reset_game(self):
        self.lives -= 1
        self.started = False

        if self.lives > 0:
            self.player = Player(self, (23, 14))
            enemy_spawn_positions = ((14, 12), (14, 13), (14, 14), (14, 15))
            self.enemies = pygame.sprite.Group((cls(self, enemy_spawn_positions[i], i) for i, cls in enumerate((Blinky, Pinky, Inky, Clyde))))
            Enemy.SPAWN_TIMER = pygame.time.get_ticks()
            self.enemies_released = 0
        elif not self.game_over:
            self.game_over = True
            self.game_over_sound.play()
     

    def handle_events(self, event):
        if not self.game_over:
            self.player.handle_event(event)
            
        
        elif event.type == pygame.KEYDOWN:    
            self.__init__()

    def update(self):
        
        if not self.started and not self.game_over:
            self.intro_sound.play()
            self.siren_sound.play(-1)
            self.started = True


        if not self.game_over:
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.prev_time) / 1000.0  # Convert to seconds
            self.prev_time = current_time
        
            self.player.update(dt)

            for enemy in self.enemies:
                enemy.update(dt)

            self.check_if_release_from_pen()



    def draw(self, screen):
        screen.blit(self.background, (0, 0))  # Display the background
        screen.blit(self.maze_image, (0, 50))     
        
        self.grid.draw(screen)   
        self.player.draw(screen)
        #self.enemies.draw(screen)

        for enemy in self.enemies.sprites():
            enemy.draw(screen)

        self.draw_score(screen)
        self.draw_lives(screen)
        self.draw_endgame(screen)

        pygame.display.flip()


    def draw_lives(self, screen):
        for i in range(self.lives):
            screen.blit(self.life_image, ((40 * i) + 290, 12.5 ))  

    def draw_score(self, screen):
        self.score_title_surface = self.font.render("Score   ", True, colours.WHITE)
        self.score_title_rect =  self.score_title_surface.get_rect()
        self.score_title_rect.center = ((const.SCREEN_WIDTH/2) - 120, 30)
        screen.blit(self.score_title_surface, self.score_title_rect)

        self.score_text_surface = self.font.render(str(self.score), True, colours.WHITE) 
        self.score_text_rect =  self.score_text_surface.get_rect()
        self.score_text_rect.topleft = (150, 13)
        screen.blit(self.score_text_surface, self.score_text_rect)

    def draw_endgame(self, screen):
        if self.game_over:
            self.endgame_surface = self.title_font.render("Press any key to restart.", True, colours.WHITE)  
            self.endgame_surface_rect =  self.endgame_surface.get_rect()
            self.endgame_surface_rect.center = (const.SCREEN_WIDTH//2, const.SCREEN_HEIGHT//2)
            screen.blit(self.endgame_surface, self.endgame_surface_rect)
