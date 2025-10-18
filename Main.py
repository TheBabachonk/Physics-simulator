import pygame
import pygame_gui
import random
import math
from Constants import pxpermeter, screen_largeur, screen_longueur, running
from Window import mass_input, width_input, createwindow
from Classes import physics_obj, static_obj

from pygame_gui.elements import UITextEntryLine


pygame.init()
screen = pygame.display.set_mode((screen_largeur, screen_longueur))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((screen_largeur, screen_longueur))
ui_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2, -1), (200,screen_longueur + 50)), manager=manager, container=None)
physics_obj_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 0), (150, 50)), text="Spawn Physic Object", manager=manager, container=ui_panel)
static_obj_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 100), (150,50)), text="Sapwn Static Object", manager=manager, container=ui_panel)
force_g = 9.81 * pxpermeter
gravity_input = UITextEntryLine(relative_rect=(pygame.Rect((20, 330), (150, 30))), manager=manager,container=ui_panel)
objs = []
ground = None
new_force_g = 0
gravity_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20,300), (150, 30)), manager=manager, container=ui_panel, text=f"Gravity ({force_g/pxpermeter:.2f} m/s²)")
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 400), (50, 50)), manager=manager, container=ui_panel, text="Start")
restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 400), (75, 50)), manager=manager, container=ui_panel, text="Restart")
simulation_started = False

def createphysicsobject():
    rect_width = 30
    rect_height = 30
    rect_x = random.randint(250, 900)
    rect_y = random.randint(100, 300)
    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 225))


    obj = physics_obj(50, rect_x, rect_y, rect_width, rect_height, c)
    objs.append(obj)
    pass

def createstaticobject():
    rect_width = 30
    rect_height = 30
    rect_x = random.randint(250, 900)
    rect_y = random.randint(100, 300)
    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 225))


    obj = static_obj(50, rect_x, rect_y, rect_width, rect_height, c)
    objs.append(obj)

def createground():
    rect_width = 1000
    rect_height = 100
    rect_x = 0
    rect_y = 500
    c = (50, 0, 255)

    ground = static_obj(1000, rect_x, rect_y, rect_width, rect_height, c)
    objs.append(ground)


createground()

while running:
    delta = clock.tick(60)
    seconds = delta / 1000.0
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

            if event.ui_element == start_button:
                if active_window is not None:
                    active_window.kill()
                    active_window = None
                simulation_started = True

            if event.ui_element == restart_button:
                simulation_started = False
                for obj in objs:
                    if isinstance(obj, physics_obj):
                        obj.reset()
                pass

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == gravity_input:
                new_force_g = float(gravity_input.text)
                force_g = new_force_g * pxpermeter
                gravity_label.set_text(f"Gravity ({force_g/pxpermeter:.2f} m/s²)")

            if active_window is not None:
                if event.ui_element == mass_input:
                    print("Even likes boys")

                if event.ui_element == width_input:
                    print("kok")
                pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            for obj in objs:
                if obj.rect.collidepoint(event.pos):
                    createwindow(obj, manager)

        manager.process_events(event)

    screen.fill((0,0,0))
    
    for obj in objs:
        obj.create_sprite(screen)
        if isinstance(obj, physics_obj) and simulation_started:
            obj.apply_velocity_y(force_g, seconds)
            obj.getweight(force_g)
            obj.getdistancey()
            for obj2 in objs:
                obj.collision_detection(obj2)
                pass


    manager.update(delta)
    manager.draw_ui(screen)
    pygame.display.flip()