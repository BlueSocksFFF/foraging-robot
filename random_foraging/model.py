import mesa
import sys

from mesa.time import SimultaneousActivation
from grid import MultiGridWithHome, GridWithObstacles
from forager import Forager
from food import Food
from obstacle import Obstacle


class RandomForagingModel(mesa.Model):
    """_
    Random Foraging Model
    """

    height_preset = 10
    width_preset = 10

    number_food_preset = 10
    number_foragers_preset = 4

    home_preset = [(0, 0), (1, 0)]

    with_obstacles_preset = True

    def __init__(
            self,
            height=height_preset,
            width=width_preset,
            number_food=number_food_preset,
            number_foragers=number_foragers_preset,
            home=home_preset,
            with_obstacles=with_obstacles_preset
    ):

        super().__init__()
        self.height = height
        self.width = width
        self.number_food = number_food
        self.number_foragers = number_foragers
        self.home = home
        self.schedule = SimultaneousActivation(self)
        self.grid = None
        self.forager_list = []
        self.found_all_food = False
        self.with_obstacles = with_obstacles
        self.init_grid()
        self.place_foragers()
        self.place_obstacles()
        self.place_food()

    def init_grid(self):
        if self.with_obstacles:
            self.grid = GridWithObstacles(self.width, self.height, torus=False, home=self.home)
        else:
            self.grid = MultiGridWithHome(self.width, self.height, torus=False, home=self.home)

    def place_foragers(self):
        for i in range(self.number_foragers):
            forager = Forager(self.next_id(), self)
            self.forager_list.append(forager)
            self.schedule.add(forager)
            pos = self.random.choice(self.home)
            self.grid.place_agent(forager, pos)

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
        if self.found_all_food:
            # print("Found all food.")
            at_home = True
            for forager in self.forager_list:
                if not forager.at_home:
                    at_home = False
                    return
            if at_home:
                sys.exit()


if __name__ == "__main__":
    # Test A*
    model = RandomForagingModel(home=[(0, 0)])
    forager = Forager(0, model)
    model.grid.place_agent(forager, (0, 7))
    print(forager.test_astar(forager.pos, model.grid.home))
