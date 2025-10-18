import pygame
import pygame_gui
from pygame_gui.elements import UITextEntryLine

active_window_objects = []
current_windowed_object = None
mass_input = None
width_input = None
height_input = None
mass_label = None
width_label = None
height_label = None

def createwindow(obj, manager):
    global active_window
    global current_windowed_object
    global mass_input
    global width_input
    global height_input
    global width_label
    global mass_label
    global height_label


    rect_x = 50

    current_windowed_object = obj

    if active_window is not None:
        active_window.kill()
        active_window = None



    obj_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((obj.x, obj.y), (200, 200)), manager=manager, window_display_title="UPUPITSOURMOMENT")

    active_window = obj_window

    mass_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 0), (100, 20)), manager=manager, container=obj_window, text=f"Mass : {obj.mass}")

    mass_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 20), (100, 20)), manager=manager, container=obj_window)

    width_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 40), (100, 20)), manager=manager, container=obj_window, text=f"Width : {obj.width}")

    width_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 60), (100, 20)), manager=manager, container=obj_window)

    height_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 80), (100, 20)), manager=manager, container=obj_window, text=f"Height : {obj.height}" )

    height_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 100), (100, 20)), manager=manager, container=obj_window)


    


def update_value(obj, obj_input, obj_parameter, obj_label, obj_text):
    new_value = float(obj_input)
    setattr(obj, obj_parameter, new_value)
    obj_label.set_text(f"{obj_text} {getattr(obj, obj_parameter)}")

    if obj_parameter == "width":
        obj.rect.width = int(new_value)

    if obj_parameter == "height":
        obj.rect.height = int(new_value)