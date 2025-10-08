import pygame
import pygame_gui
import random
import math

pygame.init()

screen_largeur = 1000
screen_longueur = 600
screen = pygame.display.set_mode((screen_largeur, screen_longueur))
clock = pygame.time.Clock()
running = True
manager = pygame_gui.UIManager((screen_largeur, screen_longueur))
ui_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (200,screen_longueur)), manager=manager, container=None)
physics_obj_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 0), (100, 50)), text="button", manager=manager, container=ui_panel)
static_obj_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 100), (100,50)), text="button", manager=manager, container=ui_panel)
force_g = 9.81
objs = []
ground = None


class object:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pass

    def updaterect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def create_sprite(self):
        pygame.draw.rect(screen, self.color, self.rect)

class physics_obj(object):
    def __init__(self, mass, weight, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.mass = mass
        self.weight = weight
        self.collided = False
        self.previousy = self.y
        self.distancetravelled = None
        self.velocity_y = 0
        self.onground = False
        self.initial_speed_y = 10
        self.speed_y = 0
        self.speed_x = 1

    def apply_gravity(self):
        if self.onground == False:
            self.velocity_y = force_g
            self.y += self.velocity_y
            self.updaterect()
        pass

    def apply_velocity_x(self):
        self.x += self.speed_x
        self.updaterect()

    def collision_detection(self, other_obj):
        if self is other_obj:
            return False
        
        if self.rect.colliderect(other_obj.rect):
            print("COLLIDED")
            print(self.y, self.previousy)
            self.onground = True
            self.distancetravelled = self.y - self.previousy
            self.get_velocity_y()
            self.previousy = self.y
        pass


    def get_velocity_y(self):
        self.speed_y = math.sqrt(self.initial_speed_y**2 + 2 * (-force_g) * (-self.distancetravelled))
        print(self.speed_y)

class static_obj(object):
     def __init__(self, mass, weight, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.mass = mass
        self.weight = weight

def createphysicsobject():
    rect_width = 30
    rect_height = 30
    rect_x = random.randint(250, 900)
    rect_y = random.randint(100, 300)
    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 225))


    obj = physics_obj(50, 50, rect_x, rect_y, rect_width, rect_height, c)
    objs.append(obj)
    pass

def createstaticobject():
    rect_width = 30
    rect_height = 30
    rect_x = random.randint(250, 900)
    rect_y = random.randint(100, 500)
    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 225))


    obj = static_obj(50, 50, rect_x, rect_y, rect_width, rect_height, c)
    objs.append(obj)

def createground():
    rect_width = 1000
    rect_height = 100
    rect_x = 0
    rect_y = 500
    c = (50, 0, 255)

    ground = static_obj(1000, 5000, rect_x, rect_y, rect_width, rect_height, c)
    objs.append(ground)


createground()

while running:
    delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == physics_obj_button:
                print("SPAWN PHYSICS OBJECT")
                createphysicsobject()

            if event.ui_element == static_obj_button:
                print("SPAWN STATIC OBJECT")
                createstaticobject()
            pass

        manager.process_events(event)

    screen.fill((0,0,0))
    
    for obj in objs:
        obj.create_sprite()
        if isinstance(obj, physics_obj):
            obj.apply_gravity()
            for obj2 in objs:
                obj.collision_detection(obj2)
                pass

    manager.update(delta)
    manager.draw_ui(screen)
    pygame.display.flip()