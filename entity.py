import random
from typing import List

from random_walk import RandomWalk
from rules import Rules


class Entity(object):
    def __init__(self, map: 'Map'):
        self.pos = RandomWalk.random_start_pos()
        """ position on the map"""

        self.infectous: bool = False
        """ entity can infect others"""

        self.recovered: bool = False
        """ entity is recovered. Entity may still be not immune when recover_effect < 1.0 """

        self.immune: bool = False
        """ person is immune and can't be infected. """

        self.days_since_exposure: int = -1
        """ how many days have passed since exposure.
        -1: person is not infected
         0: the person has been infected today
        """
        self.map = map

    def end_infection(self):
        """ entity recovers"""
        self.days_since_exposure = -1
        self.infectous = 0
        self._recover()

    def walk(self):
        """ changes position with the pattern of a levi flight """
        self.pos = RandomWalk.levy_flight(self.pos)

    def spread(self):
        """ if the person is infectous, expose all near entities with specified probabilty"""
        if self.infectous:
            near_entities: List[Entity] = self.map.get_near_entities(self, Rules.max_distance_spread)
            for near_entity in near_entities:
                probability = Rules.spread_probability
                near_entity.expose(probability)

    def expose(self, probability):
        """ expose the person to the virus with a given infection probability.
        A person that is infected at the moment, can't be infected again.
        """
        if self.immune or self.days_since_exposure >= 0:
            return
        if random.random() < probability:
            self._infect()

    # PRIVATE

    def _immunize(self, probability=1.0):
        if not self.immune:
            self.immune = random.random() < probability

    def _infect(self):
        self.days_since_exposure = 0

    def _recover(self):
        self.recovered = True
        self._immunize(Rules.recover_effect)

