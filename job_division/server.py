import mesa
import sys
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from forager import Forager
from model import JobDivisionModel

sys.path.insert(1, '../random_foraging')
from food import Food
from obstacle import Obstacle


def agent_portrayal(agent):
    if agent is None:
        print('Error: None agent')
        return

    portrayal = {}

    if type(agent) is Forager:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Filled"] = True
        portrayal["Layer"] = 2
        if agent.as_scouter:
            portrayal["Color"] = "Orange"
        else:
            portrayal["Color"] = "Aquamarine"

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


canvas_element = CanvasGrid(agent_portrayal, 10, 11, 500, 500)

server = ModularServer(
    JobDivisionModel,
    [canvas_element],
    "Forager Simulation",
    {"width": 10, "height": 11}
)
server.port = 8521
