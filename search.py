from enum import Enum
from typing import List, Callable

from map import Map

import algorithms

import time


class Algorithm(Enum):
    BFS = algorithms.breadth_first_search
    DFS = algorithms.depth_first_search
    A1 = algorithms.a_star_search_h1
    A2 = algorithms.a_star_search_h2


ALGORITHMS = {
    "BFS": Algorithm.BFS,
    "DFS": Algorithm.DFS,
    "A1": Algorithm.A1,
    "A2": Algorithm.A2
}


def get_path(node: algorithms.Node) -> List[algorithms.Node]:
    """
    Get the path from the root node to the given node.
    :param node: the node to get the path to.
    :return: the path from the root node to the given node.
    """
    path = []

    while node.parent is not None:
        path.append(node)
        node = node.parent

    path.append(node)
    return path[::-1]


def show_solution(solution: algorithms.Node, problem: Map, nodes_explored: int, nodes_frontier: int, is_informed: bool):
    """
    Show the solution to the problem and the number of nodes explored and in the frontier.
    If there is no solution prints a message indicating that.
    :param solution: the node that is the solution to the problem.
    :param problem: the map to solve.
    :param nodes_explored: number of nodes explored.
    :param nodes_frontier: number of nodes in the frontier.
    :param is_informed: True if the algorithm is informed otherwise False. Used to show the heuristic value.
    """
    if not problem.is_finished(solution.state):
        print('No solution found')
        print("Showing last path explored")

    path = get_path(solution)

    for i, node in enumerate(path):

        if i != 0:
            print(f"Action: {node.action.name}")

        if is_informed:
            print(f"({i}, {node.cost}, {node.heuristic_value}, {node.state})")
        else:
            print(f"({i}, {node.cost}, {node.state})")

    print(f"\nTotal number of nodes explored: {nodes_explored}")
    print(f"Total number of nodes in the frontier: {nodes_frontier}")


def wrapper_time(func: Callable):
    """
    Wrapper to measure the time of a function.
    :param func: function to measure the time.
    :return: the result of the function.
    """
    def wrapper(*args, **kwargs):

        time_start = time.perf_counter()
        result = func(*args, **kwargs)
        time_end = time.perf_counter()
        print(f"Time take by the function {func.__name__} is {time_end - time_start}")
        return result

    return wrapper


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='File that contains the map with the specification of the problem')
    parser.add_argument('algorithm', help='Algorithm to be used to solve the problem (BFS, DFS, A*(h1) and A*(h2))')

    args = parser.parse_args()

    if args.algorithm not in ALGORITHMS:
        print('Invalid algorithm')
        return

    algorithm_function = wrapper_time(ALGORITHMS[args.algorithm])

    problem = Map(args.file)

    solution, nodes_explored, nodes_frontier = algorithm_function(problem)

    is_informed = args.algorithm in [Algorithm.A1, Algorithm.A2]
    show_solution(solution, problem, nodes_explored, nodes_frontier, is_informed)


if __name__ == '__main__':
    main()
