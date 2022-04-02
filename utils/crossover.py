import random
from abc import ABC, abstractmethod
from components.attributes import Attributes
from config import CROSSOVER


class Crossover(ABC):

    @abstractmethod
    def get_crossover(self, f_attr: Attributes, m_attr: Attributes) -> Attributes:
        pass


class AverageCrossover(Crossover):

    def get_crossover(self, f_attr: Attributes, m_attr: Attributes) -> Attributes:
        color = (f_attr.color + m_attr.color) / 2
        tail = (f_attr.tail + m_attr.tail) / 2
        return Attributes(color, tail)


class WeightedAverageCrossover(Crossover):
    f_alpha: float = CROSSOVER['w_avg']['alpha']
    m_beta: float = CROSSOVER['w_avg']['beta']

    def get_crossover(self, f_attr: Attributes, m_attr: Attributes) -> Attributes:
        color = self.f_alpha * f_attr.color + self.m_beta * m_attr.color
        tail = self.f_alpha * f_attr.tail + self.m_beta * m_attr.tail
        return Attributes(color, tail)


class BlendCrossoverAB(Crossover):
    f_alpha: float = CROSSOVER['blx']['alpha']
    m_beta: float = CROSSOVER['blx']['beta']

    def get_crossover(self, f_attr: Attributes, m_attr: Attributes) -> Attributes:
        return Attributes(self.__blx(f_attr.color, m_attr.color), self.__blx(f_attr.tail, m_attr.tail))

    def __blx(self, f_attr: float,  m_attr: float) -> float:
        diff = abs(f_attr - m_attr)

        if f_attr <= m_attr:
            child_attr = random.uniform(f_attr - self.f_alpha * diff, m_attr + self.m_beta * diff)
        else:
            child_attr = random.uniform(m_attr - self.m_beta * diff, f_attr + self.f_alpha * diff)

        return child_attr
