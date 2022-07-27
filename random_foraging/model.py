import mesa
import sys
import numpy as np

from mesa.time import SimultaneousActivation
from grid import MultiGridWithHome
from forager import Forager
from food import Food
from obstacle import Obstacle


class RandomForagingModel(mesa.Model):
    """_
    Random Foraging Model
    """

    height_preset = 11
    width_preset = 10

    number_food_preset = 10
    number_foragers_preset = 4
    number_obstacles_preset = 5

    # Home is now a full row
    home_preset = []
    for i in range(width_preset):
        home_preset.append((i, 0))

    set_obstacles_preset = False

    obstacle_locs = [(0, 0, 4, 6), (4, 5, 3, 4), (9, 9, 4, 6), (4, 5, 9, 9)]

    environment_types = ['Random', 'Uniform', 'Gaussian', 'Vein', 'Clustered']

    def __init__(
            self,
            height=height_preset,
            width=width_preset,
            number_food=number_food_preset,
            number_foragers=number_foragers_preset,
            number_obstacles=number_obstacles_preset,
            home=home_preset,
            set_obstacles=set_obstacles_preset,
            environment='Uniform'
    ):

        super().__init__()
        self.height = height
        self.width = width
        self.number_food = number_food
        self.number_foragers = number_foragers
        self.number_obstacles = number_obstacles
        self.home = home
        self.schedule = SimultaneousActivation(self)
        self.grid = None
        self.forager_list = []
        self.found_all_food = False
        self.set_obstacles = set_obstacles
        self.environment_type = environment
        # self.random.seed(0)
        # np.random.seed(0)
        self.init_grid()
        self.place_foragers()
        self.place_food_obstacles()

    def init_grid(self):
        self.grid = MultiGridWithHome(self.width, self.height, torus=False, home=self.home)

    def place_foragers(self):
        for i in range(self.number_foragers):
            forager = Forager(self.next_id(), self)
            self.forager_list.append(forager)
            self.schedule.add(forager)
            pos = self.random.choice(self.home)
            self.grid.place_agent(forager, pos)

    def place_food_obstacles(self):
        if self.set_obstacles:
            self.place_obstacles_set()
            self.place_food_random()
        else:
            if self.environment_type == 'Random':
                self.place_random()
            elif self.environment_type == 'Uniform':
                self.place_uniform()
            elif self.environment_type == 'Gaussian':
                self.place_gaussian()
            else:
                print('Error: Environment type does not match')
                sys.exit()

    def place_random(self):
        loc_list = []
        i = 0
        while i < self.number_food + self.number_obstacles:
            x = self.random.randrange(self.width)
            y = self.random.randrange(1, self.height)  # With the first row being home
            if (x, y) not in loc_list:
                loc_list.append((x, y))
                if i < self.number_food:
                    # print(i)
                    food = Food(self.next_id(), self)
                    self.schedule.add(food)
                    self.grid.place_agent(food, (x, y))
                else:
                    obstacle = Obstacle(self.next_id(), self)
                    self.schedule.add(obstacle)
                    self.grid.place_agent(obstacle, (x, y))
                i = i + 1

    def place_food_random(self):
        for i in range(self.number_food):
            x = self.random.randrange(self.width)
            y = self.random.randrange(1, self.height)
            while (x, y) in self.home or self.check_content((x, y), Obstacle) is not None:
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
            food = Food(self.next_id(), self)
            self.schedule.add(food)
            self.grid.place_agent(food, (x, y))

    def place_obstacles_set(self):
        for i in range(len(self.obstacle_locs)):
            x_min, x_max, y_min, y_max = self.obstacle_locs[i]
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    obstacle = Obstacle(self.next_id(), self)
                    self.grid.place_agent(obstacle, (x, y))

    def place_uniform(self):
        locs = np.random.uniform(low=[0, 1], high=[self.width, self.height],
                                 size=(self.number_food + self.number_obstacles + 5, 2)).astype(int)
        # Remove duplicates
        locs_unique = np.unique(locs, axis=0)
        # Check if there are enough unique locations
        locs_unique = locs_unique.tolist()
        if len(locs_unique) < self.number_food + self.number_obstacles:
            print('Error: Uniform environment: not enough locations calculated')
            sys.exit(0)
        # Shuffle the array (only along the first axis)
        self.random.shuffle(locs_unique)
        # Create food and obstacles according to the locations.
        # Because the locations are all unique, food and obstacle will not be on the same location
        for i in range(self.number_food + self.number_obstacles):
            loc = tuple(locs_unique[i])
            if i < self.number_food:
                food = Food(self.next_id(), self)
                self.schedule.add(food)
                self.grid.place_agent(food, loc)
            else:
                obstacle = Obstacle(self.next_id(), self)
                self.schedule.add(obstacle)
                self.grid.place_agent(obstacle, loc)

    def place_gaussian(self):
        cov = [[2, 0], [0, 2]]
        mean = [self.width/2, self.height/2]
        locs = np.random.multivariate_normal(mean, cov, self.number_food + self.number_obstacles + 10).astype(int)
        locs_unique = np.unique(locs, axis=0)
        locs_unique = locs_unique.tolist()
        if len(locs_unique) < self.number_food + self.number_obstacles:
            print('Error: Gaussian Environment: Not enough locations calculated')
            sys.exit()
        self.random.shuffle(locs_unique)
        for i in range(self.number_food + self.number_obstacles):
            loc = tuple[int, int](locs_unique[i])
            if i < self.number_food:
                food = Food(self.next_id(), self)
                self.schedule.add(food)
                self.grid.place_agent(food, loc)
            else:
                obstacle = Obstacle(self.next_id(), self)
                self.schedule.add(obstacle)
                self.grid.place_agent(obstacle, loc)

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
