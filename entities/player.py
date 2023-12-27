import pygame
from pygame import Vector2
import const

class Player(pygame.sprite.Sprite):
    def __init__(self, game, start_position):
        super().__init__()

        self.game = game
        self.x, self.y = start_position
        self.movement_sheet = pygame.image.load('assets/images/player/player_movement.png')  
        
        self.movement_images = {'right': [], 'left': [], 'up': [], 'down': []}
        
        self.image = self.initialise_sprite_images()
        self.rect = self.image.get_rect()
        self.rect.topleft = (start_position)

        self.previous_direction = self.direction = 'left' 
        
        self.speed = 160
        self.velocity = Vector2(1, 0)

        self.movements = []

   


    def initialise_sprite_images(self):
        frame_width = 16
        frame_height = 16  

        #init images
        for r, direction in enumerate(self.movement_images):
            for c in range(2): 
                x = (c * frame_width) + (c+1)
                y = (r * frame_height) + (r+1)
                rect = pygame.Rect(x, y, frame_width, frame_height)
                self.movement_images[direction].append(self.movement_sheet.subsurface(rect))
        
        return self.movement_images['right'][0]

    def handle_event(self, event):

        """
        I should not allow changing direction unless it is the directions opposite

        For example I go either left or right, then I should allow the up or down direction
        whilst there is a wall there
        """
        if event.type == pygame.KEYDOWN:
            self.previous_direction = self.direction
            if event.key in (pygame.K_w, pygame.K_UP):
                self.direction = 'up'
                self.velocity = Vector2(0, -self.speed)  # Set velocity for upward movement

            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.direction = 'down'
                self.velocity = Vector2(0, self.speed)  # Set velocity for downward movement

            elif event.key in (pygame.K_a, pygame.K_LEFT):
                self.direction = 'left'
                self.velocity = Vector2(-self.speed, 0)  # Set velocity for leftward movement

            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.direction = 'right'
                self.velocity = Vector2(self.speed, 0)  # Set velocity for rightward movement


    def update(self, dt):
        
        """
        I should only update the player every direction/collision for every time they''re bang on a pellet?
        """

        displacement = self.velocity * dt


        if self.direction in ("up", "left"):
            collision = self.check_boundary_collision(self.rect.topleft, displacement)
        elif self.direction == "right":
            collision = self.check_boundary_collision(self.rect.topright, displacement)
        else:
            collision = self.check_boundary_collision(self.rect.bottomleft, displacement)


        if not collision:
            self.rect.move_ip(displacement)
        else:
            print("Collision")
        self.rect.clamp_ip(pygame.Rect(0, 0, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
       

    def check_boundary_collision(self, position, displacement):
        
        new_position = position + displacement
        collision = not self.game.grid.in_bounds(new_position)
        
        if collision:
            print("collision")
            match self.direction:
                case "up":
                    direction_vector = Vector2(1, 0)
                case "left":
                    direction_vector = Vector2(0, 1)
                case "down":
                    direction_vector = Vector2(-1, 0)
                case "right":
                    direction_vector = Vector2(0, -1)
                case _:
                    return

        
            #As collided we must return to old position
            #Get array position and add the opposite vector (direction_vector)
            #Get the screen position of this 'old position' and update the direction back to previous one
            new_array_position = Vector2(self.game.grid.getArrayPosition(new_position))
            new_position = new_array_position + direction_vector #shift back to old position
            self.rect.topleft = self.game.grid.getScreenPosition(new_position)
            #self.direction = self.previous_direction
            
            return True
        return False

    def draw(self, screen):
        
        if self.game.frame < 20: 
            current_frame = 0
        elif self.game.frame < 40:
            current_frame = 1
        else:
            current_frame = 0
            self.game.frame = 0

        #print(current_frame)
        #if not self.collision:
        current_image = self.movement_images[self.direction][current_frame]

        screen.blit(current_image, (self.rect.x, self.rect.y))
