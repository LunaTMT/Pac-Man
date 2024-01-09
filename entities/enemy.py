import pygame
import colours
import const


class Enemy(pygame.sprite.Sprite):

    SPAWN_TIMER = -3000 #Blinky is released within a second of game starting and following ghosts are every 4s
    MOVEMENT_SHEET = pygame.image.load('assets/images/enemy/enemies.jpeg')  
    MOVEMENT_SHEET.set_colorkey(colours.BLACK)
    MOVEMENT_IMAGES = {
                        0: {'right': [], 'left': [], 'up': [], 'down': []},
                        1: {'right': [], 'left': [], 'up': [], 'down': []},
                        2: {'right': [], 'left': [], 'up': [], 'down': []},
                        3: {'right': [], 'left': [], 'up': [], 'down': []},
                        4: {'right': [], 'left': [], 'up': [], 'down': []}}
    
    """
        NOTE FOR NAME
        light blue = 0
        orange     = 1
        pink       = 2
        red        = 3
        dead       = 4
    """

    #Get all movements sprite sheets from sprites
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

        self.behaviour = ("CHASE", "SCATTER", "FRIGHTENED")
        self.mode = None
        self.in_pen = True
        self.release = False
        self.direction = "right"
        self.array_pos = start_position

        self.names = {0 : "Blinky",
                      1 : "Pinky",
                      2 : "Cyan",
                      3 : "Cylde"}

    def __str__(self):
        return f"{self.names[self.id]}, released : {self.release}"    

    @property
    def array_pos(self):
        return self.grid.get_array_position(self.rect.center)
   
    @array_pos.setter
    def array_pos(self, position):
        self.rect.topleft =  self.grid.get_screen_position(position)

    def handle_events(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.current_image, (self.rect.x - const.TILE_WIDTH, self.rect.y))


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
