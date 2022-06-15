import mesa

class Forager(mesa.Agent):
    """Forager: created randomly and moves randomly to neighboring cells.
    Number is assigned.
    Can only carry one food at a time.
    MultiGrid Based.
    Simultaneous Activation."""
    
    """To Be Added: 2. Prefers New Location - Better Algorithm
                    1. Start from Home and Move Back to Home
    """
    
    
    def __init__(self, unique_id, pos, model, home, grid_width, grid_length):
        super().__init__(unique_id, model)
        self.pos = pos # Tuple for (x, y) coordinates
        self.home = home
        '''To be decided what type of reference should be used here'''
        self.food_id = None 
        '''Not Carrying food: None.
            Carrying food: unique_id of agent Food.'''
        self.past_path = None
    
    def move(self):
        if food_id == None:
            self.move_randomly()
            
    def move_randomly(self):
        neighbors = 
            
    