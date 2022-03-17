import pygame
import pygame_widgets

from sidebar import SideBar

pygame.init()

screen = pygame.display.set_mode([1000, 700])

running = True

side_bar = SideBar(800, 50)

screen.fill((255, 255, 255))
side_bar.add_slider(screen, 0, "Number of males", 1, 20, 4)
side_bar.add_slider(screen, 70, "Number of females", 1, 20, 4)
side_bar.add_slider(screen, 140, "Plant growth per round", 1, 7, 1)
side_bar.add_slider(screen, 210, "Plant energy value", 1, 100, 5)
side_bar.add_slider(screen, 280, "Maximum energy", 10, 1000, 100)
side_bar.add_slider(screen, 350, "Animal energy demand per day", 1, 20, 3)
side_bar.add_slider(screen, 420, "Breeding energy demand - female", 1, 200, 5)
side_bar.add_slider(screen, 490, "Breeding energy demand - male", 1, 200, 5)
side_bar.add_slider(screen, 560, "Maximum animal age - in rounds", 1, 300, 100)

while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    side_bar.update_sliders()

    pygame_widgets.update(events)
    pygame.display.update()

# Done! Time to quit.
pygame.quit()