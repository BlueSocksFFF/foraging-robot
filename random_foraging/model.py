import mesa

from mesa.time import SimultaneousActivation
from grid import MultiGridWithHome, GridWithObstacles
from forager import Forager
from food import Food
from obstacle import Obstacle

class RandomForagingModel(mesa.Model):
    """_
    Random Foraging Model
    """
    
    height_preset = 10
    width_preset = 10
    
    number_food_preset = 5
    number_foragers_preset = 3
    
    home_preset = (0, 0, 0, 0)
    
    with_obstacles_preset = True
    
    def __init__(
        self, 
        height = height_preset,
        width = width_preset,
        number_food = number_food_preset,
        number_foragers = number_foragers_preset,
        home = home_preset,
        with_obstacles = with_obstacles_preset
    ):
        
        super().__init__()
        self.height = height
        self.width = width
        self.number_food = number_food
        self.number_foragers = number_foragers
        self.home = home
        self.schedule = SimultaneousActivation(self)
        self.with_obstacles = with_obstacles
        self.init_grid()
        self.place_foragers()
        self.place_food()
        self.place_obstacles()
        
    def init_grid(self):
        if self.with_obstacles:
            self.grid = GridWithObstacles(self.width, self.height, torus=False, home=self.home)
        else:
            self.grid = MultiGridWithHome(self.width, self.height, torus=False, home=self.home)
        self.home_x_min, self.home_x_max, self.home_y_min, self.home_y_max = self.grid.home
                    
    def place_foragers(self):
        for i in range(self.number_foragers):
            forager = Forager(self.next_id(), self)
            self.schedule.add(forager)
            x = self.random.randrange(self.home_x_min, self.home_x_max+1)
            y = self.random.randrange(self.home_y_min, self.home_y_max+1)
            self.grid.place_agent(forager, (x, y))
        
    def place_food(self):
        for i in range(self.number_food):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            while x>=self.home_x_min and x<=self.home_x_max and y>=self.home_y_min and y<=self.home_y_max:
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
            food = Food(self.next_id(), self)
            self.schedule.add(food)
            self.grid.place_agent(food, (x, y))
    
    def place_obstacles(self):
        if not self.with_obstacles:
            return
        else:
            for i in range(self.grid.num_obstacles):
                x_min, x_max, y_min, y_max = self.grid.obstacles[i]
                for x in range(x_min, x_max+1):
                    for y in range(y_min, y_max+1):
                        obstacle = Obstacle(self.next_id(), self)
                        self.grid.place_agent(obstacle, (x, y))
            
    def step(self):
        if self.number_food == 0:
            print("Found all food.")
        self.schedule.step()