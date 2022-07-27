import mesa
import sys

sys.path.insert(1, '../random_foraging')
from obstacle import Obstacle
from astar import Astar
from food import Food


class Worker(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.food_id: int = -1
        self.food_loc: tuple[int, int] = (-1, -1)
        self.path_food: list[tuple[int, int]] = []
        self.path_home = []
        self.cost_path = -1
        self.got_to_pos_food: bool = False
        self.a_star = Astar(self.model)
        self.wait = True
        self.at_home = True
        self.found_all_food = False

    def set_path(self,
                 loc: tuple[int, int],
                 path: list[tuple[int, int]]) -> None:
        self.food_loc = loc
        self.path_food = path
        # print('worker path:', self.path_food)
        self.wait = False

    def check_home(self) -> bool:
        if self.pos in self.model.grid.home:
            self.at_home = True
            if self.food_id > 0:
                self.model.grid.food_list.append(self.food_id)
                print(self.food_id, self.model.grid.food_list)
                self.food_id = -1
                self.got_to_pos_food = False
                self.wait = True
            if self.model.found_all_food:
                self.wait = True
                # print('Worker % got home' % self.unique_id)
        else:
            self.at_home = False

    def check_content(self, pos, obj_type):
        cell_content = self.model.grid.get_cell_list_contents(pos)
        for obj in cell_content:
            if isinstance(obj, obj_type):
                return obj
        return None

    def check_found_all_food(self):
        if self.model.found_all_food:
            self.path_home, self.cost_path = self.a_star.construct_path(self.pos, self.model.grid.home)

    def check_food(self):
        food = self.check_content([self.pos], Food)
        if food is not None:
            self.food_id = food.get_id()
            self.model.grid.remove_agent(food)
            self.path_home, self.cost_path = self.a_star.construct_path(self.pos, self.model.grid.home)

    def check_before_step(self):
        self.check_home()
        if self.pos == self.food_loc:
            # print("got to pos")
            self.got_to_pos_food = True
        if self.food_id < 0:
            self.check_food()
        if len(self.model.grid.food_list) >= self.model.number_food:
            self.model.found_all_food = True
            # print('Found all food')
        self.check_found_all_food()

    def move_towards_food(self):
        # print(self.pos, self.path_food, self.got_to_pos_food)
        if self.pos not in self.path_food:
            self.model.grid.move_agent(self, self.path_food[0])
        else:
            index = self.path_food.index(self.pos)
            if index == (len(self.path_food) - 1):
                self.got_to_pos_food = True
            else:
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
        if self.pos not in self.path_home:
            self.model.grid.move_agent(self.path_home[0])
        index = self.path_home.index(self.pos)
        pos_next = self.path_home[index + 1]
        self.model.grid.move_agent(self, pos_next)

    def move(self):
        if self.model.found_all_food and self.at_home:
            self.wait = True
        elif self.model.found_all_food:
            self.move_home()
        elif not self.got_to_pos_food and self.food_id < 0:
            # print("move to food")
            self.move_towards_food()
        elif self.got_to_pos_food and self.food_id < 0:
            # print("move randomly")
            self.move_randomly()
        elif self.food_id > 0:
            # print("move home")
            self.move_home()
        else:
            print('error')

    def step(self):
        self.check_before_step()
        # print(self.wait)
        print(self.pos)
        if not self.wait:
            self.move()

    def advance(self):
        return
