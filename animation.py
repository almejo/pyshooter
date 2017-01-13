import gutils
import pygame
from pygame.locals import *

engine = None


def init_animations():
    global engine
    engine = AnimationEngine('engine.txt')


class AnimationEngine:
    def __init__(self, filename):
        self.images = {}
        animation_file = open(filename, 'r')
        lines = animation_file.readlines()
        for line in lines:
            if line[0] == '#':
                continue
            params = line.split(' ')
            print params
            frames = int(params[1])
            images = []
            for i in range(0, frames):
                image, rect = gutils.load_image(params[2].rstrip() + "_" + str(i) + ".png", True)
                images.append(image)

            self.images[params[0]] = (images, rect)

    def get_images(self, name):
        return self.images[name]


class Animation:
    def __init__(self, name, steps=1):
        global engine
        self.frame = 0
        self.counter = 0
        self.steps = steps
        self.images, self.rect = engine.get_images(name)
        self.total_frames = len(self.images)

    def get_rect(self):
        return Rect(self.rect)

    def animate(self):
        image = self.images[self.frame]
        if self.counter % self.steps == 0:
            self.frame += 1
        self.counter += 1
        if self.frame == self.total_frames:
            self.frame = 0
        return image


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 7):
            self.image, self.rect = gutils.load_image("explosion" + str(i) + ".png", True)
            self.images.append(self.image)
        self.frame = 0
        self.counter = 0
        self.rect.center = center

    def update(self):
        self.rect.move_ip(0, 1)
        self.image = self.images[self.frame]
        self.counter += 1
        if self.counter % 10 == 0:
            self.frame += 1
            if self.frame == len(self.images): self.kill()
            return


def main():
    pygame.init()
    pygame.display.set_mode((800, 600), HWSURFACE | DOUBLEBUF)
    init_animations()


if __name__ == '__main__': main()
