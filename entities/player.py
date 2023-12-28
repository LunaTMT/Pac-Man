import pygame
from pygame import Vector2
import const


class Player(pygame.sprite.Sprite):
    def __init__(self, game, start_position):
        super().__init__()

        # __init__ parameter assignment
        self.game = game
        self.grid = game.grid
        self.x, self.y = start_position

        #sprite sheets and images
        self.movement_sheet = pygame.image.load('assets/images/player/player_movement.png')  
        self.movement_images = {'right': [], 'left': [], 'up': [], 'down': []}
        self.image = self.initialise_sprite_images()
        
        #set sprite rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (start_position)

        #pacman attributes
        self.direction = 'left' 
        self.speed = 160
        self.velocity = Vector2(1, 0)
        self.movements = [] #queue
        self.eaten = 0 
   
    #Init_method
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
  
    """Update Methods"""
    def check_edge_collision(self, displacement):
        def is_boundary_collision(position):
            new_position = position + displacement
            collision = not self.grid.in_bounds(new_position)
            
            if collision:
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
                new_array_position = Vector2(self.game.grid.get_array_position(new_position))
                new_position = new_array_position + direction_vector #shift back to old position
                #self.rect.topleft = self.game.grid.get_screen_position(new_position)
                
                return True
            return False

        if self.direction in ("up", "left"):
            return is_boundary_collision(self.rect.topleft)
        elif self.direction == "right":
            return is_boundary_collision(self.rect.topright)
        else:
            return is_boundary_collision(self.rect.bottomleft)
    def check_eating_pellet(self, position):
        r, c = position
        if self.game.grid[r][c] == ".":
            self.game.grid[r][c] = ' '
            self.eaten += 1

    def set_directional_velocity(self, array_pos, available_positions):
        # print(self.movements)

        tx, ty = target = self.grid.get_screen_position(array_pos)
 
        if self.movements and self.movements[-1] in available_positions:  #and  (tx-5, ty-5) <= self.rect.topleft <= (tx+5, ty+5):
            self.rect.topleft = self.grid.get_screen_position(array_pos)
            match self.movements[-1]:
                case "up":
                    self.direction = 'up'
                    self.velocity = Vector2(0, -self.speed)  # Set velocity for upward movement
                case "down":
                    self.direction = 'down'
                    self.velocity =  Vector2(0, self.speed)
                case "left":
                    self.direction = 'left'
                    self.velocity =  Vector2(-self.speed, 0)  # Set velocity for upward movement
                case "right":
                    self.direction = 'right'
                    self.velocity =  Vector2(self.speed, 0)
            self.movements = []
        return self.velocity
    """--------------"""

    """Default Game loop functions"""
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    self.movements.append("up")
                case pygame.K_DOWN:
                    self.movements.append("down")
                case pygame.K_LEFT:
                    self.movements.append("left")
                case pygame.K_RIGHT:
                    self.movements.append("right")
          
    def update(self, dt):
        array_pos = self.grid.get_array_position(self.rect.center) #current position on grid array
        available_positions = self.grid.get_available_directions(array_pos) #the available directions the player can turn

        self.check_eating_pellet(array_pos)
        self.set_directional_velocity(array_pos, available_positions) #we get the velocity based on the available positions
      
        displacement = self.velocity * dt

        collision = self.check_edge_collision(displacement)

        if not collision:
            self.rect.move_ip(displacement)
        
        self.rect.clamp_ip(pygame.Rect(0, 0, const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

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
