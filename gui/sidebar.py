import pygame
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from gui.button_type import ButtonType
from gui.slider_type import SliderType


class SideBar:

    def __init__(self, x, y):
        self.X = x + 10
        self.Y = y
        self.sliders = {}
        self.font = pygame.font.SysFont('georgia', 12)
        self.buttons = {}
        self.reset = False
        self.start = True

    def add_slider(self, surface, offset_y, text, minimum, maximum, initial, slider_type: SliderType):
        text_surface = self.font.render(text, True, (0, 0, 0))
        surface.blit(text_surface, (self.X, self.Y+offset_y))
        slider = Slider(surface, self.X, self.Y + offset_y + 25, 90, 10, min=minimum, max=maximum, initial=initial,
                        handleRadius=4, colour=(121, 210, 121), handleColour=(77, 0, 77))
        output = TextBox(surface, self.X+30, self.Y + offset_y + 40, 30, 20, fontSize=16, borderThickness=0, radius=1,
                         font=self.font, colour=(255, 217, 179))
        output.disable()
        self.sliders[slider_type] = (slider, output)

    def update_sliders(self):
        for (slider, text_box) in self.sliders.values():
            text_box.setText(slider.getValue())

    def add_button(self, surface, offset_x, offset_y, button_type: ButtonType, color, is_reset):

        if is_reset:
            on_click = lambda: self.change_reset()
        else:
            on_click = lambda: self.change_start()

        self.buttons[button_type] = Button(surface, self.X + offset_x, self.Y + offset_y + 25, 90, 25,
                                    text=button_type.value, textColour=(255, 255, 255),
                                    radius=5, colour=color, onClick=on_click)

    def get_slider_by_type(self, slider_type: SliderType):
        return self.sliders[slider_type][0]

    def get_button(self, button_type: ButtonType):
        return self.buttons[button_type]

    def change_reset(self):
        self.reset = not self.reset

    def change_start(self):
        self.start = not self.start

    def get_button_value(self, button_type: ButtonType):
        match button_type:
            case ButtonType.START:
                return self.start
            case ButtonType.RESET:
                return self.reset

