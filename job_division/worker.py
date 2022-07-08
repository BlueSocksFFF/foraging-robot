import mesa
import sys

sys.path.insert(1, '../random_foraging')
from obstacle import Obstacle
from astar import Astar


class Worker(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.food_id: int = -1
        self.food_loc: tuple[int, int] = (-1, -1)
        self.path_food: list[tuple[int, int]] = []
        self.got_to_pos_food: bool = False
        self.a_star = Astar(self.model)
        self.wait = True
        self.at_home = True

    def set_path(self,
                 loc: tuple[int, int],
                 path: list[tuple[int, int]]) -> None:
        self.food_loc = loc
        self.path_food = path
        print('worker path:', self.path_food)
        self.wait = False

    def check_home(self) -> bool:
        if self.pos in self.model.grid.home:
            self.at_home = True
            if self.food_id > 0:
                self.model.grid.food_list.append(self.food_id)
                self.food_id = -1
                self.wait = True
        else:
            self.at_home = False

    def check_before_step(self):
        if self.pos == self.food_loc:
            self.got_to_pos_food = True
        self.chek_home()

    def move_towards_food(self):
        index = self.path_food.index(self.pos)
        next_loc = self.path_food[index + 1]
        self.model.grid.move_agent(self, next_loc)

    def move_randomly(self) -> None:
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        new_position = self.random.choice(neighbors)
        while self.check_content(new_position, Obstacle) is not None:
            neighbors.remove(new_position)
            new_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, new_position)

    def move_home(self):
        index = self.path_home.index(self.pos)
        pos_next = self.path_home[index + 1]
        self.model.grid.move_agent(self, pos_next)

    def move(self):
        if not self.got_to_pos_food and self.food_id < 0:
            self.move_towards_food()
        elif self.got_to_pos_food and self.food_id < 0:
            self.move_randomly()
        elif self.got_to_pos_food and self.food_id > 0:
            self.move_home()

    def step(self):
        print(self.wait)
        if not self.wait:
            self.move()

    def advance(self):
        return
