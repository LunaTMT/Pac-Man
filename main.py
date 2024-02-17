import pygame
from scenes.game import GameScene
from scenes.main_menu import MainMenu
import const    

if __name__ == "__main__":

    # Initialize Pygame
    pygame.init()

    # Set up the screen 
    screen = pygame.display.set_mode(const.SCREEN_SIZE)
    pygame.display.set_caption("Pacman Game")

    # Scenes
    current_scene = main_menu = MainMenu()
    game = GameScene() 
    
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if current_scene == main_menu:
                    if event.key == pygame.K_RETURN:
                        current_scene = game
                    elif event.key == pygame.K_q:
                        running = False 
        
            if current_scene == game:
                game.handle_events(event)

        if current_scene == main_menu:
            main_menu.draw(screen)
        else:
            game.update()  
            game.draw(screen) 
            game.frame += 1 

        fps = clock.get_fps()
        clock.tick(60) 

    pygame.quit()
