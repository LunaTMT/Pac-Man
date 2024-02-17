import pygame

import colours
import const

class MainMenu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 36)
        self.title_text = self.title_font.render("Pacman Game", True, colours.WHITE)
        self.start_text = self.menu_font.render("Press Enter to Start", True, colours.WHITE)
        self.quit_text = self.menu_font.render("Press Q to Quit", True, colours.WHITE)


        self.title_x = (const.SCREEN_WIDTH  - self.title_text.get_width()) // 2
        self.start_x = (const.SCREEN_WIDTH  - self.start_text.get_width()) // 2
        self.quit_x  = (const.SCREEN_WIDTH  - self.quit_text.get_width()) // 2

    def draw(self, screen):
        screen.fill(colours.BLACK) 
    
        screen.blit(self.title_text, (self.title_x, 200))
        screen.blit(self.start_text, (self.start_x, 300))
        screen.blit(self.quit_text,  (self.quit_x, 350))
        
        pygame.display.flip()
