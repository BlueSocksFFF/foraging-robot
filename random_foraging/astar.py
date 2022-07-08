import heapq
import sys
from obstacle import Obstacle


class PriorityQueue:
    """This is a supporting class 
    as a priority queue implemented with a binary heap
    """

    def __init__(self):
        """List is tuple(float, tuple)"""
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, priority, pos):
        heapq.heappush(self.elements, (priority, pos))

    def get(self):
        """Get the lowest rank pos"""
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    """pos_b is a list"""
    x_a, y_a = a
    dist = sys.maxsize
    for pos in b:
        x_b, y_b = pos
        dist_new = abs(x_a - x_b) + abs(y_a - y_b)
        if dist_new < dist:
            dist = dist_new
    return dist


class Astar:
    """The class to do astar traversal
    """

    def __init__(self, model):
        """The initialization

        Args:
            model (Model): Generally the model of itself
        """
        self.model = model
        self.grid = self.model.grid

    def get_neighbors(self, pos):
        neighbors = self.grid.get_neighborhood(pos, moore=False, include_center=False)
        for neighbor in neighbors:
            cell_content = self.grid.get_cell_list_contents([neighbor])
            for obj in cell_content:
                if isinstance(obj, Obstacle):
                    neighbors.remove(neighbor)
        return neighbors

    def astar_search(self, start, goals):
        """
        start is a tuple of position
        goal is a list of tuples
        """

        frontier = PriorityQueue()
        frontier.put(0, start)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current in goals:
                break

            for next_grid in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_grid not in cost_so_far or new_cost < cost_so_far[next_grid]:
                    cost_so_far[next_grid] = new_cost
                    priority = new_cost + heuristic(next_grid, goals)
                    frontier.put(priority, next_grid)
                    came_from[next_grid] = current

        return came_from, cost_so_far

    def construct_path(self, start, goals):
        came_from, cost_so_far = self.astar_search(start, goals)
        cost = sys.maxsize
        true_goal = goals[0]
        if len(goals) > 1:
            for goal in goals:
                if goal in cost_so_far.keys():
                    cost_new = cost_so_far[goal]
                    if cost_new < cost:
                        cost = cost_new
                        true_goal = goal
        cost = cost_so_far[true_goal]
        current = true_goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path, cost
