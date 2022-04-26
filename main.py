import pygame
import pygame_widgets
from pygame.rect import Rect

from gui import gui_config
from gui.map import Map
from gui.sidebar import SideBar

pygame.init()

screen = pygame.display.set_mode([gui_config.WIDTH, gui_config.HEIGHT])
pygame.display.set_caption("Natural selection simulator")

running = True

side_bar = SideBar(gui_config.WIDTH - gui_config.BAR_WIDTH, 50)
map_visualisation = Map(screen)

screen.fill((255, 255, 255))
side_bar.add_slider(screen, 0, "Number of males", 1, 20, 4)
side_bar.add_slider(screen, 70, "Number of females", 1, 20, 4)
side_bar.add_slider(screen, 140, "Plant growth per round", 1, 100, 10)
side_bar.add_slider(screen, 210, "Plant energy value", 1, 100, 5)
side_bar.add_slider(screen, 280, "Animal energy demand per day", 1, 20, 3)
side_bar.add_slider(screen, 350, "Breeding energy demand - female", 1, 90, 15)
side_bar.add_slider(screen, 420, "Breeding energy demand - male", 1, 90, 15)
side_bar.add_slider(screen, 490, "Maximum animal age - in rounds", 1, 300, 100)

while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    pygame.draw.rect(screen, (188, 235, 134), Rect(0, 0, gui_config.WIDTH - gui_config.BAR_WIDTH, gui_config.HEIGHT))

    side_bar.update_sliders()
    map_visualisation.render()

    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()