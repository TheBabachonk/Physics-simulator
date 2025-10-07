import pygame
import pygame_gui

pygame.init()

screen_largeur = 800
screen_longueur = 600
screen = pygame.display.set_mode((screen_largeur, screen_longueur))
clock = pygame.time.Clock()
running = True
manager = pygame_gui.UIManager((800, 600))
#button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text="button", manager=manager)

while running:
    delta = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            pass


        manager.process_events(event)
    
    manager.update(delta)

    pygame.display.flip()
    manager.draw_ui(screen)