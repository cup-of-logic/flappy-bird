import pygame
import numpy as np
import random


class Bird:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Pole:
    def __init__(self):
        self.coord_up = []
        self.coord_down = []
        self.width = 200
        self.height = 400

    def create(self, x, y):
        self.coord_up.append([x, y])
        self.coord_down.append([x, y+self.height+150])


class FlappyBirdGame:
    def __init__(self):
        pygame.init()

        self.bird = Bird(x=200, y=200, width=50, height=50)
        self.pole = Pole()

        self.WIDTH, self.HEIGHT = 500, 500
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Flappy Bird Game")

        self.POLE_WIDTH, self.POLE_HEIGHT = 70, 400
        self.BG_IMG = pygame.image.load('bg.png')
        self.BIRD_IMG = pygame.transform.scale(pygame.image.load('bird.png'), (self.bird.width, self.bird.height))
        self.POLE_UP_IMG = pygame.transform.scale(pygame.image.load('pole_up.png'), (self.POLE_WIDTH, self.POLE_HEIGHT))
        self.POLE_DOWN_IMG = pygame.transform.scale(pygame.image.load('pole_down.png'), (self.POLE_WIDTH, self.POLE_HEIGHT))
        self.FPS = 60
        self.POLE_GAP = 200
        self.JUMP_LIMIT = 60

        self.bird_mask = np.zeros(shape=(self.HEIGHT, self.WIDTH), dtype=bool)
        self.pole_mask = np.zeros(shape=(self.HEIGHT, self.WIDTH), dtype=bool)
        self.start_point = self.bird.y
        self.bird_vel = 3
        self.pole_vel = 1
        self.game_over = False
        self.score = 0

        with open('best.txt', 'r') as file:
            self.best = int(file.read())

        self.pole.create(x=self.WIDTH, y=random.randint(-self.POLE_HEIGHT + 30, -90))
        self.main()

    def collided(self):
        if -7 >= self.bird.y or self.bird.y >= self.HEIGHT-self.bird.height+7:
            return True

        for i in range(len(self.pole.coord_up)):
            if self.bird.x == self.pole.coord_up[i][0]:
                self.score += 1
            if (self.bird.x+7 < self.pole.coord_up[i][0] + self.POLE_WIDTH
                    and self.bird.x-7 + self.bird.width > self.pole.coord_up[i][0] and (
                    self.bird.y+7 < self.pole.coord_up[i][1] + self.POLE_HEIGHT
                    or self.bird.y-7 + self.bird.height > self.pole.coord_down[i][1])):
                return True

        return False

    def add_text(self, text, size, color, x, y):
        font = pygame.font.SysFont(None, size)
        screen_text = font.render(text, True, color)
        self.window.blit(screen_text, [x, y])

    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(self.FPS)

            if self.best < self.score // 4 * 5:
                self.best = self.score // 4 * 5
                with open("best.txt", 'w') as file:
                    file.write(str(self.best))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_point = self.bird.y
                        self.bird_vel = -5

            if self.start_point - self.bird.y >= self.JUMP_LIMIT:
                self.bird_vel = 3

            for i in range(abs(self.bird_vel)):
                if self.collided():
                    self.pole_vel = 0
                    self.bird_vel = 0
                    self.game_over = True
                    break
                self.bird.y += self.bird_vel/abs(self.bird_vel)

            for i in range(len(self.pole.coord_up)):
                if self.bird.x == self.pole.coord_up[i][0]:
                    self.score += 1

            # Creating a pole
            if self.pole.coord_up[-1][0] <= self.WIDTH - self.POLE_GAP:
                self.pole.create(x=self.WIDTH, y=random.randint(-self.POLE_HEIGHT + 30, -90))

            self.window.blit(self.BG_IMG, (-10, -300))

            if not self.game_over:
                i = 0
                while i < len(self.pole.coord_up):
                    if self.pole.coord_up[i][0] < 0 - self.POLE_WIDTH:
                        self.pole.coord_up.pop(i)
                        self.pole.coord_down.pop(i)
                    else:
                        self.window.blit(self.POLE_UP_IMG, (self.pole.coord_up[i][0], self.pole.coord_up[i][1]))
                        self.window.blit(self.POLE_DOWN_IMG, (self.pole.coord_down[i][0], self.pole.coord_down[i][1]))
                        self.pole.coord_up[i][0] -= self.pole_vel
                        self.pole.coord_down[i][0] -= self.pole_vel
                        i += 1

                self.window.blit(self.BIRD_IMG, (self.bird.x, self.bird.y))
                self.add_text(text=f"Score: {(self.score // 4) * 5}", size=30, color=(0, 0, 0), x=10, y=10)
                self.add_text(text=f"Best: {self.best}", size=30, color=(0, 0, 0), x=400, y=10)
            else:
                self.add_text(text="GAME OVER!", size=100, color=(255, 0, 0), x=30, y=200)
                self.add_text(text=f"SCORE: {(self.score // 4) * 5}", size=50, color=(255, 0, 0), x=160, y=260)
                self.add_text(text=f"BEST: {self.best}", size=50, color=(255, 0, 0), x=170, y=300)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    FlappyBirdGame()
