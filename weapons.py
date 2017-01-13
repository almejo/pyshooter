import pygame

import animation
import constants


class EnemyShoot(pygame.sprite.Sprite):
    image = None

    def __init__(self, center, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.animation = animation.Animation('shoot_normal')
        self.image = self.animation.animate()
        self.rect = self.animation.get_rect()
        self.rect.center = center
        self.velocity = velocity

    def update(self):
        if self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT or self.rect.left < 0 or self.rect.right > constants.SCREEN_WIDTH:
            self.kill()
            return

        self.rect.move_ip(self.velocity[0], self.velocity[1])


class Shoot(pygame.sprite.Sprite):
    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)
        self.animation = animation.Animation('shoot_normal')
        self.image = self.animation.animate()
        self.rect = self.animation.get_rect()
        self.rect.center = point

    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        else:
            self.rect.move_ip(0, -8)


class Missiles:
    def __init__(self, owner):
        self.counter = 10
        self.owner = owner

    def do_shoot(self, group):
        group.add(MissileSprite(self.owner.rect.midtop, 1))
        group.add(MissileSprite(self.owner.rect.midtop, -1))
        self.counter -= 1
        if self.counter == 0:
            return False
        return True

    def get_bullets(self):
        return self.counter


class MissileSprite(pygame.sprite.Sprite):
    def __init__(self, center, side):
        pygame.sprite.Sprite.__init__(self)
        self.animation = animation.Animation('shoot_missile', 20)
        self.image = self.animation.animate()
        self.rect = self.animation.get_rect()
        self.rect.center = center
        self.velocity_x = 1 * side
        self.velocity_y = -3
        self.counter = 0

    def update(self):
        self.anim = self.animation.animate()
        self.rect.move_ip(self.velocity_x, self.velocity_y)
        if self.rect.bottom < 0: self.kill()
        if self.counter > 30: self.velocity_x = 0
        self.counter += 1
