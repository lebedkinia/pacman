import pygame
import pygame.gfxdraw
import math

with open("map.txt", "r") as inp:
    map_data = [list(map(int, y.rstrip().split())) for y in inp.readlines()]

speed = 16


class Pacman:
    square = 20
    direc_animation = 0

    def __init__(self, x, y, r):
        self.score = 0  # имеющиеся очки
        self.max_score = 0  # максимальное кол-во очков
        self.pos_arr = [y, x]
        self.pos_x = x * self.square  # позиция по x
        self.pos_y = y * self.square - 10  # позиция по y
        self.pos_x_start = x * self.square
        self.pos_y_start = y * self.square - 10
        self.health = 3  # кол-во жизней
        self.mouth = [30, 330]  # угол рта пакмена
        self.rad_pacman = r  # радиус пакмена
        self.crossroad = [False, 0]  # перекрёсток [(есть перекрёсток или нет), (сколько возможных поворотов)]
        self.direction = ["none", 0, True]  # направления движение [куда, скорость, остановлен ли]

    def tick(self, r, s, mode=1):
        global speed

        # проверка нахождения за стенами
        if (self.pos_arr[0] == 17 and self.pos_arr[1] >= 26) or \
                (self.pos_arr[0] == 17 and self.pos_arr[1] <= 1):
            return

        if mode == 0:
            speed = 8
        else:
            speed = 16

        # анимация пакмена
        if not self.direction[2]:
            self.animation()

        self.square = int(s)
        self.rad_pacman = r + r // 1.5
        self.pos_arr = [(self.pos_y - self.square // 2) // self.square, (self.pos_x - self.square // 2) // self.square]
        self.crossroad_func()

        keys = pygame.key.get_pressed()

        # движение пакмена
        if self.direction[0] == 'Up' or self.direction[0] == 'Down':
            if map_data[(self.pos_y + self.square // 2) // self.square][self.pos_arr[1]] != 1 and \
                    self.direction[0] == 'Down':
                self.pos_y += int(self.direction[1])
            elif map_data[(self.pos_y - self.square // 2 - int(self.square * 0.05)) // self.square][
                self.pos_arr[1]] != 1 and \
                    self.direction[0] == 'Up':
                self.pos_y += int(self.direction[1])
            else:
                self.direction = ["none", 0, True]

            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.direction[0] == 'Down':
                self.direction = ['Up', -self.square / speed, False]
                self.mouth = [300, 600]
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.direction[0] == 'Up':
                self.direction = ['Down', self.square / speed, False]
                self.mouth = [120, 420]

            self.turn()

        else:
            if map_data[self.pos_arr[0]][((self.pos_x - self.square // 2) // self.square) + 1] != 1 and \
                    self.direction[0] == 'Right':
                self.pos_x += int(self.direction[1])
            elif map_data[self.pos_arr[0]][
                ((self.pos_x + self.square // 2 - int(self.square * 0.05)) // self.square) - 1] != 1 and \
                    self.direction[0] == 'Left':
                self.pos_x += int(self.direction[1])
            else:
                self.direction = ["none", 0, True]

            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.direction[0] == 'Right':
                self.direction = ['Left', -self.square / speed, False]
                self.mouth = [210, 510]
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.direction[0] == 'Left':
                self.direction = ['Right', self.square / speed, False]
                self.mouth = [30, 330]

            self.turn()

    def move(self):
        keys = pygame.key.get_pressed()

        if self.direction[2]:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction = ['Up', -self.square / speed, False]
                self.mouth = [300, 600]
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction = ['Down', self.square / speed, False]
                self.mouth = [120, 420]
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction = ['Left', -self.square / speed, False]
                self.mouth = [210, 510]
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction = ['Right', self.square / speed, False]
                self.mouth = [30, 330]

    def turn(self):
        # Позволяет поворачивать в движении
        y, x = int(self.pos_y // self.square), int(self.pos_x // self.square)
        if (self.pos_x - self.square // 2) % self.square == 0 and (self.pos_y - self.square // 2) % self.square == 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if map_data[int((self.pos_y + self.square // 2) // self.square)][x] != 1:
                    self.direction = ['Down', self.square / speed, False]
                    self.mouth = [120, 420]
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if map_data[int((self.pos_y - self.square // 2 - int(self.square * 0.05)) // self.square)][x] != 1:
                    self.direction = ['Up', -self.square / speed, False]
                    self.mouth = [300, 600]
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if map_data[y][int((self.pos_x + self.square // 2 - 1) // self.square) - 1] != 1:
                    self.direction = ['Left', -self.square / speed, False]
                    self.mouth = [210, 510]
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if map_data[y][int((self.pos_x - self.square // 2) // self.square) + 1] != 1:
                    self.direction = ['Right', self.square / speed, False]
                    self.mouth = [30, 330]

    def crossroad_func(self):
        if (self.pos_x - self.square // 2) % self.square == 0 and (self.pos_y - self.square // 2) % self.square == 0:
            self.crossroad[1] = int(map_data[self.pos_arr[0]][self.pos_arr[1] + 1] != 1) + \
                                int(map_data[self.pos_arr[0]][self.pos_arr[1] - 1] != 1) + \
                                int(map_data[self.pos_arr[0] + 1][self.pos_arr[1]] != 1) + \
                                int(map_data[self.pos_arr[0] - 1][self.pos_arr[1]] != 1)

    def portal(self):
        # функция портала
        self.pos_arr = [(self.pos_y - self.square // 2) // self.square, (self.pos_x - self.square // 2) // self.square]

        if self.pos_arr[0] == 17 and self.pos_arr[1] >= 26:
            if self.direction[0] == "Right" and self.pos_arr[1] >= 28:
                self.pos_x = - self.square
            elif self.direction[0] == "Right" and 26 <= self.pos_arr[1] < 28:
                self.pos_x += int(self.direction[1])
            elif self.direction[0] == "Left" and self.pos_arr[1] > 25:
                self.pos_x += int(self.direction[1])

        if self.pos_arr[0] == 17 and self.pos_arr[1] <= 1:
            if self.direction[0] == "Right":
                self.pos_x += int(self.direction[1])
            elif self.direction[0] == "Left" and -2 < self.pos_arr[1] <= 1:
                self.pos_x += int(self.direction[1])
            elif self.direction[0] == "Left" and self.pos_arr[1] <= -2:
                self.pos_x = self.square * 28

    def draw(self, screen):
        # Отрисовка пакмена
        start_angle = math.radians(self.mouth[0])
        end_angle = math.radians(self.mouth[1])
        start_angle = math.radians(0)
        end_angle = math.radians(360)
        # print(start_angle, end_angle)
        # pygame.draw.circle(screen, rect=(self.pos_x - self.rad_pacman, self.pos_y - self.rad_pacman, self.rad_pacman * 2, self.rad_pacman * 2), color=(255, 255, 0))
        pygame.draw.circle(screen, (255, 255, 0), (self.pos_x, self.pos_y), 10)
        # pygame.gfxdraw.pie(screen, (self.pos_x + self.rad_pacman) / 2, (self.pos_y + self.rad_pacman) / 2, 75, start_angle, end_angle, (255, 0, 0))

    def resize(self, s):
        # что происходит с пакменом про изменении размера экрана
        self.direction = ["none", 0, True]
        self.pos_x = (self.pos_arr[1] + 1) * s - s // 2
        self.pos_y = (self.pos_arr[0] + 1) * s - s // 2

    def animation(self):
        if self.direction[0] == "Right":
            if self.mouth[0] + abs(self.mouth[1] - 360) == 60:
                self.direc_animation = 1
            elif self.mouth[0] + abs(self.mouth[1] - 360) == 0:
                self.direc_animation = -1
            self.mouth[0] -= self.direc_animation * 2
            self.mouth[1] += self.direc_animation * 2
        elif self.direction[0] == "Left" or self.direction[0] == "Up" or self.direction[0] == "Down":
            if self.mouth[0] - abs(self.mouth[1] - 360) == 60:
                self.direc_animation = 1
            elif self.mouth[0] - abs(self.mouth[1] - 360) == 0:
                self.direc_animation = -1
            self.mouth[0] -= self.direc_animation * 2
            self.mouth[1] += self.direc_animation * 2

    def death(self, d=0):
        if d == 'damage':
            self.health -= 1
            self.pos_x = self.pos_x_start
            self.pos_y = self.pos_y_start
            return False
        if self.health <= 0:
            return True

    def add_score(self):
        self.score += 10
        if self.score == 10000:
            self.health += 1
