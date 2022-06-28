import mesa

class Obstacle(mesa.Agent):
    """ Obstacles do not move.
        And do not allow other agents.
    """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def get_id(self):
        return self.unique_id
    
    def step(self):
        return
    
    def advance(self):
        return