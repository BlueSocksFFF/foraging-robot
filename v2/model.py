import mesa

from mesa.time import SimultaneousActivation
from grid import MultiGridWithHome
from forager import Forager
from food import Food

class RandomForagingModel(mesa.Model):
    """_
    Random Foraging Model
    """
    
    height_preset = 20
    width_preset = 20
    
    food_ratio_preset = 0.2
    number_foragers_preset = 3
    
    home_preset = (0, 0, 0, 0)
    
    verbose = True
    
    def __init__(
        self, 
        height = height_preset,
        width = width_preset,
        food_ratio = food_ratio_preset,
        number_foragers = number_foragers_preset
    ):
        
        super().__init__()
        self.height = height
        self.width = width
        self.food_ratio = food_ratio
        self.number_foragers = number_foragers
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGridWithHome(self.width, self.height, torus=False, home=(0, 0, 0, 0))
        
        #TODO: Add Data Collector
                
        home_x_min, home_x_max, home_y_min, home_y_max = self.grid.home
        
        for i in range(self.number_foragers):
            forager = Forager(self.next_id(), self)
            self.schedule.add(forager)
            x = self.random.randrange(home_x_min, home_x_max+1)
            y = self.random.randrange(home_y_min, home_y_max+1)
            self.grid.place_agent(forager, (x, y))
            # Test
            print(i, x, y)
            
        for i in range(int(self.grid.width*self.grid.height*self.food_ratio)):
            food = Food(self.next_id(), self)
            self.schedule.add(food)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            # while x>=home_x_min & x<=home_x_max & y>=home_y_min & y<=home_y_max:
            #     x = self.random.randrange(width)
            #     y = self.random.randrange(height)
            self.grid.place_agent(food, (x, y))
            # Test
            print(i, x, y)
            
    def step(self):
        self.schedule.step()
        #Add verbose test
        