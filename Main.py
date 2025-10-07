import pygame
import pygame_gui
import random

pygame.init()

screen_largeur = 1000
screen_longueur = 600
screen = pygame.display.set_mode((screen_largeur, screen_longueur))
clock = pygame.time.Clock()
running = True
manager = pygame_gui.UIManager((screen_largeur, screen_longueur))
ui_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (200,screen_longueur)), manager=manager, container=None)
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 0), (100, 50)), text="button", manager=manager, container=ui_panel)

def createphysicsobject():
    rect_width = 30
    rect_height = 30
    rect_x = random.randint(250, 900)
    rect_y = random.randint(100, 500)

    new_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 225))

    new_obj = pygame.draw.rect(screen, color, new_rect)


    pass

while running:
    delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                print("SPAWN PHYSICS OBJECT")
                createphysicsobject()
            pass


        manager.process_events(event)
    
    manager.update(delta)

    pygame.display.flip()
    manager.draw_ui(screen)