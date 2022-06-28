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
        
class GridWithObstacles(MultiGridWithHome):
    """A Grid with obstacles
    """
    
    def __init__(self, width, height, torus, home):
        super().__init__(width, height, torus, home)
        self.obstacles = dict()
        self.num_obstacles = 0
        self.add_obstacle(5, 7, 5, 7)
        
    def add_obstacle(self, min_x, max_x, min_y, max_y):
        self.obstacles[self.num_obstacles] = (min_x, max_x, min_y, max_y)
        self.num_obstacles += 1