import pygame
import random
import A_star

# Загрузка карты
with open("map_for_ghost.txt", "r") as inp:
    map_data = [list(map(int, y.rstrip().split())) for y in inp.readlines()]

speed = 16


class Ghost:
    square = 20
    param_animation = 0

    def __init__(self, x, y):
        self.patrol_active = False
        self.way = map_data
        self.death_cooldown = 0
        self.mode_cooldown = 0
        self.life = 1
        self.mode = 1
        self.texture = pygame.image.load("Ghost_sprites/Blinky/red_right.png")
        self.pos_arr = [y, x]
        self.pos_x = x * self.square - 10
        self.pos_y = y * self.square - 10
        self.direction = ["none", 0, True]
        self.crossroad = [False, 0]
        self.direc = (['Up', -self.square / 16, False], ['Down', self.square / 16, False],
                      ['Left', -self.square / 16, False], ['Right', self.square / 16, False])

    def tick(self, s, pac, direc_pac):
        self.square = int(s)
        self.crossroad_func()
        self.pos_arr = [(self.pos_y - self.square // 2) // self.square, (self.pos_x - self.square // 2) // self.square]

        if self.mode == 1:
            self.move(pac)
        elif self.mode == 0:
            self.mode_cooldown += 1
            self.move_rand()

        if self.mode_cooldown >= 600:
            self.mode = 1
            self.texture = pygame.image.load("Ghost_sprites/Blinky/red_left.png")
            self.mode_cooldown = 0

        if self.life == 0:
            self.death_cooldown += 1
            self.pos_x = 1 * self.square
            self.pos_y = 1 * self.square

        if self.death_cooldown == 120:
            self.life = 1
            self.pos_x = 14 * self.square - self.square // 2
            self.pos_y = 15 * self.square - self.square // 2
            self.mode = 1
            self.direction = ["none", 0, True]
            self.texture = pygame.image.load("Ghost_sprites/Blinky/red_left.png")
            self.death_cooldown = 0

    def move(self, pac):
        # функция движение
        if (self.pos_x - self.square // 2) % self.square == 0 and \
                (self.pos_y - self.square // 2) % self.square == 0:
            self.way = A_star.main(map_data, (self.pos_arr[0], self.pos_arr[1]), (pac[0], pac[1]))

            if self.way[self.pos_arr[0] + 1][self.pos_arr[1]] == 2:
                self.direction = ['Down', self.square / 16, False]
            elif self.way[self.pos_arr[0] - 1][self.pos_arr[1]] == 2:
                self.direction = ['Up', -self.square / 16, False]
            elif self.way[self.pos_arr[0]][self.pos_arr[1] + 1] == 2:
                self.direction = ['Right', self.square / 16, False]
            elif self.way[self.pos_arr[0]][self.pos_arr[1] - 1] == 2:
                self.direction = ['Left', -self.square / 16, False]

        if self.direction[0] == 'Up' or self.direction[0] == 'Down':
            # коллизая со стенами
            if map_data[self.pos_arr[0] + 1][self.pos_arr[1]] != 1 and \
                    self.direction[0] == 'Down':
                self.pos_y += int(self.direction[1])
            elif map_data[self.pos_arr[0]][self.pos_arr[1]] != 1 and \
                    self.direction[0] == 'Up':
                self.pos_y += int(self.direction[1])
            else:
                self.direction = ["none", 0, True]
        else:
            if map_data[self.pos_arr[0]][self.pos_arr[1] + 1] != 1 and \
                    self.direction[0] == 'Right':
                self.pos_x += int(self.direction[1])
            elif map_data[self.pos_arr[0]][self.pos_arr[1]] != 1 and \
                    self.direction[0] == 'Left':
                self.pos_x += int(self.direction[1])
            else:
                self.direction = ["none", 0, True]

    def move_rand(self):

        if self.direction[2]:
            self.direction = random.choice(self.direc)

        if self.direction[0] == 'Up' or self.direction[0] == 'Down':

            # коллизая со стенами
            if map_data[(self.pos_y + self.square // 2) // self.square][self.pos_arr[1]] != 1 and \
                    self.direction[0] == 'Down':
                self.pos_y += int(self.direction[1])
                self.direc = (['Down', self.square / 16, False], ['Left', -self.square / 16, False],
                              ['Right', self.square / 16, False])
            elif map_data[(self.pos_y - self.square // 2 - int(self.square * 0.05)) // self.square][
                self.pos_arr[1]] != 1 and \
                    self.direction[0] == 'Up':
                self.pos_y += int(self.direction[1])
                self.direc = (['Up', -self.square / 16, False], ['Left', -self.square / 16, False],
                              ['Right', self.square / 16, False])
            else:
                self.direction = ["none", 0, True]

        else:

            # коллизая со стенами
            if map_data[self.pos_arr[0]][((self.pos_x - self.square // 2) // self.square) + 1] != 1 and \
                    self.direction[0] == 'Right':
                self.pos_x += int(self.direction[1])
                self.direc = (['Up', -self.square / 16, False], ['Down', self.square / 16, False],
                              ['Right', self.square / 16, False])
            elif map_data[self.pos_arr[0]][((self.pos_x + self.square // 2 -
                                             int(self.square * 0.05)) // self.square) - 1] != 1 and \
                    self.direction[0] == 'Left':
                self.pos_x += int(self.direction[1])
                self.direc = (['Up', -self.square / 16, False], ['Down', self.square / 16, False],
                              ['Left', -self.square / 16, False])
            else:
                self.direction = ["none", 0, True]

    def crossroad_func(self):
        #  проверка на перекрёсток
        if (self.pos_x - self.square // 2) % self.square == 0 and (self.pos_y - self.square // 2) % self.square == 0:
            self.crossroad[1] = int(map_data[self.pos_arr[0]][self.pos_arr[1] + 1] != 1) + \
                                int(map_data[self.pos_arr[0]][self.pos_arr[1] - 1] != 1) + \
                                int(map_data[self.pos_arr[0] + 1][self.pos_arr[1]] != 1) + \
                                int(map_data[self.pos_arr[0] - 1][self.pos_arr[1]] != 1)

        if self.crossroad[1] >= 3 and self.crossroad[0]:
            self.crossroad[0] = False
            self.direction = ["none", 0, True]
        elif self.crossroad[1] <= 2:
            self.crossroad[0] = True

    def draw(self, screen):
        if self.life == 1:
            resized_texture = pygame.transform.scale(self.texture, (self.square, self.square))
            screen.blit(resized_texture, (self.pos_x - self.square // 2, self.pos_y - self.square // 2))

    def resize(self, s):
        self.direction = ["none", 0, True]
        self.pos_x = (self.pos_arr[1] + 1) * s - s // 2
        self.pos_y = (self.pos_arr[0] + 1) * s - s // 2

    def fright(self):
        self.mode = 0
        self.texture = pygame.image.load("Ghost_sprites/ghost_fright.png")
        self.direction = ["none", 0, False]

    def death(self):
        self.life = 0
        self.death_cooldown = 0


class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = pygame.image.load("Ghost_sprites/Blinky/red_right.png")


class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = pygame.image.load("Ghost_sprites/Pinky/Pinky_right.png")
    
    def animation(self):
        if self.mode == 1:
            if self.direction[0] == 'Up':
                self.texture = pygame.image.load("Ghost_sprites/Pinky/Pinky_up.png")
                self.texture = pygame.image.load("Ghost_sprites/Pinky/Pinky_up.png")
            elif self.direction[0] == 'Down':
                self.texture = pygame.image.load("Ghost_sprites/Pinky/Pinky_down.png")
            elif self.direction[0] == 'Right':
                self.texture = pygame.image.load("Ghost_sprites/Pinky/Pinky_right.png")
            elif self.direction[0] == 'Left':
                self.texture = pygame.image.load("Ghost_sprites/Pinky/Pinky_left.png")


class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = pygame.image.load("Ghost_sprites/Inky/Inky_right.png")
    
    def animation(self):
        if self.mode == 1:
            if self.direction[0] == 'Up':
                self.texture = pygame.image.load("Ghost_sprites/Inky/Inky_up.png")
            elif self.direction[0] == 'Down':
                self.texture = pygame.image.load("Ghost_sprites/Inky/Inky_down.png")
            elif self.direction[0] == 'Right':
                self.texture = pygame.image.load("Ghost_sprites/Inky/Inky_right.png")
            elif self.direction[0] == 'Left':
                self.texture = pygame.image.load("Ghost_sprites/Inky/Inky_left.png")


class Klyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.texture = pygame.image.load("Ghost_sprites/Klyde/Klyde_right.png")
    
    def animation(self):
        if self.mode == 1:
            if self.direction[0] == 'Up':
                self.texture = pygame.image.load("Ghost_sprites/Klyde/Klyde_up.png")
            elif self.direction[0] == 'Down':
                self.texture = pygame.image.load("Ghost_sprites/Klyde/Klyde_down.png")
            elif self.direction[0] == 'Right':
                self.texture = pygame.image.load("Ghost_sprites/Klyde/Klyde_right.png")
            elif self.direction[0] == 'Left':
                self.texture = pygame.image.load("Ghost_sprites/Klyde/Klyde_left.png")