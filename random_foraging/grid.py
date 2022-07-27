import mesa
from mesa.space import MultiGrid


class MultiGridWithHome(MultiGrid):
    """A multigrid with home area
    """
    
    def __init__(self, width, height, torus, home):
        super().__init__(width, height, torus)
        self.home = home
        self.food_list = []
        
    def add_to_food_list(self, food_id):
        self.food_list.append(food_id)
