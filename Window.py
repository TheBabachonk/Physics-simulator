import pygame
import pygame_gui
from pygame_gui.elements import UITextEntryLine

active_window = None
current_windowed_object = None
mass_input = None
width_input = None
current_mass = None

def createwindow(obj, manager):
    global active_window
    global current_windowed_object
    global mass_input
    global current_mass

    rect_x = 50

    current_windowed_object = obj

    if active_window is not None:
        active_window.kill()
        active_window = None



    obj_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((obj.x, obj.y), (200, 200)), manager=manager, window_display_title="UPUPITSOURMOMENT")

    active_window = obj_window

    current_mass = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 0), (100, 20)), manager=manager, container=obj_window, text=f"Mass : {obj.mass}")

    mass_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 20), (100, 20)), manager=manager, container=obj_window)

    width = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 40), (100, 20)), manager=manager, container=obj_window, text=f"Width : {obj.width}")

    width_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 60), (100, 20)), manager=manager, container=obj_window)

    print(current_windowed_object)

def update_mass(obj):
    new_mass = float(mass_input.text)
    obj.mass = new_mass
    current_mass.set_text(f"Mass : {obj.mass}")
    print(obj.mass)
