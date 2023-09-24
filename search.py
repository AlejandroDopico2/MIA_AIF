from enum import Enum

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
    "A*(h1)": Algorithm.A1,
    "A*(h2)": Algorithm.A2
}


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='File that contains the map with the specification of the problem')
    parser.add_argument('algorithm', help='Algorithm to be used to solve the problem (BFS, DFS, A*(h1) and A*(h2))')

    args = parser.parse_args()

    if args.algorithm not in ALGORITHMS:
        print('Invalid algorithm')
        return

    algorithm = ALGORITHMS[args.algorithm]

    map = Map(args.file)
    time_start = time.perf_counter()
    solution = algorithm(map)
    time_end = time.perf_counter()

    print(f"Time was {time_end - time_start}")

    # TODO: Needed or only for debug ?

    # position = map.start
    # print(position)
    # position, _ = map.update_position(position, Action.ROTATE_COUNTERCLOCKWISE)
    # print(position)
    # position, _ = map.update_position(position, Action.ROTATE_CLOCKWISE)
    # print(position)
    # position, _ = map.update_position(position, Action.ROTATE_CLOCKWISE)
    # print(position)
    # position, _ = map.update_position(position, Action.ROTATE_CLOCKWISE)
    # print(position)
    # position, _ = map.update_position(position, Action.ROTATE_CLOCKWISE)
    # print(position)
    # position, _ = map.update_position(position, Action.MOVE)
    # print(position)
    # position, _ = map.update_position(position, Action.MOVE)
    # print(position)
    # position, _ = map.update_position(position, Action.ROTATE_COUNTERCLOCKWISE)
    # print(position)
    # position, _ = map.update_position(position, Action.MOVE)
    # print(position)
    # print(map.end)


if __name__ == '__main__':
    main()
