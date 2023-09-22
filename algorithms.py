from dataclasses import dataclass
from collections import deque
from typing import Optional
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

    def expand(self, problem: Map):
        s = self.state
        nodes = []

        for action in problem.get_actions(s):
            ss, cost = problem.update_position(s, action)
            nodes.append(Node(state=ss, parent=self, action=action, cost=cost + self.cost))

        return nodes


def breadth_first_search(problem: Map) -> Node:
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

    return -1

def depth_first_search(problem: Map) -> Node:
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

    return -1

def best_first_search(problem: Map, h) -> Node:
    node = Node(problem.start, None, None, 0)
    frontier = PriorityQueue()
    frontier.put((f(node, h), node))
    reached = {problem.start : node}

    while not(frontier.empty()):
        node = frontier.get()[1]
        if problem.is_finished(node.state):
            return node
        for child in node.expand(problem):
            s = child.state
            if (not(s in reached) or (child.cost < reached[s].cost)):
                reached[s] = child
                frontier.put((f(child, h), child))
    return -1

def f(node: Node, h):
    return node.cost + h(node)

def h1(node: Node):
    return 0

def h2(node: Node):
    return 0

def aStar_search_h1(problem: Map) -> Node:
    return best_first_search(problem, h1)

def aStar_search_h2(problem: Map) -> Node:
    return best_first_search(problem, h2)
