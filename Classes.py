import pygame
from Constants import pxpermeter

class object:
    def __init__(self, x, y, width, height, color, mass):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.mass = mass
        pass

    def getweight(self, force_g):
        self.weight = self.mass * (force_g/pxpermeter)

    def updaterect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def create_sprite(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class physics_obj(object):
    def __init__(self, mass, x, y, width, height, color):
        super().__init__(x, y, width, height, color, mass)
        self.collided = False
        self.previousy = self.y
        self.distancetravelled = 0
        self.velocity_y = 0
        self.onground = False
        self.velocity_x = 1
        self.initial_x = self.x
        self.initial_y = self.y

    def apply_velocity_x(self):
        self.x += self.velocity_x
        self.updaterect()

    def collision_detection(self, other_obj):
        if self is other_obj:
            return False
        
        if self.rect.colliderect(other_obj.rect):
            self.onground = True
            self.getdistancey()
        pass

    def getdistancey(self):
        self.distancetravelled = self.y - self.previousy
        self.previousy = self.y


    def apply_velocity_y(self, force_g, seconds):
        if not self.onground:
            self.velocity_y += force_g * seconds
            self.y += self.velocity_y * seconds
            self.updaterect()

    def momentumloss():
        pass

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.updaterect()
        self.onground = False
        self.velocity_x = 0
        self.velocity_y = 0
        pass

class static_obj(object):
     def __init__(self, mass, x, y, width, height, color):
        super().__init__(x, y, width, height, color, mass)