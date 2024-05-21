import pygame
import numpy as np
import random


class Bird:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Pole:
    def __init__(self):
        self.coord_up = []
        self.coord_down = []
        self.width = 50
        self.height = 400

    def create(self, x, y):
        self.coord_up.append(pygame.Rect(x, y, self.width, self.height))
        self.coord_down.append(pygame.Rect(x, y + self.height + 150, self.width, self.height))


class FlappyBirdGame:
    def __init__(self):
        pygame.init()

        self.bird = Bird(x=200, y=200, width=50, height=50)
        self.pole = Pole()

        self.WIDTH, self.HEIGHT = 500, 500
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Flappy Bird Game")

        self.POLE_WIDTH, self.POLE_HEIGHT = 100, 400
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

        self.get_mask()
        self.pole.create(x=self.WIDTH, y=random.randint(-self.POLE_HEIGHT + 10, -60))
        self.main()

    def get_mask(self):
        bird_arr = np.asarray(pygame.surfarray.array2d(self.BIRD_IMG), dtype=bool)

        for i in range(len(bird_arr)):
            for j in range(len(bird_arr[0])):
                self.bird_mask[int(j + self.bird.y)][int(i + self.bird.x)] = bird_arr[i][j]

        pole_up_arr = np.asarray(pygame.surfarray.array2d(self.POLE_UP_IMG), dtype=bool)
        pole_down_arr = np.asarray(pygame.surfarray.array2d(self.POLE_DOWN_IMG), dtype=bool)

        for ind in range(len(self.pole.coord_up)):
            if self.WIDTH < self.pole.coord_up[ind].left < 0:
                continue

            for i in range(len(pole_up_arr)):
                for j in range(len(pole_up_arr[0])):
                    if i + self.pole.coord_up[ind].left < self.HEIGHT and j + self.pole.coord_down[ind].top < self.WIDTH:
                        self.pole_mask[int(j + self.pole.coord_up[ind].top)][int(i + self.pole.coord_up[ind].left)] = pole_up_arr[i][j]
                        self.pole_mask[int(j + self.pole.coord_down[ind].top)][int(i + self.pole.coord_down[ind].left)] = pole_down_arr[i][j]

    def collided(self):
        return any(self.bird.rect.colliderect(pole) for pole in self.pole.coord_up + self.pole.coord_down)

    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(self.FPS)

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
                    break
                self.bird.y += self.bird_vel / abs(self.bird_vel)

            # Creating a pole
            if self.pole.coord_up[-1].left <= self.WIDTH - self.POLE_GAP:
                self.pole.create(x=self.WIDTH, y=random.randint(-self.POLE_HEIGHT + 10, -60))

            self.window.blit(self.BG_IMG, (-10, -300))

            i = 0
            while i < len(self.pole.coord_up):
                if self.pole.coord_up[i].left < 0 - self.POLE_WIDTH:
                    self.pole.coord_up.pop(i)
                    self.pole.coord_down.pop(i)
                else:
                    self.window.blit(self.POLE_UP_IMG, (self.pole.coord_up[i].left, self.pole.coord_up[i].top))
                    self.window.blit(self.POLE_DOWN_IMG, (self.pole.coord_down[i].left, self.pole.coord_down[i].top))
                    self.pole.coord_up[i].left -= self.pole_vel
                    self.pole.coord_down[i].left -= self.pole_vel
                    i += 1

            self.window.blit(self.BIRD_IMG, (self.bird.x, self.bird.y))
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    FlappyBirdGame()
