import pygame
from pygame import Vector2
import const
import colours

class Player(pygame.sprite.Sprite):
    
    """INIT"""
    def __init__(self, game, start_position):
        super().__init__()

        # __init__ parameter assignment
        self.game = game
        self.grid = game.grid

        #sprite sheets and images
        self.movement_sheet = pygame.image.load('assets/images/player/player_movement.png')  
        self.movement_sheet.set_colorkey(colours.BLACK)
        self.movement_images = {'right': [], 'left': [], 'up': [], 'down': []}

        #set sprite rect
        self.image = self.initialise_sprite_images()
        self.rect = self.image.get_rect()
        self.current_image = self.movement_images["right"][0]

        #pacman attributes
        self.direction = None 
        self.speed = 120
        self.velocity = Vector2(1, 0)
        self.movements = [] #queue
        self.eaten = 0 
        self.eaten_power_up = False
        self.in_tunnel = False
        self.array_pos = start_position
        
    def initialise_sprite_images(self):
        frame_width = 15
        frame_height = 15 

        #init images
        for r, direction in enumerate(self.movement_images):
            for c in range(2): 
                x = (c * frame_width) 
                y = (r * frame_height) 
                rect = pygame.Rect(x, y, frame_width, frame_height)
                self.movement_images[direction].append(self.movement_sheet.subsurface(rect))
        return self.movement_images['right'][0]
    """--------------"""


    @property
    def array_pos(self):
        return self.grid.get_array_position(self.rect.center)
   
    @array_pos.setter
    def array_pos(self, position):
        self.rect.topleft =  self.grid.get_screen_position(position)
        
    
    """Update Methods"""
    def check_edge_collision(self, displacement):
        def is_boundary_collision(position):
            new_position = position + displacement
            collision = not self.grid.in_bounds(new_position)         
            return collision

        if self.direction in ("up", "left"):
            return is_boundary_collision(self.rect.topleft)
        elif self.direction == "right":
            return is_boundary_collision(self.rect.topright)
        else:
            return is_boundary_collision(self.rect.bottomleft)
        
    def check_eating(self):
        r, c = self.array_pos
    
        match self.game.grid[r][c]:
            case ".":
                self.game.grid[r][c] = ' '
                self.eaten += 1
            case "o":
                print("eaten power up")
                self.game.grid[r][c] = ' '
                self.eaten_power_up = True
                self.eaten += 1
        
    def check_traveling_through_passage(self):

        if not self.in_tunnel:
            match self.array_pos:
                case (14, 0):
                    self.array_pos = (14, 29)
                    self.in_tunnel = True
                case (14, 29):
                    self.array_pos = (14, 0)
                    self.in_tunnel = True
        else:
            if self.array_pos in ((14, 1), (14, 28)):
                self.in_tunnel = False
 
    def set_directional_velocity(self):
        target = self.grid.get_screen_position(self.array_pos) #to stop jitteriness on turning
        available_positions = self.grid.get_available_directions(self.array_pos) #the available directions the player can turn

        """
        Only changed when 
            - its a valid movement
            - The rectangle top left position is exactly on the new target position (to create smooth transition)
        """
        
        if (self.movements and self.movements[-1] in available_positions and self.rect.topleft == target):
            
            match self.movements[-1]:
                case "up":
                    self.direction = 'up'
                    self.velocity = Vector2(0, -self.speed)  
                case "down":
                    self.direction = 'down'
                    self.velocity =  Vector2(0, self.speed)
                case "left":
                    self.direction = 'left'
                    self.velocity =  Vector2(-self.speed, 0) 
                case "right":
                    self.direction = 'right'
                    self.velocity =  Vector2(self.speed, 0)
        return self.velocity
    """--------------"""


    """Default Game loop functions"""
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key:
                if event.key == pygame.K_UP and self.direction != "up":
                    self.movements.append("up")

                elif event.key == pygame.K_DOWN  and self.direction != "down":
                    self.movements.append("down")

                elif event.key == pygame.K_LEFT  and self.direction != "left":
                    self.movements.append("left")

                elif event.key == pygame.K_RIGHT  and self.direction != "right":
                    self.movements.append("right")
          
    def update(self, dt):
    
        self.check_eating()
        self.set_directional_velocity() #we get the velocity based on the available positions

        displacement = self.velocity * dt
        collision = self.check_edge_collision(displacement)
        

        if collision:
            self.rect.topleft = self.grid.get_screen_position(self.array_pos)
        else:
            self.rect.move_ip(displacement)
        
        self.check_traveling_through_passage()
 
    def draw(self, screen):
        
        if self.game.frame < 10: 
            current_frame = 0
        elif self.game.frame < 20:
            current_frame = 1
        else:
            current_frame = 0
            self.game.frame = 0
        
        if self.direction:
            self.current_image = self.movement_images[self.direction][current_frame]
        screen.blit(self.current_image, (self.rect.x - const.TILE_WIDTH, self.rect.y))
    """--------------"""