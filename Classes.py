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


    def getweight(self, gravity_force_m_s2):
        self.weight = self.mass * gravity_force_m_s2 

    def updaterect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def create_sprite(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class physics_obj(object):
    def __init__(self, mass, x, y, width, height, color, gravity_force_m_s2=9.81):
        super().__init__(x, y, width, height, color, mass)
        self.initial_velocity_x = 0
        self.initial_velocity_y = 0
        self.velocity_x = self.initial_velocity_x
        self.velocity_y = self.initial_velocity_y
        self.collided = False
        self.previousy = self.y
        self.distancetravelled = 0
        self.onground = False
        self.initial_x = self.x
        self.initial_y = self.y
        self.initial_velocity_y_set = False
        self.initial_velocity_x_set = False
        self.old_rect = self.rect
        self.gravity_force = gravity_force_m_s2

    def apply_velocity_x(self):
        if self.initial_velocity_x_set is not True:
            self.velocity_x = self.initial_velocity_x
            self.initial_velocity_x_set = True
        self.x += self.velocity_x
        self.updaterect()

    def collision_detection(self, other_obj):
        if self is other_obj:
            return False
        
        if self.rect.colliderect(other_obj.rect):
            if isinstance(other_obj, static_obj):
                if self.rect.bottom >= other_obj.rect.top and self.old_rect.bottom < other_obj.rect.top:
                    self.onground = True
                elif self.rect.left <= other_obj.rect.right and self.old_rect.left > other_obj.rect.right:
                    print("HIT LEFT")
                if self.rect.right >= other_obj.rect.left and self.old_rect.right < other_obj.rect.left:
                    print("HIT RIGHT")
                elif self.rect.top <= other_obj.rect.bottom and self.old_rect.top > other_obj.rect.bottom:
                    print("HIT TOP")
            pass
        pass

    def getdistancey(self):
        self.distancetravelled = self.y - self.previousy
        self.previousy = self.y

    def apply_velocity_y(self, seconds):
        self.old_rect = self.rect.copy()
        if self.initial_velocity_y_set is not True:
            self.velocity_y = -self.initial_velocity_y
            self.initial_velocity_y_set = True
        if not self.onground:
            self.velocity_y += (self.gravity_force * pxpermeter) * seconds
            self.y += self.velocity_y * seconds
            self.updaterect()

    def momentumloss():
        pass

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.updaterect()
        self.onground = False
        self.initial_velocity_x_set = False
        self.initial_velocity_y_set = False
        self.velocity_x = self.initial_velocity_x
        self.velocity_y = self.initial_velocity_y
        pass

class static_obj(object):
     def __init__(self, mass, x, y, width, height, color):
        super().__init__(x, y, width, height, color, mass)