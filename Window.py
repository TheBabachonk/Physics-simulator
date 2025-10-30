import pygame
import pygame_gui
from pygame_gui.elements import UITextEntryLine
from Classes import physics_obj

active_window = []
current_windowed_object = None
stop = False

def createwindow(obj, manager):
    global current_windowed_object

    rect_x = 50

    current_windowed_object = obj


    window_height = 240
    if isinstance(obj, physics_obj):
        window_height = 280
    
    obj_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((obj.rect.x, obj.rect.y), (200, window_height)), manager=manager, window_display_title="Object Properties")

    obj_window.linked_object = obj
    obj_window.owner_window = obj_window
    
    active_window.append(obj_window)

    mass_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 0), (100, 20)), manager=manager, container=obj_window, text=f"Mass : {obj.mass}")
    mass_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 20), (100, 20)), manager=manager, container=obj_window, object_id='#mass_input')

    width_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 40), (100, 20)), manager=manager, container=obj_window, text=f"Width : {obj.width}")
    width_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 60), (100, 20)), manager=manager, container=obj_window, object_id='#width_input')

    height_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 80), (100, 20)), manager=manager, container=obj_window, text=f"Height : {obj.height}" )
    height_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 100), (100, 20)), manager=manager, container=obj_window, object_id='#height_input')

    if isinstance(obj, physics_obj):
        initial_velocity_y_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 120), (100, 20)), manager=manager, container=obj_window, text=f"IVY : {obj.initial_velocity_y}")
        initial_velocity_y_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 140), (100, 20)), manager=manager, container=obj_window, object_id='#initial_velocity_y_input')
        initial_velocity_x_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 160), (100, 20)), manager=manager, container=obj_window, text=f"IVX : {obj.initial_velocity_x}")
        initial_velocity_x_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 180), (100, 20)), manager=manager, container=obj_window, object_id="#initial_velocity_x_input")
        
        # NEW: Gravity input for physics objects
        gravity_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((rect_x, 200), (100, 20)), manager=manager, container=obj_window, text=f"Gravity : {obj.gravity_force:.2f}")
        gravity_input = UITextEntryLine(relative_rect=pygame.Rect((rect_x, 220), (100, 20)), manager=manager, container=obj_window, object_id='#gravity_input')


        obj_window.initial_velocity_y_label = initial_velocity_y_label
        obj_window.initial_velocity_x_label = initial_velocity_x_label
        initial_velocity_y_input.parent_window_ref = obj_window
        initial_velocity_x_input.parent_window_ref = obj_window
        
        initial_velocity_y_input.linked_object = obj
        initial_velocity_x_input.linked_object = obj

        # NEW: Link gravity elements
        obj_window.gravity_label = gravity_label
        gravity_input.parent_window_ref = obj_window
        gravity_input.linked_object = obj

    else:
        initial_velocity_y_label = None 
        initial_velocity_y_input = None
        gravity_label = None
        gravity_input = None


    obj_window.mass_label = mass_label
    obj_window.width_label = width_label
    obj_window.height_label = height_label


    mass_input.linked_object = obj
    mass_input.parent_window_ref = obj_window
    width_input.linked_object = obj
    width_input.parent_window_ref = obj_window
    height_input.linked_object = obj
    height_input.parent_window_ref = obj_window


def update_value(text_input_element, obj_parameter, obj_text):
    obj = text_input_element.linked_object
    parent_window = text_input_element.parent_window_ref
    
    if obj is None or parent_window is None:
        print("Error: Linked object or parent window reference missing on input element.")
        return

    try:
        new_value = float(text_input_element.get_text())
        
        setattr(obj, obj_parameter, new_value)
        
        if obj_parameter == "mass":
            parent_window.mass_label.set_text(f"{obj_text} {getattr(obj, obj_parameter)}")
        elif obj_parameter == "width":
            parent_window.width_label.set_text(f"{obj_text} {getattr(obj, obj_parameter)}")
            obj.rect.width = int(new_value)
        elif obj_parameter == "height":
            parent_window.height_label.set_text(f"{obj_text} {getattr(obj, obj_parameter)}")
            obj.rect.height = int(new_value)
        elif obj_parameter == "initial_velocity_y":
            if isinstance(obj, physics_obj) and parent_window.initial_velocity_y_label:
                parent_window.initial_velocity_y_label.set_text(f"{obj_text} {getattr(obj, obj_parameter)}")
                obj.velocity_y = new_value # This affects the current velocity
        elif obj_parameter == "initial_velocity_x":
            if isinstance(obj, physics_obj) and parent_window.initial_velocity_x_label:
                parent_window.initial_velocity_x_label.set_text(f"{obj_text} {getattr(obj, obj_parameter)}")
                obj.velocity_x = new_value # This affects the current velocity
        # NEW: Handle gravity_force update
        elif obj_parameter == "gravity_force":
            if isinstance(obj, physics_obj) and parent_window.gravity_label:
                parent_window.gravity_label.set_text(f"{obj_text} {getattr(obj, obj_parameter):.2f}")


    except ValueError:
        print(f"Invalid input for {obj_parameter}: {text_input_element.get_text()}")