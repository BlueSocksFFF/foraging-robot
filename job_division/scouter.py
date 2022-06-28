import mesa
from random_foraging import Forager

class Scouter(Forager):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)