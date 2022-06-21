import mesa
from mesa.space import MultiGrid

class MultiGridWithHome(MultiGrid):
    """A multigrid with home area
    """
    
    def __init__(self, width, height, torus, home):
        super().__init__(width, height, torus)
        self.home = home
