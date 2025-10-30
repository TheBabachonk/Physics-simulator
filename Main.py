import pygame
import pygame_gui
import random
import math
from Constants import pxpermeter, screen_largeur, screen_longueur, running
import Window as Window_Manager
from Classes import physics_obj, static_obj

from pygame_gui.elements import UITextEntryLine


pygame.init()

DEFAULT_GRAVITY_M_S2 = 9.81

screen = pygame.display.set_mode((screen_largeur, screen_longueur))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((screen_largeur, screen_longueur))
ui_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2, -1), (200,screen_longueur + 50)), manager=manager, container=None)
physics_obj_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 0), (150, 50)), text="Spawn Physic Object", manager=manager, container=ui_panel)
static_obj_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 100), (150,50)), text="Spawn Static Object", manager=manager, container=ui_panel)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 400), (50, 50)), manager=manager, container=ui_panel, text="Start")
restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 400), (75, 50)), manager=manager, container=ui_panel, text="Reset")
objs = []

simulation_started = False

last_click_time = 0
DOUBLE_CLICK_TIME_THRESHOLD = 300

is_dragging = False
dragged_object = None
offset_x = 0
offset_y = 0

def createphysicsobject():
    rect_width = 30
    rect_height = 30
    rect_x = random.randint(250, 900)
    rect_y = random.randint(100, 300)
    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 225))

    obj = physics_obj(50, rect_x, rect_y, rect_width, rect_height, c, DEFAULT_GRAVITY_M_S2)
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

    ui_consumed_mouse_down = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if manager.process_events(event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ui_consumed_mouse_down = True
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == physics_obj_button:
                print("SPAWN PHYSICS OBJECT")
                createphysicsobject()

            if event.ui_element == static_obj_button:
                print("SPAWN STATIC OBJECT")
                createstaticobject()

            if event.ui_element == start_button:
                if simulation_started:
                    print("Simulation already running, re-initializing physics objects.")
                    for obj in objs:
                        if isinstance(obj, physics_obj):
                            obj.reset()

                if Window_Manager.active_window:
                    for window in list(Window_Manager.active_window):
                        window.kill()
                        Window_Manager.active_window.remove(window) 
                
                simulation_started = True
                print("Simulation Started.")

            if event.ui_element == restart_button:
                simulation_started = False
                if Window_Manager.active_window:
                    for window in list(Window_Manager.active_window):
                        window.kill()
                        Window_Manager.active_window.remove(window)
                for obj in objs:
                    if isinstance(obj, physics_obj):
                        obj.reset()
                print("Simulation Reset.")
                pass

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if hasattr(event.ui_element, 'object_ids'):
                if '#mass_input' in event.ui_element.object_ids:
                    Window_Manager.update_value(event.ui_element, "mass", "Mass : ")
                elif '#width_input' in event.ui_element.object_ids:
                    Window_Manager.update_value(event.ui_element, "width", "Width : ")
                elif '#height_input' in event.ui_element.object_ids:
                    Window_Manager.update_value(event.ui_element, "height", "Height : ")
                elif '#initial_velocity_y_input' in event.ui_element.object_ids:
                    Window_Manager.update_value(event.ui_element, "initial_velocity_y", "IVY : ")
                elif '#initial_velocity_x_input' in event.ui_element.object_ids:
                    Window_Manager.update_value(event.ui_element, "initial_velocity_x", "IVX : ")
                elif '#gravity_input' in event.ui_element.object_ids:
                    Window_Manager.update_value(event.ui_element, "gravity_force", "Gravity : ")


        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            closed_window = event.ui_element
            if closed_window in Window_Manager.active_window:
                Window_Manager.active_window.remove(closed_window)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not ui_consumed_mouse_down:
                current_time = pygame.time.get_ticks()
                if current_time - last_click_time < DOUBLE_CLICK_TIME_THRESHOLD:
                    for obj in objs:
                        if obj.rect.collidepoint(event.pos):
                            window_exists = False
                            for existing_window in Window_Manager.active_window:
                                if hasattr(existing_window, 'linked_object') and existing_window.linked_object == obj:
                                    window_exists = True
                                    manager.set_focus_set(existing_window) 
                                    break
                            if not window_exists:
                                Window_Manager.createwindow(obj, manager)
                            break
                    last_click_time = 0
                else:
                    last_click_time = current_time
                    if not simulation_started:
                        for obj in objs:
                            if obj.rect.collidepoint(event.pos):
                                is_dragging = True
                                dragged_object = obj
                                mouse_x, mouse_y = event.pos
                                offset_x = obj.x - mouse_x
                                offset_y = obj.y - mouse_y
                                objs.remove(obj)
                                objs.append(obj)
                                break
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_dragging = False
            dragged_object = None

        if event.type == pygame.MOUSEMOTION and is_dragging and dragged_object:
            mouse_x, mouse_y = event.pos
            dragged_object.x = mouse_x + offset_x
            dragged_object.y = mouse_y + offset_y
            dragged_object.updaterect()
            for window in Window_Manager.active_window:
                if hasattr(window, 'linked_object') and window.linked_object == dragged_object:
                    window.set_position((dragged_object.x - 50, dragged_object.y - 100))
                    break

    screen.fill((0,0,0))
    
    for obj in objs:
        obj.create_sprite(screen)
        if isinstance(obj, physics_obj) and simulation_started:
            for obj2 in objs:
                obj.collision_detection(obj2)
                pass
            obj.apply_velocity_y(seconds)
            obj.apply_velocity_x()
            obj.getweight(obj.gravity_force)
            obj.getdistancey()


    manager.update(delta)
    manager.draw_ui(screen)
    pygame.display.flip()