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
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

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
        self.old_rect = self.rect.copy()
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
                overlap_left = self.rect.right - other_obj.rect.left
                overlap_right = other_obj.rect.right - self.rect.left
                overlap_top = self.rect.bottom - other_obj.rect.top
                overlap_bottom = other_obj.rect.bottom - self.rect.top

                if self.old_rect.bottom <= other_obj.rect.top and overlap_top > 0:
                    self.y = other_obj.rect.top - self.height
                    self.updaterect()
                    self.onground = True
                    if isinstance(other_obj, static_obj) and self.velocity_x == 0:
                        v = 0
                        self.velocity_y = -(((self.mass * self.velocity_y)+(other_obj.mass * v))/(self.mass + other_obj.mass))
                    return

                elif self.old_rect.top >= other_obj.rect.bottom and overlap_bottom > 0:
                    self.y = other_obj.rect.bottom
                    self.updaterect()
                    self.velocity_y = -self.velocity_y * 0.5
                    print("HIT TOP")
                    return
                
                elif self.old_rect.right <= other_obj.rect.left and overlap_left > 0:
                    self.x = other_obj.rect.left - self.width
                    self.updaterect()
                    self.velocity_x = -self.velocity_x * 0.5
                    print("HIT LEFT")
                    return

                elif self.old_rect.left >= other_obj.rect.right and overlap_right > 0:
                    self.x = other_obj.rect.right
                    self.updaterect()
                    self.velocity_x = -self.velocity_x * 0.5
                    print("HIT RIGHT")
                    return
            
            if self.onground and self.rect.bottom > other_obj.rect.top and self.rect.top < other_obj.rect.bottom:
                self.y = other_obj.rect.top - self.height
                self.updaterect()
                self.velocity_y = 0
                return
        else:
            pass

    def getdistancey(self):
        self.distancetravelled = self.y - self.previousy
        self.previousy = self.y

    def apply_velocity_y(self, seconds):
        if self.initial_velocity_y_set is not True:
            self.velocity_y = -self.initial_velocity_y
            self.initial_velocity_y_set = True
        
        if self.velocity_y != 0:
            self.onground = False

        if not self.onground:
            self.velocity_y += (self.gravity_force * pxpermeter) * seconds
            self.y += self.velocity_y * seconds
            self.updaterect()

    def reset(self):
        self.onground = False
        self.initial_velocity_x_set = False
        self.initial_velocity_y_set = False
        self.velocity_x = self.initial_velocity_x
        self.velocity_y = self.initial_velocity_y
        self.x = self.initial_x
        self.y = self.initial_y
        self.updaterect()
        self.old_rect = self.rect.copy()
        pass

class static_obj(object):
     def __init__(self, mass, x, y, width, height, color):
        super().__init__(x, y, width, height, color, mass)