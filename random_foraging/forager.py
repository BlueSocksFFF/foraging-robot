import mesa
from astar import Astar
from food import Food
from obstacle import Obstacle

class Forager(mesa.Agent):
    """Forager: created randomly and moves randomly to neighboring cells.
    Number is assigned.
    Can only carry one food at a time.
    MultiGrid Based.
    Simultaneous Activation."""
    
    """To Be Added: 2. Prefers New Location - Better Algorithm
                    1. Start from Home and Move Back to Home
    """
    
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        '''To be decided what type of reference should be used here'''
        self.food_id = None 
        '''Not Carrying food: None.
            Carrying food: unique_id of agent Food.'''
        self.at_home = True
        self.num_rounds = 0
        self.a_star = Astar(self.model)
        self.path_home = []
        self.cost_home = 0
        
    def get_id(self):
        return self.unique_id
    
    def move(self):
        if self.model.number_food == 0:
            if self.at_home:
                print("End with number of rounds: %s" %self.num_rounds)
                return
            else:
                self.move_home()
        elif self.food_id != None:
            self.move_home()
        else:
            self.move_randomly()
            
    def move_randomly(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(neighbors)
        while self.check_content(new_position, Obstacle) != None:
            neighbors.remove(new_position)
            new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)
        
    def check_content(self, pos, type):
        cell_content = self.model.grid.get_cell_list_contents([pos])
        for obj in cell_content:
            if isinstance(obj, type):
                return obj
        return None
            
    def move_home(self):
        index = self.path_home.index(self.pos)
        pos_next = self.path_home[index+1]
        self.model.grid.move_agent(self, pos_next)
        
    def check_before_step(self):
        self.check_at_home()
        if self.food_id == None:
            food = self.check_content(self.pos, Food)
            if food != None:
                self.food_id = food.get_id()
                self.model.grid.remove_agent(food)
                self.model.number_food -= 1
                self.path_home, self.cost_home = self.a_star.construct_path(self.pos, self.model.grid.home)
            
    def print_summary(self):
        print("Forager id: %s, number of rounds: %s" %(self.unique_id, self.num_rounds))
                       
    def step(self):
        self.check_before_step()
        self.move()
        
    def advance(self):
        print(self.food_id)
        return
            
    def check_at_home(self):
        if self.pos in self.model.grid.home:
            self.at_home = True
            self.food_id = None
            return True
        else:
            self.at_home = False
            return False
            
    def test_astar(self, start, goals):
        return self.a_star.construct_path(start,goals)
        