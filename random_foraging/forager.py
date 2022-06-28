import mesa
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
        
    def get_id(self):
        return self.unique_id
    
    def move(self):
        if self.model.number_food == 0:
            if self.at_home:
                print("End with number of rounds: %s" %self.num_rounds)
                return
            else:
                self.move_home()
        elif self.food_id == None:
            self.move_randomly()
        else:
            self.move_home()
            
    def move_randomly(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(neighbors)
        while self.check_content(new_position, Obstacle) != None:
            neighbors.remove(new_position)
            new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)
        self.at_home = False
        
    def check_content(self, pos, type):
        cell_content = self.model.grid.get_cell_list_contents([pos])
        for obj in cell_content:
            if isinstance(obj, type):
                return obj
        return None
            
    def move_home(self):
        # TODO: revise to make it more elegant
        home_x_min, home_x_max, home_y_min, home_y_max = self.model.grid.home
        pos_x, pos_y = self.pos
        if home_x_max < pos_x:
            self.model.grid.move_agent(self, (pos_x-1, pos_y))
        elif home_x_min > pos_x:
            self.model.grid.move_agent(self, (pos_x+1, pos_y))
        elif home_y_max < pos_y:
            self.model.grid.move_agent(self, (pos_x, pos_y-1))
        elif home_y_min > pos_y:
            self.model.grid.move_agent(self, (pos_x, pos_y+1))
        else:
            self.at_home = True
            self.food_id = None
            self.model.grid.add_to_food_list(self.food_id)
            self.num_rounds += 1
            
    def print_summary(self):
        print("Forager id: %s, number of rounds: %s" %(self.unique_id, self.num_rounds))
                       
    def step(self):
        self.move()
        
    def advance(self):
        if self.food_id != None:
            return
        if self.check_content(self.pos, Food) != None:
            food = self.check_content(self.pos, Food)
            self.food_id = food.get_id()
            self.model.grid.remove_agent(food)
            self.model.number_food -= 1