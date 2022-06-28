import mesa

class Food(mesa.Agent):
    """ Food agent that does not move
    """
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def get_id(self):
        return self.unique_id
    
    def step(self):
        return
    
    def advance(self):
        #Test
        super()
        return