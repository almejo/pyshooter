import pygame
import random
from pygame.locals import *

import animation
import constants
import gutils
import weapons


class Nave(pygame.sprite.Sprite):
    laser_fx = gutils.load_sound_file("laser.wav")

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)

        animation.init_animations()
        self.animation = animation.Animation('nave', 10)
        self.image = self.animation.animate()
        self.rect = self.animation.get_rect()

        self.counter = 0
        self.rect.center = center
        self.x_velocity = 0
        self.y_velocity = 0
        self.key_y_buff = []
        self.key_x_buff = []
        self.weapon = weapons.Missiles(self)

    def get_velocity(self):
        if len(self.key_x_buff) > 0:
            x = self.key_x_buff[-1:][0]
        else:
            x = 0
        if len(self.key_y_buff) > 0:
            y = self.key_y_buff[-1:][0]
        else:
            y = 0
        return x, y

    def update(self):
        velocity = self.get_velocity()
        self.rect.move_ip(velocity[0], velocity[1])

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > constants.SCREEN_WIDTH:
            self.rect.right = constants.SCREEN_WIDTH

        self.image = self.animation.animate()

        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.rect.bottom = constants.SCREEN_HEIGHT

    def process_key(self, event, lasers):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if -1 not in self.key_y_buff:
                    self.key_y_buff.append(-4)
            elif event.key == K_DOWN:
                if 1 not in self.key_y_buff:
                    self.key_y_buff.append(4)
            elif event.key == K_RIGHT:
                if 1 not in self.key_x_buff:
                    self.key_x_buff.append(4)
            elif event.key == K_LEFT:
                if -1 not in self.key_x_buff:
                    self.key_x_buff.append(-4)
            elif event.key == K_SPACE:
                Nave.laser_fx.play()
                lasers.add(weapons.Shoot(self.rect.midtop))
            elif event.key == K_x:
                if self.weapon is not None:
                    if not self.weapon.do_shoot(lasers): self.weapon = None
        elif event.type == KEYUP:
            if event.key == K_UP:
                if -4 in self.key_y_buff:
                    self.key_y_buff.remove(-4)
            if event.key == K_DOWN:
                if 4 in self.key_y_buff:
                    self.key_y_buff.remove(4)
            if event.key == K_RIGHT:
                if 4 in self.key_x_buff:
                    self.key_x_buff.remove(4)
            elif event.key == K_LEFT:
                if -4 in self.key_x_buff:
                    self.key_x_buff.remove(-4)

    def get_weapon_bullets(self):
        if self.weapon is not None:
            return self.weapon.get_bullets()
        return 0


class AEnemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.counter = 0
        self.x_velocity = 0
        self.y_velocity = 0
        pass

    def update(self):
        self.step()
        self.rect.move_ip((self.x_velocity, self.y_velocity))
        self.counter += 1


class EnemyRing(AEnemy):
    def __init__(self, center_x):
        AEnemy.__init__(self)
        self.start_time = pygame.time.get_ticks()
        self.x_velocity = 0
        self.y_velocity = 3
        self.animation = animation.Animation('enemy_ring', 20)
        self.image = self.animation.animate()
        self.rect = self.animation.get_rect()
        self.rect.center = (center_x, 0 - self.rect.height)

        self.first = random.randint(50, 150)
        self.second = self.first + random.randint(50, 150)

    def do_shoot(self, group):
        if len(group) < 30 and self.counter % 70 == 0 or self.counter % 90 == 0:
            group.add(weapons.EnemyShoot(self.rect.midtop, (1, 2)))
            group.add(weapons.EnemyShoot(self.rect.midtop, (-1, 2)))

    def step(self):
        if self.first < self.counter < self.second:
            self.y_velocity = 0
        elif self.counter > self.second:
            self.y_velocity = 4

        if self.rect.bottom > constants.SCREEN_HEIGHT:
            self.kill()
        self.image = self.animation.animate()


class Enemy(AEnemy):
    def __init__(self):
        AEnemy.__init__(self)
        self.animation = animation.Animation('enemy_triangle')
        self.image = self.animation.animate()
        self.rect = self.animation.get_rect()

        self.rect.center = (constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 4)
        self.x_velocity = random.randint(-5, 5)
        self.y_velocity = random.randint(-5, 5)

    def step(self):
        if self.rect.left < 0 or self.rect.right > constants.SCREEN_WIDTH - 32: self.x_velocity = -self.x_velocity
        if self.rect.top < 0 or self.rect.bottom >= constants.SCREEN_HEIGHT - 32: self.y_velocity = -self.y_velocity
        if self.x_velocity == 0: self.x_velocity = random.randint(-5, 5)
        if self.y_velocity == 0: self.y_velocity = random.randint(-5, 5)
        self.image = self.animation.animate()

    def do_shoot(self, group):
        if len(group) < 30 and self.counter % 70 == 0 or self.counter % 90 == 0 or self.counter % 110 == 0:
            group.add(weapons.EnemyShoot(self.rect.midtop, (0, 2)))
