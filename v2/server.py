import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from forager import Forager
from food import Food
from obstacle import Obstacle
from model import RandomForagingModel

def agent_portrayal(agent):
    
    if agent is None:
        return
    
    portrayal = {}
    
    if type(agent) is Forager:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Color"] = "Aquamarine"
        portrayal["Filled"] = True
        portrayal["Layer"] = 2

    elif type(agent) is Food:
        portrayal["Shape"] = "rect"
        portrayal['w'] = 0.5
        portrayal['h'] = 0.5
        portrayal["Color"] = "Plum"
        portrayal["Filled"] = True
        portrayal["Layer"] = 1
        
    elif type(agent) is Obstacle:
        portrayal["Shape"] = "rect"
        portrayal['w'] = 1
        portrayal['h'] = 1
        portrayal["Color"] = "Olive"
        portrayal["Filled"] = True
        portrayal["Layer"] = 0
        
        
    return portrayal

canvas_element = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

#TODO: add model params

server = ModularServer(
    RandomForagingModel,
    [canvas_element],
    "Forager Simulation",
    {"width":10, "height":10}
)
server.port = 8521