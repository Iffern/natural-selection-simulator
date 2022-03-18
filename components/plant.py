from components.point import Point


class Plant:
    def __init__(self, position: Point = None, energy: float = None):
        self.position = position
        self.energy = energy
