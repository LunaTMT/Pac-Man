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
        self.boost_speed = self.speed + 3
        self.boost_timer = 0
        self.velocity = Vector2(1, 0)
        self.movements = [] #queue
        self.eaten = 0 
        self.eaten_power_up = False
        self.in_tunnel = False
        self.array_pos = start_position

        self.has_moved_from_default = False
        
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

    """Properties"""
    @property
    def array_pos(self):
        return self.grid.get_array_position(self.rect.center)
   
    @array_pos.setter
    def array_pos(self, position):
        self.rect.topleft =  self.grid.get_screen_position(position)
    """--------------"""  

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
 
    def check_booster_finished(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.boost_timer >= 500:
            self.set_velocity(self.direction, self.speed)
            self.boost_timer = 0
            return True
        return False


    def set_directional_velocity(self):
        target = self.grid.get_screen_position(self.array_pos) #to stop jitteriness on turning
        available_positions_on_grid = self.grid.get_available_directions(self, self.array_pos) #the available directions the player can turn
        
        """ So long as there are actual movements in the queue
            AND this movement is an available position on the grid
            AND the player is bang on the target position (used to ensure smooth transition)
            AND the player is not in the secret tunnel 
            (^ otherwise they can glitch out of board as there are no boundaries for above and below in tunnel (SEE ARRAY IN CONST VAL = "_"))    
        """
        if (self.movements 
            and self.movements[-1] in available_positions_on_grid 
            and self.rect.topleft == target 
            and not self.in_tunnel):

            movement = self.movements[-1]

            """
            In the following we change the velocity based on the direction

            However the direction we turn is import for the speed we set the player at:
                We only want to give a boost when the user turns a corner, this would come under as an ALTERNATIVE DIRECTION
                The speed remains the default when turning around (AN OPPOSITE DIRECTION)
            """

            if movement == self.get_current_direction_opposite():
                self.set_velocity(self.movements[-1], self.speed)

            elif movement in self.get_current_direction_alternatives():
                self.set_velocity(self.movements[-1], self.boost_speed)
                self.boost_timer = pygame.time.get_ticks()
                print("boosting")    #boost


            #We dont want to boost on first move
            if not self.has_moved_from_default:
                self.has_moved_from_default = True

            #Of course at the end update the current direction 
            self.direction = self.movements[-1]
        
        return self.velocity
    
    def set_velocity(self, direction, speed):
        match direction:
            case "up":
                self.velocity = Vector2(0, -speed)  
            case "down":
                self.velocity = Vector2(0, speed)
            case "left":
                self.velocity = Vector2(-speed, 0) 
            case "right":
                self.velocity = Vector2(speed, 0)


    def get_current_direction_opposite(self):
        match self.direction:
            case "up":
                return "down"
            case "down":
                return "up"
            case "left":
                return "right"
            case "right":
                return "left"
    
    def get_current_direction_alternatives(self):
        if self.direction in ("up", "down"):
            return ("left", "right")
        return ("up", "down")
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
        self.check_traveling_through_passage()

        self.set_directional_velocity()
        self.check_booster_finished() 

        displacement = self.velocity * dt
        collision = self.check_edge_collision(displacement)

        #Finally make our movement
        if collision:
            self.rect.topleft = self.grid.get_screen_position(self.array_pos) #ensures its on exact square 
        else:
            self.rect.move_ip(displacement)
            
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