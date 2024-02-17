import pygame
import colours
import const
import heapq


class Enemy(pygame.sprite.Sprite):
     # Set the desired speed here

    SPAWN_TIMER = -3000
    MOVEMENT_SHEET = pygame.image.load('assets/images/enemy/enemies.jpeg')
    
    MOVEMENT_IMAGES = {
        0: {'right': [], 'left': [], 'up': [], 'down': []},
        1: {'right': [], 'left': [], 'up': [], 'down': []},
        2: {'right': [], 'left': [], 'up': [], 'down': []},
        3: {'right': [], 'left': [], 'up': [], 'down': []},
        4: {'right': [], 'left': [], 'up': [], 'down': []}}

    for id, directions in MOVEMENT_IMAGES.items():
        for direction in directions:
            for c in range(2):
                x = (c * const.TILE_WIDTH)
                y = (id * const.TILE_HEIGHT)
                rect = pygame.Rect(x, y, const.TILE_WIDTH, const.TILE_HEIGHT)
                MOVEMENT_IMAGES[id][direction].append(MOVEMENT_SHEET.subsurface(rect))


    def __init__(self, game, start_position, id):
        super().__init__()

        self.game = game
        self.grid = game.grid
        self.id = id

        self.current_image = self.image = Enemy.MOVEMENT_IMAGES[id]['right'][0]
        self.rect = self.image.get_rect()

        self.speed = 120
        self.behaviour = ("CHASE", "SCATTER", "FRIGHTENED")
        self.mode = None
        self.in_pen = True
        self.released = False
        self.direction = "right"
        self.array_pos = start_position
        self.velocity = pygame.Vector2(0, 0)
        self.names = {
            0: "Blinky",
            1: "Pinky",
            2: "Cyan",
            3: "Cylde"
        }
        self.release_positions = [] 
        self.direction = None

    def __str__(self):
        return f"{self.names[self.id]}, released: {self.released}"

    @property
    def array_pos(self):
        return self.grid.get_array_position(self.rect.center)

    @array_pos.setter
    def array_pos(self, position):
        self.rect.topleft = self.grid.get_screen_position(position)

    @property
    def screen_pos(self):
        return self.rect.topleft


    def handle_events(self):
        pass


    def update(self, dt):
        if self.released:
            target = self.game.player.array_pos
            path = self.astar(self.array_pos, target)
            
            self.set_directional_velocity(path[1])

            displacement = self.velocity * dt
            collision = self.check_edge_collision(displacement)

            if collision:
                self.array_pos = self.array_pos
            else:
                self.rect.move_ip(displacement)




    def draw(self, screen):
        screen.blit(self.current_image, (self.rect.x - const.TILE_WIDTH, self.rect.y))


    def heuristic(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def astar(self, start, goal):
        open_set = [(0, start)]
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == goal:
               return self.reconstruct_path(came_from, goal)


            closed_set.add(current)

            for neighbor in self.get_valid_neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1  # Assuming uniform movement cost

                if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                    heapq.heappush(open_set, (tentative_g_score + self.heuristic(neighbor, goal), neighbor))
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

        return None  # If the goal is not reachable


    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def get_valid_neighbors(self, node):
        x, y = node
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(r, c) for (r, c) in neighbors if self.grid[r][c] != '#']

    def set_directional_velocity(self, target):
        # Calculate the direction to move towards the target
        dx = target[0] - self.array_pos[0]
        dy = target[1] - self.array_pos[1]

        match (dx, dy):
            case (0, 1):
                self.direction = "up"
                self.velocity = pygame.Vector2(self.speed, 0)
            case (0, -1):
                self.direction = "down"
                self.velocity = pygame.Vector2(-self.speed, 0)
            case (1, 0):
                self.direction = "left"
                self.velocity = pygame.Vector2(0, self.speed)
            case (-1, 0):
                self.direction = "right"
                self.velocity = pygame.Vector2(0, -self.speed)


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


class Blinky(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_positions = [(13, 12), (13, 13), (12, 13), (11, 13)]

class Pinky(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_positions = [(13, 13), (12, 13), (11, 13)]

class Inky(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_positions = [(13, 14), (12, 14), (11, 14)]

class Clyde(Enemy):
    def __init__(self, game, start_position, id):
        super().__init__(game, start_position, id)
        self.release_positions = [(13, 15), (13, 14), (12, 14), (11, 14)]