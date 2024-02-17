import pygame
import colours
import const
import heapq
import random

from math import sqrt
from pygame import Vector2

class Enemy(pygame.sprite.Sprite):
     # Set the desired speed here

    SPAWN_TIMER = -3000
    CIRCLE_RADIUS = const.TILE_WIDTH * 5

    MOVEMENT_SHEET = pygame.image.load('assets/images/enemy/enemies.jpeg')
    MOVEMENT_IMAGES = {
        0: {'right': [], 'down': [], 'left': [], 'up': []},
        1: {'right': [], 'down': [], 'left': [], 'up': []},
        2: {'right': [], 'down': [], 'left': [], 'up': []},
        3: {'right': [], 'down': [], 'left': [], 'up': []},
        4: {'right': [], 'down': [], 'left': [], 'up': []}} #4 == dead
    
    direction_starting_points = [0, 30, 60, 90]
    for id, directions in MOVEMENT_IMAGES.items():
        for d_id, direction in enumerate(directions):
            for c in range(2):
                x = direction_starting_points[d_id] + (c * const.TILE_WIDTH)
                y = (id * const.TILE_HEIGHT)
               
                rect = pygame.Rect(x, y, const.TILE_WIDTH, const.TILE_HEIGHT)
                MOVEMENT_IMAGES[id][direction].append(MOVEMENT_SHEET.subsurface(rect))


    FRIGHTENED_SHEET = pygame.image.load('assets/images/enemy/to_eat.jpeg')
    FRIGHTENED_IMAGES = []

    for i in range(2):
        rect = pygame.Rect( i * const.TILE_WIDTH, 0, const.TILE_WIDTH, const.TILE_HEIGHT)
        FRIGHTENED_IMAGES.append(FRIGHTENED_SHEET.subsurface(rect))


    FRIGHTENED_FLASH_SHEET = pygame.image.load('assets/images/enemy/to_eat_flash.jpeg')
    FRIGHTENED_IMAGES_FLASH = []

    for i in range(2):
        rect = pygame.Rect( i * const.TILE_WIDTH, 0, const.TILE_WIDTH, const.TILE_HEIGHT)
        FRIGHTENED_IMAGES_FLASH.append(FRIGHTENED_FLASH_SHEET.subsurface(rect))

    mode_timer = pygame.time.get_ticks()
    frightened_timer = 0
    enemies = []

    def __init__(self, game, start_position, id):
        super().__init__()

        self.game = game
        self.grid = game.grid
        self.id = id

        self.current_image = self.image = Enemy.MOVEMENT_IMAGES[id]['right'][0]
        self.rect = self.image.get_rect()

        self.speed = 120
        self.behaviour = ("CHASE", "SCATTER", "FRIGHTENED")
        self.mode = "SCATTER"

        self.flash_frightened = False
        self.in_tunnel = False
        self.in_pen = True
        self.release_idx = 0
        self.released = False
        self.stopped = False
        self.eaten = False
     
        r, c = start_position
        self.array_pos = (r, c+1)
        self.default_position = (14, 14)
        self.velocity = Vector2(0, 0)

        self.i = 0
        self.release_positions = [] 
        self.direction = "up"

        self.timer_event = 0

        self.id_to_name = {0: "BLINKY",
                           1: "PINKY",
                           2: "INKY",
                           3: "CLYDE",
                           4: "DEADERS"}
        
        Enemy.enemies.append(self)

    def __str__(self):
        return f"{self.name}, released: {self.released}"

    @property
    def name(self):
        return self.id_to_name[self.id] 

    @property
    def array_pos(self):
        return self.grid.get_array_position(self.rect.center)
   
    @array_pos.setter
    def array_pos(self, position):
        self.rect.topleft =  self.grid.get_screen_position(position)

    @property
    def screen_pos(self):
        return self.rect.topleft

    @property
    def center_position(self):
        return self.rect.x - (const.TILE_WIDTH/2), self.rect.y + (const.TILE_HEIGHT/2)
    

    def set_mode(self, mode):
        if mode == "FRIGHTENED":
            Enemy.frightened_timer = pygame.time.get_ticks()
            self.speed = 60
        elif not self.eaten:
            self.speed = 120

        if self.name == "CYLDE":
            if mode == "CHASE":
                self.mode = "SCATTER"
            elif mode == "SCATTER":
                self.mode = "CHASE"
        else:
            self.mode = mode


    def set_new_scatter_position(self):      
        new_position = random.choice(self.scatter_positions)
                        
        while new_position == self.scatter_position:
            new_position = random.choice(self.scatter_positions)
        
        self.scatter_position = new_position
    
    def set_directional_velocity(self, target):
        # Calculate the direction to move towards the target
        dr = target[0] - self.array_pos[0]
        dc = target[1] - self.array_pos[1]
        
        match (dr, dc):
            case (-1, 0):
                self.direction = "up"
                self.velocity = pygame.Vector2(0, -self.speed)
            case (1, 0):
                self.direction = "down"
                self.velocity = pygame.Vector2(0, self.speed)
            case (0, -1):
                self.direction = "left"
                self.velocity = pygame.Vector2(-self.speed, 0)
            case (0, 1):
                self.direction = "right"
                self.velocity = pygame.Vector2(self.speed, 0)


    def get_target(self):
        if self.in_pen:
            if self.array_pos == self.release_position:
                self.in_pen = False
                
            return self.release_position

        if self.eaten:
            return self.default_position

        match self.get_mode():
            case "CHASE":
                return self.calculate_chase_target()
            
            case "SCATTER":
                if isinstance(self, Clyde):
                    self.scatter_position = self.game.player.array_pos
                    return self.scatter_position
    
                if self.array_pos == self.scatter_position:
                    self.set_new_scatter_position()
                return self.scatter_position
            
            case "FRIGHTENED":
                return self.game.player.opposite_grid_position
                
    def get_mode(self):
        center_x, center_y = self.center_position
        distance = sqrt((self.game.player.rect.centerx - center_x)**2 + (self.game.player.rect.centery - center_y)**2)

        # Check if the object is within the circle
        if distance <= Enemy.CIRCLE_RADIUS:
            return "CHASE"
        else:
            return self.mode
    
    

    
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

    def check_frightened(self):
        
        if self.mode == "FRIGHTENED":
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - Enemy.frightened_timer
          
            if elapsed_time > 6000:
                for enemy in Enemy.enemies:
                    if not enemy.eaten:
                        enemy.speed = 120
                        enemy.mode = "CHASE"
                        enemy.flash_frightened = False
                    
            elif elapsed_time > 4000:
                self.flash_frightened = True
        else:
            pass
            
    def check_mode_switch(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - Enemy.mode_timer
        
        
        if self.mode == "SCATTER" and elapsed_time > 5000:
            self.set_mode("CHASE")
            Enemy.mode_timer = pygame.time.get_ticks()

        elif self.mode == "CHASE" and elapsed_time > 3000:
            self.set_mode("SCATTER")
            Enemy.mode_timer = pygame.time.get_ticks()
        

    def check_eaten(self):

        states = [enemy.eaten for enemy in Enemy.enemies]
        print(states)
            

        if self.eaten and self.array_pos == self.default_position:
            self.in_pen = True
            self.eaten = False
            self.speed = 120
            self.mode = "SCATTER"

    """
    DEFAULT FUNCTIONS FOR PYGAME OBJECT
    """
    def handle_event(self, _):
        pass

    def update(self, dt): 
            if self.released and not self.stopped:
                self.check_traveling_through_passage()
                self.check_mode_switch()
                self.check_frightened()
                self.check_eaten()

                self.path = self.astar()

                if self.path and len(self.path) >= 2:
                    if (self.screen_pos == self.grid.get_screen_position(self.path[0])):
                        self.set_directional_velocity(self.path[1])
                    else:
                        self.set_directional_velocity(self.path[0])

                displacement = self.velocity * dt
                collision = self.check_edge_collision(displacement)
            
                if collision:
                    self.array_pos = self.array_pos
                else:
                    self.rect.move_ip(displacement)

    def draw(self, screen):
        if not self.stopped:
            if self.game.frame < 10: 
                current_frame = 0
            elif self.game.frame < 20:
                current_frame = 1
            else:
                current_frame = 0
                self.game.frame = 0
            
            x, y = self.grid.get_screen_position(self.array_pos)

            if self.eaten:
               self.current_image = Enemy.MOVEMENT_IMAGES[4][self.direction][current_frame]
            
            elif self.mode == "FRIGHTENED":
                if self.flash_frightened:
                    self.current_image = (Enemy.FRIGHTENED_IMAGES_FLASH[current_frame], Enemy.FRIGHTENED_IMAGES[current_frame])[current_frame]
                else:
                    self.current_image = Enemy.FRIGHTENED_IMAGES[current_frame]
            else:
                self.current_image = Enemy.MOVEMENT_IMAGES[self.id][self.direction][current_frame]
            

            screen.blit(self.current_image, (self.rect.x - const.TILE_WIDTH, self.rect.y))
            #pygame.draw.circle(screen, colours.WHITE, self.center_position, Enemy.CIRCLE_RADIUS, 2)


    """
    PATHFINDING
    """
    def astar(self):

        def heuristic(self, node, goal):
            if goal is None:
                return 0  # or some other default value
            return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

        start = self.array_pos
        goal = self.get_target()
        open_set = [(0, start)]
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(self, start, goal)}

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == goal:
               path = self.reconstruct_path(came_from, goal)

                   
               return path

            closed_set.add(current)

            for neighbor in self.get_valid_neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1  # Assuming uniform movement cost

                if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                    heapq.heappush(open_set, (tentative_g_score + heuristic(self, neighbor, goal), neighbor))
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(self, neighbor, goal)

        return None  # If the goal is not reachable

    def reconstruct_path(self, came_from, current):
        total_path = []
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def get_valid_neighbors(self, node):
        x, y = node
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(r, c) for (r, c) in neighbors if self.grid.in_borders((r,c)) and self.grid.in_bounds((r, c))]



class Blinky(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_position = (8, 16)
        self.scatter_positions = [(1, 16), (1, 27), (8, 27), (8, 16), (5, 22)]
        self.scatter_position = random.choice(self.scatter_positions)

    def calculate_chase_target(self):
        return self.game.player.array_pos
      
class Pinky(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_position = (8, 13)
        self.scatter_positions = [(1, 2), (1, 13), (8, 13), (8, 2), (5, 7)]
        self.scatter_position = random.choice(self.scatter_positions)

    def calculate_chase_target(self):
        pacman = self.game.player
        pr, pc = pacman.array_pos

        match pacman.direction:
            case "up":
                target = (max(0, pr - 4), pc)
            case "down":
                target = (min(const.ROWS - 1, pr + 4), pc)
            case "left":
                target = (pr, max(0, pc - 4))
            case "right":
                target = (pr, min(const.COLUMNS - 1, pc + 4))
            case _:
                target = (pc, pc)
        return target
        
class Inky(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_position = (14, 19)
        self.scatter_positions = [(20, 16), (20, 27), (29, 27), (29, 16), (23, 22)]
        self.scatter_position = random.choice(self.scatter_positions)
        #self.default_position = (15, 16)
    
    def calculate_chase_target(self):
        pacman = self.game.player
        pr, pc = pacman.array_pos
        target = (pr, pc)

        match pacman.direction:
            case "up":
                target = (pr, pc - 2)
            case "down":
                target = (pr,  pc + 2)
            case "left":
                target = (pr - 2, pc)
            case "right":
                target = (pr + 2, pc)

        if self.array_pos == target:
            return pacman.array_pos
        return target

class Clyde(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_position = (11, 12)
        self.scatter_positions =  [(20, 2), (20, 13), (29, 13), (29, 2), (24, 7)]
        self.scatter_position = random.choice(self.scatter_positions)

    
    def calculate_chase_target(self):
        if self.array_pos == self.scatter_position:
            self.set_new_scatter_position()
        return self.scatter_position
    
