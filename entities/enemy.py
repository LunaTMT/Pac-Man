import pygame
import colours
import const

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, start_position, name):
        super().__init__()

        self.game = game
        self.grid = game.grid
        

        """
           Blinky (red) is very aggressive and hard to shake once he gets behind you, 
           Pinky  (pink) tends to get in front of you and cut you off, 
           Inky   (light blue) is the least predictable of the bunch, 
           Clyde  (orange) seems to do his own thing and stay out of the way.
        """
        self.name = name


        """
            Scatter Mode: In this mode, the ghosts have specific pre-defined locations on the game board where 
            they aim to go. Each ghost has its own scatter corner where it moves to when the game is in scatter mode. 
            This behavior is generally used to create patterns in the ghost's movements and give players a chance to 
            strategize around predictable ghost locations.

            Frightened Mode: When Pac-Man eats a power pellet, the ghosts turn blue and enter frightened mode.
            In this state, the ghosts become vulnerable, and their behavior changes. 
            Instead of chasing Pac-Man, they will try to avoid him and move in a random or less predictable manner.
            Pac-Man can eat the frightened ghosts for extra points during this time.
        """
        self.behaviour = ("CHASE", "SCATTER", "FRIGHTENED")


        #Enemy images
        self.movement_sheet = pygame.image.load('assets/images/enemy/enemies.jpeg')  
        self.movement_sheet.set_colorkey(colours.BLACK)
        self.movement_images = {
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
        
        #set sprite rect
        self.image = self.initialise_sprite_images()
        self.rect = self.image.get_rect()
        self.current_image = self.movement_images[name]["right"][0]



        self.array_pos = start_position

    def initialise_sprite_images(self):
            
        frame_width = 15
        frame_height = 15 

        #init images
        for _, direction in enumerate(self.movement_images[self.name]):
            for c in range(2): 
                x = (c * frame_width) 
                y = (self.name * frame_height) 
                rect = pygame.Rect(x, y, frame_width, frame_height)
                self.movement_images[self.name][direction].append(self.movement_sheet.subsurface(rect))
        return self.movement_images[self.name]['right'][0]


    @property
    def array_pos(self):
        return self.grid.get_array_position(self.rect.center)
   
    @array_pos.setter
    def array_pos(self, position):
        self.rect.topleft =  self.grid.get_screen_position(position)




    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.current_image, (self.rect.x - const.TILE_WIDTH, self.rect.y))
