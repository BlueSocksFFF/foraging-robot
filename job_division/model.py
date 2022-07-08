import mesa
from mesa.time import SimultaneousActivation
import sys

from worker import Worker
from scouter import Scouter

sys.path.insert(1, '../random_foraging')
from grid import GridWithObstacles, MultiGridWithHome
from food import Food
from obstacle import Obstacle

class JobDivisionModel(mesa.Model):
    """
    Job Division Model
    """
    height_preset = 10
    width_preset = 10

    number_food_preset = 10
    number_workers_preset = 3
    number_scouter_preset = 1

    home_preset = [(0, 0), (1, 0)]

    with_obstacles_preset = True

    def __init__(
        self,
        height=height_preset,
        width=width_preset,
        number_food=number_food_preset,
        number_workers=number_workers_preset,
        number_scouters = number_scouter_preset,
        home=home_preset,
        with_obstacles=with_obstacles_preset
    ):

        super().__init__()
        self.height = height
        self.width = width
        self.number_food = number_food
        self.number_workers = number_workers
        self.number_scouters = number_scouters
        self.home = home
        self.schedule = SimultaneousActivation(self)
        self.grid = None
        self.scouter_list = []
        self.worker_list = []
        self.with_obstacles = with_obstacles
        self.init_grid()
        self.place_workers()
        self.place_scouters()
        self.place_obstacles()
        self.place_food()

    def init_grid(self):
        if self.with_obstacles:
            self.grid = GridWithObstacles(self.width, self.height, torus=False, home=self.home)
        else:
            self.grid = MultiGridWithHome(self.width, self.height, torus=False, home=self.home)

    def place_workers(self):
        for i in range(self.number_workers):
            worker = Worker(self.next_id(), self)
            self.worker_list.append(worker)
            self.schedule.add(worker)
            pos = self.random.choice(self.home)
            self.grid.place_agent(worker, pos)

    def place_scouters(self):
        for i in range(self.number_scouters):
            scouter = Scouter(self.next_id(), self)
            self.scouter_list.append(scouter)
            self.schedule.add(scouter)
            pos = self.random.choice(self.home)
            self.grid.place_agent(scouter, pos)

    def place_food(self):
        for i in range(self.number_food):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            while (x, y) in self.home or self.check_content((x, y), Obstacle) is not None:
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
            food = Food(self.next_id(), self)
            self.schedule.add(food)
            self.grid.place_agent(food, (x, y))

    def place_obstacles(self):
        if not self.with_obstacles:
            return
        else:
            for i in range(self.grid.num_obstacles):
                x_min, x_max, y_min, y_max = self.grid.obstacles[i]
                for x in range(x_min, x_max + 1):
                    for y in range(y_min, y_max + 1):
                        obstacle = Obstacle(self.next_id(), self)
                        self.grid.place_agent(obstacle, (x, y))

    def check_content(self, pos, its_type):
        cell_content = self.grid.get_cell_list_contents([pos])
        for obj in cell_content:
            if isinstance(obj, its_type):
                return obj
        return None

    def step(self):
        self.schedule.step()

