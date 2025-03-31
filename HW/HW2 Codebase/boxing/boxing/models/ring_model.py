import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    """
    A class to manage a ring with boxers.

    Attributes:
        ring (List[Boxer]): The list of boxers in the ring.

    """

    def __init__(self):
        """Initializes the RingModel with an empty ring.

        """
        self.ring: List[Boxer] = []

    def fight(self) -> str:

        """compute outcome of a fight between two boxers.

        Args:
            self (Boxer): The boxer initiating the fight.

        Returns: 
            name of the winner (str)

        Raises:
            ValueError: If there are less than two boxers in the ring.
     

        """

        if len(self.ring) < 2:
            logger.error(f"There must be two boxers to start a fight.")
            raise ValueError("There must be two boxers to start a fight.")

        boxer_1, boxer_2 = self.get_boxers()

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)

        # Compute the absolute skill difference
        # And normalize using a logistic function for better probability scaling
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))

        random_number = get_random()

        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1

        update_boxer_stats(winner.id, 'win')
        update_boxer_stats(loser.id, 'loss')

        self.clear_ring()

        return winner.name

    def clear_ring(self):
        """Clears all boxers from the ring. If the ring is already empty, logs a warning.

        """
        if not self.ring:
            logger.error("Ring is empty")
            raise ValueError("Ring is empty")
        
        self.ring.clear()

    def enter_ring(self, boxer: Boxer):
        """Adds a boxer to the ring.

        Args:
            boxer (Boxer): The boxer to enter the ring.

        Raises:
            TypeError: If the boxer is not a valid Boxer instance.
            ValueError: If the ring is already full.

        """
        if not isinstance(boxer, Boxer):
            logger.error("Invalid type: Boxer is not a valid Boxer instance")
            raise TypeError(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")

        if len(self.ring) >= 2:
            logger.error(f"Ring is full, cannot add more boxers.")
            raise ValueError("Ring is full, cannot add more boxers.")

        self.ring.append(boxer)
        logger.info(f"Successfully added boxer to ring: {boxer.name} ")


    def get_boxers(self) -> List[Boxer]:
        """Returns a list of all boxers currently in the ring.

        Returns:
            List[Boxer]: A list of all boxers currently in the ring.

        Raises:
            ValueError: If the ring is empty.

        """
        if not self.ring:
            logger.error("Ring is empty")
            raise ValueError("Ring is empty")
            
        else:
            logger.info("Retrieving all boxers in the ring")

        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        """Returns the quantifled skill value of boxer.

        Returns:
            float: The the quantifled skill value of boxer.

        """
        # Arbitrary calculations
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier
        logger.info(f"Retrieving fighting skill for boxer: {skill} ")


        return skill