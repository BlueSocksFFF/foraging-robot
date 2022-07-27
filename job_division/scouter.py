import mesa
import sys
import numpy as np

sys.path.insert(1, '../random_foraging')
from astar import Astar
from obstacle import Obstacle
from food import Food


class Scouter(mesa.Agent):

    def __init__(self, unique_id, model: mesa.Model) -> None:
        super().__init__(unique_id, model)
        self.found_food: bool = False
        self.food_location: tuple[int, int] = (-1, -1)
        self.at_home: bool = True
        self.a_star = Astar(self.model)
        self.path_home: list[tuple[int, int]] = []
        self.path_food = []
        self.cost_path: int = 0
        self.wait: bool = False

    def check_home(self) -> bool:
        if self.pos in self.model.grid.home:
            # print('at home')
            self.at_home = True
        else:
            self.at_home = False

    def check_content(self, pos, its_type):
        cell_content = self.model.grid.get_cell_list_contents(pos)
        for obj in cell_content:
            if isinstance(obj, its_type):
                return obj
        return None

    def check_food(self):
        if not self.found_food:
            neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
            food = self.check_content(neighbors, Food)
            if food is not None:
                # print('found food')
                self.found_food = True
                self.food_location = food.pos
                self.path_home, self.cost_path = self.a_star.construct_path(self.pos, self.model.grid.home)
                if self.path_home is None:
                    self.path_food = [self.pos, self.food_location]
                else:
                    self.path_food = self.path_home[::-1]
                    self.path_food.append(self.food_location)

    def check_home_workers(self):
        workers_at_home = []
        for worker in self.model.worker_list:
            if worker.at_home:
                workers_at_home.append(worker)
        if not workers_at_home or self.model.found_all_food:
            self.wait = True
            return
        else:
            self.wait = False
            number_workers_sent = np.random.randint(1, len(workers_at_home) + 1)
            workers_sent = np.random.choice(workers_at_home, number_workers_sent, replace=False)
            for worker in workers_sent:
                worker.set_path(self.food_location, self.path_food)
            self.found_food = False

    def check_found_all_food(self):
        if self.model.found_all_food:
            self.path_home, self.cost_path = self.a_star.construct_path(self.pos, self.model.grid.home)

    def check_before_step(self):
        self.check_food()
        self.check_home()
        self.check_found_all_food()
        if self.at_home and self.found_food:
            self.check_home_workers()

    def move_randomly(self) -> None:
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(neighbors)
        while self.check_content(new_position, Obstacle) is not None:
            neighbors.remove(new_position)
            new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)

    def move_home(self):
        # print(self.path_home)
        index = self.path_home.index(self.pos)
        pos_next = self.path_home[index + 1]
        self.model.grid.move_agent(self, pos_next)

    def move(self) -> None:
        print('found food:', self.found_food)
        print('at home: ', self.at_home)
        if self.model.found_all_food and self.at_home:
            self.wait = True
        elif self.model.found_all_food:
            self.move_home()
        elif not self.found_food:
            self.move_randomly()
        elif not self.at_home and self.found_food:
            self.move_home()
        else:
            print('Error')
            print('found food', self.found_food)
            print('at home', self.at_home)

    def step(self):
        self.check_before_step()

        print(self.wait)
        if not self.wait:
            self.move()

    def advance(self) -> None:
        return
