import os

from algorithms import Node
from map import Map

from random import randint

from search import ALGORITHMS

MAP_SIZES = [3, 5, 7, 9]
NUM_MAPS = 10

TEMP_FILE = "temp.txt"


def generate_map(size: int) -> Map:
    """
    Generate a map of the given size.
    :param size: size of the map to generate.
    :return: the generated map.
    """
    text_input = f"{size} {size}\n"

    for i in range(size):
        for j in range(size):
            value = randint(1, 9)
            text_input += f"{value} "
        text_input += "\n"

    text_input += f"0 0 {randint(0, 7)}\n"
    text_input += f"{size - 1} {size - 1} {randint(0, 8)}\n"

    with open(TEMP_FILE, 'w') as f:
        f.write(text_input)

    problem = Map(TEMP_FILE)
    os.remove(TEMP_FILE)

    return problem


def get_depth(node: Node) -> int:
    """
    Get the depth of the given node.
    :param node: the node to get the depth of.
    :return: the depth of the given node.
    """
    depth = 0
    temp_node = node

    while temp_node.parent is not None:
        depth += 1
        temp_node = temp_node.parent

    return depth


def main():
    for size in MAP_SIZES:

        average_depth = {algorithm: 0 for algorithm in ALGORITHMS.values()}
        average_cost = {algorithm: 0 for algorithm in ALGORITHMS.values()}
        average_nodes_explored = {algorithm: 0 for algorithm in ALGORITHMS.values()}
        average_nodes_frontier = {algorithm: 0 for algorithm in ALGORITHMS.values()}

        for i in range(NUM_MAPS):
            problem = generate_map(size)

            for algorithm in ALGORITHMS.values():

                solution, nodes_explored, nodes_frontier = algorithm(problem)

                average_depth[algorithm] += get_depth(solution)
                average_cost[algorithm] += solution.cost
                average_nodes_explored[algorithm] += nodes_explored
                average_nodes_frontier[algorithm] += nodes_frontier

        print(f"Size: {size}x{size}")

        for algorithm in ALGORITHMS.values():
            print(f"Algorithm: {algorithm.__name__}")
            print(f"Average depth: {average_depth[algorithm] / NUM_MAPS}")
            print(f"Average cost: {average_cost[algorithm] / NUM_MAPS}")
            print(f"Average nodes explored: {average_nodes_explored[algorithm] / NUM_MAPS}")
            print(f"Average nodes in frontier: {average_nodes_frontier[algorithm] / NUM_MAPS}")
            print()


if __name__ == '__main__':
    main()
