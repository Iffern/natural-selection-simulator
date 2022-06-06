import pygame_widgets
from pygame import Surface

from config import PLANT_ENERGY, PLANT_GROWTH_PER_ROUND, BREED_ENERGY_FEMALE, BREED_ENERGY_MALE, \
    ENERGY_DEMAND_PER_ROUND, NUMBER_OF_MALE_ANIMALS, NUMBER_OF_FEMALE_ANIMALS
from gui.button_type import ButtonType
from gui.slider_type import SliderType
from gui.sidebar import SideBar


class SimulationSettings:
    side_bar: SideBar
    screen: Surface

    def __init__(self, side_bar: SideBar, screen: Surface):
        self.side_bar = side_bar
        self.screen = screen

    def set_default_configuration(self):
        self.side_bar.add_slider(self.screen, 0, "Number of males", 1, 20, NUMBER_OF_MALE_ANIMALS, SliderType.MALE)
        self.side_bar.add_slider(self.screen, 70, "Number of females", 1, 20, NUMBER_OF_FEMALE_ANIMALS, SliderType.FEMALE)
        self.side_bar.add_slider(self.screen, 140, "Plant growth per round", 1, 100, PLANT_GROWTH_PER_ROUND, SliderType.PL_PER_ROUND)
        self.side_bar.add_slider(self.screen, 210, "Plant energy value", 1, 100, PLANT_ENERGY, SliderType.PL_ENERGY)
        self.side_bar.add_slider(self.screen, 280, "Animal energy demand per day", 1, 20, ENERGY_DEMAND_PER_ROUND, SliderType.A_DAY_ENERGY)
        self.side_bar.add_slider(self.screen, 350, "Breeding energy demand - female", 1, 90, BREED_ENERGY_FEMALE, SliderType.F_BREEDING)
        self.side_bar.add_slider(self.screen, 420, "Breeding energy demand - male", 1, 90, BREED_ENERGY_MALE, SliderType.M_BREEDING)
        self.side_bar.add_slider(self.screen, 490, "Maximum animal age - in rounds", 1, 300, 100, SliderType.MAX_AGE)
        self.side_bar.add_button(self.screen, 0, 560, ButtonType.RESET, (255, 0, 0), True)
        self.side_bar.add_button(self.screen, 95, 560, ButtonType.START, (126, 245, 66), False)

    def update_settings(self, events):
        self.side_bar.update_sliders()
        pygame_widgets.update(events)

    def get_slider_value_by_type(self, slider_type: SliderType):
        slider = self.side_bar.get_slider_by_type(slider_type)
        return slider.getValue()

    def get_button_value_by_type(self, button_type: ButtonType):
        return self.side_bar.get_button_value(button_type)
