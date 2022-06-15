import mesa
from mesa.time import SimultaneousActivation
# Step can be divided into stages
from mesa.space import MultiGrid
# It is arbitrary

from mesa import Agent, Model 

class FoodAgent(Agent):
    """Agent that is food"""
    def __init__(self, unique_id, model):
        '''Could add more attributes'''
        super().__init__(unique_id, model)
        # Set Location
        
    def step(self):
        # To be edited
        pass      
    
class ForagerAgent(Agent):
    """Agent that forages food"""
    
    def __init__(self, unique_id, model):
        '''Could add more attributes'''
        super().__init__(unique_id, model)
        
    def step(self):
        '''Location change'''
        self.move()
        
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = False,
            include_center = False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
class InitialModel(Model):
    """The most basic model"""
    
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.schedule = SimultaneousActivation(self)
        self.grid = MultiGrid(width, height, False)
        # Cannot be torus because it cannot move cross boarder
        
        # Create agents
        for i in range(self.num_agents):

            a = ForagerAgent(i, self)
            self.schedule.add(a)
            
            # Add agents to the grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
    def step(self):
        self.schedule.step()