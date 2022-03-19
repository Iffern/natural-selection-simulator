import pygame

from components import config


class Map:
    def __init__(self, screen):
        self.width = config.MAP_WIDTH
        self.height = config.MAP_HEIGHT
        self.screen = screen
        self.plant = pygame.transform.scale(pygame.image.load('gui/resources/seeds.png'), (20, 20))
        self.animal_female = pygame.transform.scale(pygame.image.load('gui/resources/peacock_female.png'), (50, 50))
        self.animal_male = pygame.transform.scale(pygame.image.load('gui/resources/peacock_male.png'), (60, 60))
        self.animals = []
        self.plants = []

    def render(self):
        self.screen.blit(self.plant, (0, 0))
        self.screen.blit(self.animal_female, (0, 30))
        self.screen.blit(self.animal_male, (0, 80))
