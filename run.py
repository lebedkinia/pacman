import pygame
import time
from Ghost import Blinky, Pinky, Inky, Klyde
from Pacman import Pacman
import math

square, radius = 20, 7
width, height = 28 * square, 36 * square
fps = 60

with open("map.txt", "r") as inp:
    map_data = [list(map(int, y.rstrip().split())) for y in inp.readlines()]


class RoundedWall:
    def __init__(self, map_data, cell_size=square):
        self.map_data = map_data
        self.rows = len(map_data)
        self.cols = len(map_data[0])

    def is_wall(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and self.map_data[y][x] == 1

    def draw_wall_segment(self, screen, x, y, form):
        cx, cy = x * square, y * square
        size = square
        line_size = square
        color_blue = (0, 0, 255)
        color_black = (0, 0, 0)
        color_red = (255, 0, 0)

        if form == "inner_bottom_left":
            pass
            pygame.draw.arc(screen, color_blue, (cx - size // 2 - 2, cy - size // 2 - 1, size + 4, size + 3), math.radians(270), math.radians(360), 4)
        elif form == "inner_bottom_right":
            pass
            pygame.draw.arc(screen, color_blue, (cx + size // 2 - 4, cy - size // 2 - 4, size + 7, size + 7), math.radians(180), math.radians(270), 6)
        elif form == "inner_top_left":
            pass
            rct = (cx - size // 2 -4, cy + size // 2 - 4, size + 6, size + 6)
            pygame.draw.arc(screen, color_blue, rct, 0, math.radians(90), 6)
        elif form == "inner_top_right":
            pass
            pygame.draw.arc(screen, color_blue, (cx + size // 2 - 4, cy + size // 2 - 4, size + 7, size + 7), math.radians(90), math.radians(180), 6)
            
        elif form == "vertical":
            pygame.draw.rect(screen, color_blue, (cx + size // 3, cy, size // 3, size))
        elif form == "horizontal":
            pygame.draw.rect(screen, color_blue, (cx, cy + size // 3, size, size // 3))

    def determine_wall_form(self, x, y):
        """
        Определение формы стены на основе соседей.
        :param x: Координата x.
        :param y: Координата y.
        :return: Строка, описывающая форму стены.w
        """
        neighbors = {
            "top": self.is_wall(x, y - 1),
            "bottom": self.is_wall(x, y + 1),
            "left": self.is_wall(x - 1, y),
            "right": self.is_wall(x + 1, y),
            "top_right": self.is_wall(x + 1, y + 1),
            "top_left": self.is_wall(x - 1, y + 1),
            "bottom_right": self.is_wall(x + 1, y - 1),
            "bottom_left": self.is_wall(x - 1, y - 1),
        }

        # вертикальных и горизонтальных стен

        # внутренних углов
        if not neighbors["top"] and neighbors["bottom"] and not neighbors["left"] and neighbors["right"]:
            return "inner_top_right"
        elif not neighbors["top"] and neighbors["bottom"] and neighbors["left"] and not neighbors["right"]:
            return "inner_top_left"
        elif neighbors["top"] and not neighbors["bottom"] and not neighbors["left"] and neighbors["right"]:
            return "inner_bottom_right"
        elif neighbors["top"] and not neighbors["bottom"] and neighbors["left"] and not neighbors["right"]:
            return "inner_bottom_left"
        elif neighbors["top"] and neighbors["top_left"] and neighbors["left"] and neighbors["bottom_left"] and \
                neighbors["bottom"] and neighbors["bottom_right"] and neighbors["right"] and not neighbors["top_right"]:
            return "inner_top_right"
        elif neighbors["top"] and neighbors["top_left"] and neighbors["left"] and not neighbors["bottom_left"] and \
                neighbors["bottom"] and neighbors["bottom_right"] and neighbors["right"] and neighbors["top_right"]:
            return "inner_bottom_left"
        elif neighbors["top"] and neighbors["top_left"] and neighbors["left"] and neighbors["bottom_left"] and \
                neighbors["bottom"] and not neighbors["bottom_right"] and neighbors["right"] and neighbors["top_right"]:
            return "inner_bottom_right"
        elif neighbors["top"] and not neighbors["top_left"] and neighbors["left"] and neighbors["bottom_left"] and \
                neighbors["bottom"] and neighbors["bottom_right"] and neighbors["right"] and neighbors["top_right"]:
            return "inner_top_left"

        elif neighbors["top"] and neighbors["bottom"] and not (neighbors["left"] and neighbors["right"]):
            return "vertical"
        elif neighbors["left"] and neighbors["right"] and not (neighbors["top"] and neighbors["bottom"]):
            return "horizontal"
        else:
            return "horizontal"

    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.is_wall(x, y):
                    form = self.determine_wall_form(x, y)
                    self.draw_wall_segment(screen, x, y, form)


def deth_screen(screen, width, height):
    font = pygame.font.SysFont(None, 100)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.fill((0, 0, 0))
    screen.blit(text, (width // 4, height // 5))
    pygame.display.flip()
    time.sleep(2)


def main():
    global width, height, square, radius, map_data, dead, dead_pucman, start_game, menu

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()

    hero = Pacman(14, 27, radius)
    enemies = [Blinky(14, 15), Pinky(14, 16), Inky(14, 17), Klyde(14, 18)]

    wall = RoundedWall(map_data)

    dead = False
    menu = True
    start_game = False

    dead_pucman = [210, 510]
    mode = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        if menu:
            font = pygame.font.SysFont(None, 50)
            new_game_text = font.render("New Game", True, (255, 255, 255))
            new_game_rect = new_game_text.get_rect(center=(width // 2, height // 2 - 50))
            screen.blit(new_game_text, new_game_rect)

            exit_text = font.render("Exit", True, (255, 255, 255))
            exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 50))
            screen.blit(exit_text, exit_rect)

            texture_display = pygame.image.load("start_display.png")
            texture_display = pygame.transform.scale(texture_display, (int(texture_display.get_width() * 0.4),
                                                                      int(texture_display.get_height() * 0.4)))
            screen.blit(texture_display, (width // 2 - texture_display.get_width() // 2, int(height * 0.2) - texture_display.get_height() // 2))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                start_game = True
                menu = False
                dead = False
                with open("map.txt", "r") as inp:
                    map_data = [list(map(int, y.rstrip().split())) for y in inp.readlines()]

            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit(0)

        elif start_game and not dead:
            wall.draw(screen)
            for i in range(36):
                for j in range(28):
                    if map_data[i][j] == 2:
                        pygame.draw.circle(screen, (245, 245, 220), (j * square + square // 2, i * square + square // 2), radius // 2)
                    elif map_data[i][j] == 3:
                        pygame.draw.circle(screen, (245, 245, 220), (j * square + square // 2, i * square + square // 2), radius)

            pygame.draw.rect(screen, (255, 255, 255), (int(12.8 * square), int(15.35 * square), int(square * 2.4), square // 3))

            for enemy in enemies:
                enemy.draw(screen)
                enemy.tick(square, hero.pos_arr, hero.direction)
                if enemy.mode == 1:
                    mode = 1
                else:
                    mode = 0

            hero.draw(screen)
            hero.portal()
            hero.tick(radius, square, mode)
            hero.move()

            if not ((hero.pos_arr[0] == 17 and hero.pos_arr[1] >= 26) or (hero.pos_arr[0] == 17 and hero.pos_arr[1] <= 1)):
                x, y = hero.pos_x // hero.square, hero.pos_y // hero.square
                if map_data[y][x] == 2:
                    map_data[y][x] = 0
                    hero.add_score()
                elif map_data[y][x] == 3:
                    map_data[y][x] = 0
                    mode = 0
                    for enemy in enemies:
                        enemy.fright()

            for enemy in enemies:
                hero_rect = pygame.Rect(hero.pos_x + square // 2, hero.pos_y + square // 2, 1, 1)
                enemy_rect = pygame.Rect(enemy.pos_x, enemy.pos_y, square * 0.9, square * 0.9)
                if hero_rect.colliderect(enemy_rect):
                    if enemy.mode == 1:
                        hero.death('damage')
                        dead = hero.death()
                        enemies = [Blinky(14, 15), Pinky(14, 16), Inky(14, 17), Klyde(14, 18)]
                    else:
                        enemy.death()
                        hero.score += 200
                    pygame.time.delay(500)

            font = pygame.font.SysFont(None, 36)
            score_text = font.render('HIGH SCORE', True, (255, 255, 255))
            screen.blit(score_text, (11 * square, square))
            score_value = font.render(str(hero.score), True, (255, 255, 255))
            screen.blit(score_value, (14 * square, square * 2))

            for i in range(hero.health):
                pygame.draw.arc(screen, (255, 255, 0), (i * square, 2 * square, radius * 2, radius * 2), 3.66519, 9.42478, 2)

            if pygame.display.get_window_size() != (width, height):
                width, height = pygame.display.get_window_size()
                square = min(height // 36, width // 28)
                radius = max(int(square * 0.35), 1)
                hero.resize(square)
                for enemy in enemies:
                    enemy.resize(square)

        elif dead:
            if dead_pucman[0] < dead_pucman[1]:
                dead_pucman[0] += 1.5
                dead_pucman[1] -= 1.5
            deth_screen(screen, width, height)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                dead = False
                menu = True
                dead_pucman = [210, 510]
                hero = Pacman(14, 27, radius)
                enemies = [Blinky(14, 15), Pinky(14, 16), Inky(14, 17), Klyde(14, 18)]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    


if __name__ == "__main__":
    main()

    # def draw_wall_segment(self, screen, x, y, form):
    #     cx, cy = x * square, y * square
    #     size = square
    #     line_size = square
    #     color_blue = (0, 0, 255)
    #     color_black = (0, 0, 0)
    #
    #     if form == "inner_bottom_left":
    #         pygame.draw.arc(screen, color_blue, (cx - size // 2, cy - size // 2, size, size), 0, 90, 3)
    #         pygame.draw.arc(screen, color_black, (cx - size // 2, cy - size // 2, size - line_size // 2, size - line_size // 2), 0, 90, 5)
    #     elif form == "inner_bottom_right":
    #         pygame.draw.arc(screen, color_blue, (cx + size // 2, cy - size // 2, size, size), 90, 180, 3)
    #         pygame.draw.arc(screen, color_black, (cx + size // 2, cy - size // 2, size - line_size // 2, size - line_size // 2), 90, 180, 5)
    #     elif form == "inner_top_left":
    #         pygame.draw.arc(screen, color_blue, (cx - size // 2, cy + size // 2, size, size), 270, 360, 3)
    #         pygame.draw.arc(screen, color_black, (cx - size // 2, cy + size // 2, size - line_size // 2, size - line_size // 2), 270, 360, 5)
    #     elif form == "inner_top_right":
    #         pygame.draw.arc(screen, color_blue, (cx + size // 2, cy + size // 2, size, size), 180, 270, 3)
    #         pygame.draw.arc(screen, color_black, (cx + size // 2, cy + size // 2, size - line_size // 2, size - line_size // 2), 180, 270, 5)
    #     elif form == "vertical":
    #         pygame.draw.rect(screen, color_blue, (cx + size // 3, cy, size // 3, size))
    #     elif form == "horizontal":
    #         pygame.draw.rect(screen, color_blue, (cx, cy + size // 3, size, size // 3))
