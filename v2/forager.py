import mesa
from food import Food

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
        self.past_path = None
        self.at_home = True
        
    def get_id(self):
        return self.unique_id
    
    def move(self):
        if self.food_id == None:
            #Test
            print("Move Randomly")
            self.move_randomly()
        else:
            print("Move Home")
            self.move_home()
            
    def move_randomly(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)
            
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
            
    def step(self):
        self.move()
        
    def advance(self):
        cell_content = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_content:
            if isinstance(obj, Food):
                self.food_id = obj.get_id()
                self.model.grid.remove_agent(obj)
        # Test
        print("forager", self.unique_id, self.pos, self.food_id)
        


        
        