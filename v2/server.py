import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from forager import Forager
from food import Food
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
        portrayal["Layer"] = 0

    elif type(agent) is Food:
        portrayal["Shape"] = "rect"
        portrayal['w'] = 0.5
        portrayal['h'] = 0.5
        portrayal["Color"] = "Plum"
        portrayal["Filled"] = True
        portrayal["Layer"] = 1
        
        
    return portrayal

canvas_element = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

#TODO: add model params

server = ModularServer(
    RandomForagingModel,
    [canvas_element],
    "Forager Simulation",
    {"width":20, "height":20}
)
server.port = 8521