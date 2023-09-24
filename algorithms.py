from dataclasses import dataclass
from collections import deque
from typing import Optional, Callable
from queue import PriorityQueue

from map import Action, Map, Position


@dataclass
class Node:
    state: Position
    parent: Optional['Node']
    action: Optional[Action]
    cost: int

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return f"Node(state={self.state}, parent={self.parent.state}, cost={self.cost})"

    def __lt__(self, obj):
        return self.cost < obj.cost

    def expand(self, problem: Map) -> list['Node']:
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


def breadth_first_search(problem: Map) -> Optional[Node]:
    """
    Breadth-first search algorithm
    :param problem: map to solve
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """

    node = Node(problem.start, None, None, 0)

    if problem.is_finished(node.state):
        return node

    frontier = deque([node])
    reached = [problem.start]

    while frontier:
        node = frontier.popleft()
        for child in node.expand(problem):
            s = child.state
            if problem.is_finished(s):
                return child
            elif s not in reached:
                reached.append(s)
                frontier.append(child)

    return None


def depth_first_search(problem: Map) -> Optional[Node]:
    """
    Depth-first search algorithm
    :param problem: map to solve
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """

    node = Node(problem.start, None, None, 0)

    frontier = [node]
    reached = []

    while frontier:
        node = frontier.pop()
        if problem.is_finished(node.state):
            return node
        reached.append(node)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in reached and child not in frontier)

    return None


def a_star_search(problem: Map, heuristic: Callable[[Position], float]) -> Optional[Node]:
    """
    A* search algorithm in the given problem using the heuristic provided
    :param problem: map to solve
    :param heuristic: heuristic function to use (takes a position and returns an integer)
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """

    function = lambda n: n.cost + heuristic(n.state)

    node = Node(problem.start, None, None, 0)

    frontier = PriorityQueue()
    frontier.put((function(node), node))

    reached = {problem.start: 0}

    while not (frontier.empty()):
        node = frontier.get()[1]

        if problem.is_finished(node.state):
            return node

        for child in node.expand(problem):
            s = child.state

            if not (s in reached) or (child.cost < reached[s]):
                reached[s] = child
                frontier.put((function(child), child))

    return None


def a_star_search_h1(problem: Map) -> Node:
    """
    A* search algorithm in the given problem using the Chebyshev distance as heuristic
    :param problem: map to solve
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """
    return a_star_search(problem, problem.heuristic_1)


def a_star_search_h2(problem: Map) -> Node:
    """
    A* search algorithm in the given problem using the Chebyshev distance plus the angle distance as heuristic
    :param problem: map to solve
    :return: solution node (using its parents recursively the path can be generated) or None if no solution was found
    """
    return a_star_search(problem, problem.heuristic_2)
