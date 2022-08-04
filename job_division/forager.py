import mesa
import numpy as np
import sys

sys.path.insert(1, '../random_foraging')
from food import Food
from obstacle import Obstacle
from astar import Astar

# is it better for foragers to remember food list and communicate with other agents too?

class Forager(mesa.Agent):

    def __init__(self, unique_id, model, as_scouter, like_cluster):
        self.unique_id = unique_id
        self.model = model
        self.food_id = -1
        self.path_home = None
        self.cost_home = None
        self.path_food = None
        self.as_scouter = as_scouter
        self.to_communicate = False
        self.at_home = True
        self.location_set = False
        self.got_to_food_loc = False
        # Like cluster
        self.like_cluster = like_cluster
        self.food_location_list = []
        self.astar = Astar(self.model)

    # Change roles

    def change_to_scouter(self):
        self.as_scouter = True

    def change_to_forager(self):
        self.as_scouter = False

    # Communication

    def communicate(self):
        foragers_at_home = self.model.update_foragers_at_home()
        number_foragers_at_home = len(foragers_at_home)
        number_food_found = len(self.food_location_list)
        if number_foragers_at_home < 1:
            # print('less than 1')
            return
        elif number_food_found > number_foragers_at_home:
            # print('more food found')
            for i in range(number_foragers_at_home):
                if foragers_at_home[i].as_scouter:
                    pass
                else:
                    foragers_at_home[i].set_location(self.food_location_list[i])
            self.to_communicate = False
            self.food_id = -1
        else:
            # print('more workers home')
            foragers_sent = np.random.choice(foragers_at_home, number_food_found, replace=False)
            print(foragers_sent)
            for i in range(number_food_found):
                foragers_sent[i].set_location(self.food_location_list[i])
            self.to_communicate = False
            self.food_id = -1

    def like_cluster_communicate(self):
        foragers_at_home = self.model.update_foragers_at_home()
        number_foragers_at_home = len(foragers_at_home)
        number_food_found = len(self.food_location_list)
        if number_food_found < 1:
            print('Error: Less than 1 food found.')
            sys.exit()
        elif number_foragers_at_home < 1:
            return
        elif number_food_found == 1:
            food_location = self.food_location_list[0]
            for forager_at_home in foragers_at_home:
                forager_at_home.set_location(food_location)
        else:
            # BUG: What if mean location has obstacle?? Maybe just return?
            mean_location = tuple[int, int]([int(sum(index)/len(index)) for index in zip(*self.food_location_list)])
            print(mean_location)
            cell_content = self.model.grid.get_cell_list_contents(mean_location)
            for obj in cell_content:
                if isinstance(obj, Obstacle):
                    print('Error: the end location is an obstacle')
                    return
            for forager_at_home in foragers_at_home:
                forager_at_home.set_location(mean_location)
        return

    def set_location(self, location):
        # print('location set', self.unique_id)
        self.path_food, cost = self.astar.construct_path(self.pos, location)
        # print(self.path_food)
        self.location_set = True

    # Check

    def check_food(self):
        cell_content = self.model.grid.get_cell_list_contents(self.pos)
        for obj in cell_content:
            if isinstance(obj, Food):
                self.food_id = obj.get_id()
                self.model.grid.remove_agent(obj)
                self.model.grid.food_list.append(self.food_id)
                self.path_home, self.cost_home = self.astar.construct_path(self.pos, self.model.grid.home)
                self.got_to_food_loc = False

    def check_food_around(self):
        # print('checked around')
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        # print(neighbors)
        for obj in neighbors:
            # print(type(obj), obj.pos)
            if isinstance(obj, Food):
                # print('found food')
                food_location = obj.pos
                if food_location not in self.food_location_list:
                    # print('found a unique food')
                    self.food_location_list.append(obj.pos)
                    self.to_communicate = True

    def check_at_home(self):
        if self.pos in self.model.home:
            self.at_home = True
            return True
        else:
            self.at_home = False
            return False

    def check_before_step(self):
        self.check_at_home()
        self.check_food_around()
        if self.model.found_all_food:
            self.path_home, self.cost_home = self.astar.construct_path(self.pos, self.model.grid.home)
        if not self.at_home and self.food_id < 0:
            self.check_food()

    # Move

    def move_randomly(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        cell_content = self.model.grid.get_cell_list_contents(neighbors)
        for obj in cell_content:
            if isinstance(obj, Obstacle):
                neighbors.remove(obj.pos)
        if len(neighbors) <= 0:
            print('Error: no neighbor without obstacle')
            sys.exit()
        next_position = self.random.choice(neighbors)
        self.model.grid.move_agent(self, next_position)

    def move_home(self):
        index = self.path_home.index(self.pos)
        if index == len(self.path_home) - 1:
            return
        pos_next = self.path_home[index + 1]
        self.model.grid.move_agent(self, pos_next)

    def move_to_food(self):
        if self.pos not in self.path_food:
            self.model.grid.move_agent(self, self.path_food[0])
        index = self.path_food.index(self.pos)
        if index == len(self.path_food) - 1:
            self.got_to_food_loc = True
            self.location_set = False
            return
        pos_next = self.path_food[index + 1]
        self.model.grid.move_agent(self, pos_next)

    def move(self):
        if self.as_scouter:
            if self.model.found_all_food and self.at_home:
                return
            elif self.model.found_all_food:
                self.move_home()
            elif self.food_id < 0:
                self.move_randomly()
            elif not self.at_home:
                self.move_home()
            elif self.to_communicate and self.like_cluster:
                self.like_cluster_communicate()
            elif self.to_communicate:
                self.communicate()
            else:
                return
        else:
            if self.model.found_all_food and self.at_home:
                return
            elif self.model.found_all_food:
                self.move_home()
            elif self.food_id < 0:
                if self.got_to_food_loc:
                    self.move_randomly()
                elif self.location_set:
                    self.move_to_food()
            elif not self.at_home:
                self.move_home()
            elif self.to_communicate and self.like_cluster:
                self.like_cluster_communicate()
            elif self.to_communicate:
                self.communicate()
            else:
                return

    def step(self):
        self.check_before_step()
        self.move()

    def advance(self):
        if self.at_home:
            self.food_id = -1
        return
