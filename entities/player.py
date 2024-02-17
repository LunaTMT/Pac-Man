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
        
        self.death_sheet = pygame.image.load('assets/images/player/player_death.png')  
        self.death_sheet.set_colorkey(colours.BLACK)
        self.death_images = []

        self.current_images = self.movement_images

        self.initialise_sprite_images()

        #set sprite rect
        self.image = self.movement_images['right'][0]
        self.rect = self.image.get_rect()
        self.current_image = self.movement_images["right"][0]

        #pacman attributes
        self.direction = None 
        self.speed = 120
        self.boost_speed = self.speed + 4
        self.boost_timer = 0
        self.velocity = Vector2(0, 0)
        self.movements = [] #queue
        self.eaten = 0 
        self.eaten_power_up = False
        self.in_tunnel = False
        self.dead = False

        r, c = start_position
        self.array_pos = (r, c+1) #Its very akward but we must account for _ in const.grid for the magic tunnel
        #thus top left position is not actually (1,1) but (1, 2)

        self.has_moved_from_default = False


        self.quadrants = {"Q1": {"R"        : [0, 15],
                                 "C"        : [2, 14],
                                 "OPP"      : "Q4",
                                 "CORNER"   : (1, 2)},

                          "Q2": {"R"        : [0, 15],
                                 "C"        : [15, 27],
                                 "OPP"      : "Q3",
                                 "CORNER"   : (1, 27)},

                          "Q3": {"R"        : [15, 28],
                                 "C"        : [2, 14],
                                 "OPP"      : "Q2",
                                 "CORNER"   : (29, 2)},

                          "Q4": {"R"        : [15, 28],
                                 "C"        : [15, 27],
                                 "OPP"      : "Q1",
                                 "CORNER"   : (29, 27)}}

        
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
        

        for i in range(12):
            x = i * 15
            y = 0
            rect = pygame.Rect(x, y, frame_width, frame_height)
            self.death_images.append(self.death_sheet.subsurface(rect))

    """--------------"""

    """Properties"""
    @property
    def array_pos(self):
        return self.grid.get_array_position(self.rect.center)
   
    @array_pos.setter
    def array_pos(self, position):
        self.rect.topleft = self.grid.get_screen_position(position)

    @property
    def screen_pos(self):
        return self.grid.get_screen_position(self.array_pos)
    
    @property
    def opposite_grid_position(self):
        for boundary in self.quadrants.values():
            row_bound, col_bound, opposite, _ = boundary.values()
            row, col = self.array_pos

            if row_bound[0] <= row < row_bound[1] and col_bound[0] <= col <= col_bound[1]:
                return self.quadrants[opposite]["CORNER"]



    """--------------"""  

    """Update Methods"""
    def check_edge_collision(self, displacement):
        def is_boundary_collision(position):
            new_position = position + displacement
            collision = not self.grid.in_bounds(self.grid.get_array_position(new_position))
            return collision

        if self.direction in ("up", "left"):
            return is_boundary_collision(self.rect.topleft)
        elif self.direction == "right":
            return is_boundary_collision(self.rect.topright)
        elif self.direction == "down":
            return is_boundary_collision(self.rect.bottomleft)
        else:
            return False
        
    def check_eating(self):
        r, c = self.array_pos
        self.current_arr_pos = (r, c)
       #Play sound here
        match self.game.grid[r][c]:
            case ".":
                self.game.grid[r][c] = ' '
                self.game.score += 10
            case "o":
                self.game.grid[r][c] = ' '
                self.eaten_power_up = True
                self.game.score += 100
                self.game.make_enemies_frightened()
                
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

    def check_collision(self):
        collisions = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in collisions:
            if not enemy.eaten:
                if enemy.mode == "FRIGHTENED":
                    self.game.score += 200
                    enemy.eaten = True
                    enemy.speed = 200
            
                else:
                    self.dead = True
                    self.death_timer = pygame.time.get_ticks()
                    self.game.stop_enemies()

    def update_directional_velocity(self):
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
            
            and not self.in_tunnel

            and self.rect.topleft == target):

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


            #We dont want to boost on first move
            if not self.has_moved_from_default:
                self.has_moved_from_default = True

            #Of course at the end update the current direction 
            self.direction = self.movements[-1]
        
     
    
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
                    self.collision = False

                elif event.key == pygame.K_DOWN  and self.direction != "down":
                    self.movements.append("down")
                    self.collision = False

                elif event.key == pygame.K_LEFT  and self.direction != "left":
                    self.movements.append("left")
                    self.collision = False

                elif event.key == pygame.K_RIGHT  and self.direction != "right":
                    self.movements.append("right")
                    self.collision = False
          
    def update(self, dt):
        if not self.dead:

            self.check_eating()
            self.check_traveling_through_passage()
            self.check_collision()

            self.update_directional_velocity()
            self.check_booster_finished() 
            

            displacement = self.velocity * dt
            collision = self.check_edge_collision(displacement)


            if collision:
                self.array_pos = self.array_pos
            else:
                self.rect.move_ip(displacement)
            
    def draw(self, screen):
        
        if self.dead:
            self.draw_death()
        else:
            if self.game.frame < 10: 
                current_frame = 0
            elif self.game.frame < 20:
                current_frame = 1
            else:
                current_frame = 0
                self.game.frame = 0
            
            if self.direction:
                self.current_image = self.movement_images[self.direction][current_frame]
        
        x, y = self.rect.topleft
        screen.blit(self.current_image, (x-const.TILE_WIDTH, y+50))

    def draw_death(self):
        elapsed_time = pygame.time.get_ticks() - self.death_timer

        if elapsed_time >= 1500:
            self.current_image = self.death_images[-1]

            if elapsed_time >= 2000:
                self.game.reset_game()
        else:
            self.current_image = self.death_images[elapsed_time // 125]



    """--------------"""