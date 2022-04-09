from components.point import Point
import pygame


class Plant:
    position: Point
    energy: float

    def __init__(self, position: Point = None, energy: float = None):
        self.position = position
        self.energy = energy

    def get_image(self):
        return 'gui/resources/seeds.png'

    def display(self, screen, scale: Point):
        display_size = 10
        display_position = (scale.x * self.position.x + scale.x / 2 - display_size / 2,
                            scale.y * self.position.y + scale.y / 2 - display_size / 2)
        scaled_image = pygame.transform.scale(pygame.image.load(self.get_image()), (display_size, display_size))
        screen.blit(scaled_image, display_position)
