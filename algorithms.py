from dataclasses import dataclass
from collections import deque
from typing import Optional, Callable, Tuple, List
from queue import PriorityQueue

from map import Action, Map, Position


@dataclass
class Node:
    state: Position
    parent: Optional['Node']
    action: Optional[Action]
    cost: int
    heuristic_value: float

    def __init__(self,
                 state: Position,
                 parent: Optional['Node'],
                 action: Optional[Action],
                 cost: int):

        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic_value = 0

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return f"Node(state={self.state}, parent={self.parent.state}, cost={self.cost})"

    def __lt__(self, obj):
        return self.cost < obj.cost

    def expand(self, problem: Map) -> List['Node']:
        """
        Expand the node, generating all the possible children
        :param problem: map to solve
        :return: list of nodes that are children of the current node
        """
        s = self.state
        nodes = []

        for action in problem.get_actions(s):
            ss, cost = problem.update_position(s, action)
            nodes.append(Node(state=ss, parent=self, action=action, cost=cost + self.cost))

        return nodes


def breadth_first_search(problem: Map) -> Tuple[Node, int, int]:
    """
    Breadth-first search algorithm. Returns the node that is the solution to the problem with the number of nodes
    explored and the number of nodes in the frontier. If no solution is found the last node explored is returned.
    :param problem: map to solve
    :return: solution node, number of nodes explored and number of nodes in the frontier.
    """

    node = Node(problem.start, None, None, 0)

    frontier = deque([node])
    reached = {problem.start}

    while frontier:
        node = frontier.popleft()

        for child in node.expand(problem):
            s = child.state

            if problem.is_finished(s):
                return child, len(reached), len(frontier)

            if child.state not in reached:
                reached.add(s)
                frontier.append(child)

    return node, len(reached), len(frontier)


def depth_first_search(problem: Map) -> Tuple[Node, int, int]:
    """
    Depth-first search algorithm. Returns the node that is the solution to the problem with the number of nodes
    explored and the number of nodes in the frontier. If no solution is found the last node explored is returned.
    :param problem: map to solve
    :return: solution node, number of nodes explored and number of nodes in the frontier.
    """

    node = Node(problem.start, None, None, 0)

    frontier = [node]
    reached = {problem.start}

    while frontier:
        node = frontier.pop()

        for child in node.expand(problem):

            if problem.is_finished(child.state):
                return child, len(reached), len(frontier)

            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)

    return node, len(reached), len(frontier)


def a_star_search(problem: Map, heuristic: Callable[[Position], float]) -> Tuple[Node, int, int]:
    """
    A* search algorithm in the given problem using the heuristic provided. Returns the node that is the solution to the
    problem with the number of nodes explored and the number of nodes in the frontier. If no solution is found the last
    node explored is returned.
    :param problem: map to solve
    :param heuristic: heuristic function to use (takes a position and returns a float)
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """

    function = lambda n: n.cost + heuristic(n.state)

    node = Node(problem.start, None, None, 0)
    node.heuristic_value = heuristic(node.state)

    frontier = PriorityQueue()
    frontier.put((function(node), node))

    reached = {problem.start: node}

    while not (frontier.empty()):
        node = frontier.get()[1]

        if problem.is_finished(node.state):
            return node, len(reached), frontier.qsize()

        for child in node.expand(problem):
            s = child.state

            if not (s in reached) or (child.cost < reached[s].cost):
                child.heuristic_value = heuristic(child.state)

                reached[s] = child
                frontier.put((function(child), child))

    return node, len(reached), frontier.qsize()


def a_star_search_h1(problem: Map) -> Tuple[Node, int, int]:
    """
    A* search algorithm in the given problem using the Chebyshev distance as heuristic. Returns the node that is the
    solution to the problem with the number of nodes explored and the number of nodes in the frontier. If no solution
    is found the last node explored is returned.
    :param problem: map to solve
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """
    return a_star_search(problem, problem.heuristic_1)


def a_star_search_h2(problem: Map) -> Tuple[Node, int, int]:
    """
    A* search algorithm in the given problem using the Chebyshev distance plus the angle distance as heuristic. Returns
    the node that is the solution to the problem with the number of nodes explored and the number of nodes in the
    frontier. If no solution is found the last node explored is returned.
    :param problem: map to solve
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """
    return a_star_search(problem, problem.heuristic_2)
