import pygame
from pygame import Vector2
import const

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        self.x, self.y = x, y
        self.movement_sheet = pygame.image.load('assets/images/player/player_movement.png')  
        
        self.images = {'right': [], 'left': [], 'up': [], 'down': []}

        frame_width = 16
        frame_height = 16  

        for r, direction in enumerate(self.images):
            for c in range(2): 
                x = (c * frame_width) + (c+1)
                y = (r * frame_height) + (r+1)
                rect = pygame.Rect(x, y, frame_width, frame_height)
                self.images[direction].append(self.movement_sheet.subsurface(rect))

        self.image = self.images['right'][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.direction = 'right' 
        
        self.speed = 160
        self.velocity = Vector2(1, 0)

    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction = 'up'
                self.velocity = Vector2(0, -self.speed)  # Set velocity for upward movement

            elif event.key == pygame.K_s:
                self.direction = 'down'
                self.velocity = Vector2(0, self.speed)  # Set velocity for downward movement

            elif event.key == pygame.K_a:
                self.direction = 'left'
                self.velocity = Vector2(-self.speed, 0)  # Set velocity for leftward movement

            elif event.key == pygame.K_d:
                self.direction = 'right'
                self.velocity = Vector2(self.speed, 0)

    def update(self, dt):
        
        self.rect.move_ip(self.velocity * dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))


    def draw(self, screen):
        
        if self.game.frame < 20: 
            current_frame = 0
        elif self.game.frame < 40:
            current_frame = 1
        else:
            current_frame = 0
            self.game.frame = 0

        print(current_frame)
       
        current_image = self.images[self.direction][current_frame]

        screen.blit(current_image, (self.rect.x, self.rect.y))
