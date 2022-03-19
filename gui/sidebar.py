import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


class SideBar:

    def __init__(self, x, y):
        self.X = x + 10
        self.Y = y
        self.items = {}
        self.font = pygame.font.SysFont('georgia', 12)

    def add_slider(self, surface, offset_y, text, minimum, maximum, initial):
        text_surface = self.font.render(text, True, (0, 0, 0))
        surface.blit(text_surface, (self.X, self.Y+offset_y))
        slider = Slider(surface, self.X, self.Y + offset_y + 25, 90, 10, min=minimum, max=maximum, initial=initial,
                        handleRadius=4, colour=(121, 210, 121), handleColour=(77, 0, 77))
        output = TextBox(surface, self.X+30, self.Y + offset_y + 40, 30, 20, fontSize=16, borderThickness=0, radius=1,
                         font=self.font, colour=(255, 217, 179))
        output.disable()
        self.items[slider] = output

    def update_sliders(self):
        for key, value in self.items.items():
            value.setText(key.getValue())
