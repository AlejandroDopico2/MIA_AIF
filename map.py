from dataclasses import dataclass
from enum import Enum
from typing import List


class Orientation(Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7
    IRRELEVANT = 8


ORIENTATION_TO_COORDINATES = {
    Orientation.NORTH: (-1, 0),
    Orientation.NORTHEAST: (-1, 1),
    Orientation.EAST: (0, 1),
    Orientation.SOUTHEAST: (1, 1),
    Orientation.SOUTH: (1, 0),
    Orientation.SOUTHWEST: (1, -1),
    Orientation.WEST: (0, -1),
    Orientation.NORTHWEST: (-1, -1),
}


class Action(Enum):
    MOVE = 0
    ROTATE_CLOCKWISE = 1
    ROTATE_COUNTERCLOCKWISE = 2


@dataclass
class Position:
    x: int
    y: int
    orientation: Orientation = Orientation.IRRELEVANT


class Map:

    matrix: List[List[int]]
    start: Position
    end: Position

    def __init__(self, filename: str):
        """
        Create a map from a file. It is assumed that the file is in the following format:

        - rows cols
        - matrix (rows x cols)
        - start_row start_col start_orientation
        - end_row end_col end_orientation

        :type filename: str
        :param filename: name of the file that contains the map
        """

        with open(filename, 'r') as f:
            lines = f.readlines()

        rows, cols = map(int, lines[0].split())
        lines = lines[1:]

        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]

        for row in range(rows):
            for col, value in enumerate(lines[row].split()):
                self.matrix[row][col] = int(value)

        lines = lines[rows:]

        start_row, start_col, start_orientation = map(int, lines[0].split())
        end_row, end_col, end_orientation = map(int, lines[1].split())

        self.start = Position(start_row, start_col, Orientation(start_orientation))
        self.end = Position(end_row, end_col, Orientation(end_orientation))

    def __str__(self):
        string = '\n'.join([' '.join(map(str, row)) for row in self.matrix])
        string += '\n'
        string += f'Start position: {self.start.x} {self.start.y} {self.start.orientation}\n'
        string += f'End position: {self.end.x} {self.end.y} {self.end.orientation}\n'

        return string

    def update_position(self, position: Position, action: Action) -> tuple[Position, int]:
        """
        Update the position of the robot according to the action. It the action is not valid, the cost is -1.
        :param position: position of the robot
        :param action: action to be performed
        :return: tuple with the new position and the cost of the action
        """

        if action == Action.MOVE:

            new_x = position.x + ORIENTATION_TO_COORDINATES[position.orientation][0]
            new_y = position.y + ORIENTATION_TO_COORDINATES[position.orientation][1]

            new_position = Position(new_x, new_y, position.orientation)

            if not self.is_position_valid(new_position):
                return new_position, -1

            cost = self.matrix[new_x][new_y]

            return new_position, cost

        if action == Action.ROTATE_CLOCKWISE:

            new_orientation = Orientation((position.orientation.value + 1) % 8)
            new_position = Position(position.x, position.y, new_orientation)
            cost = 1

            return new_position, cost

        if action == Action.ROTATE_COUNTERCLOCKWISE:

            new_orientation = Orientation((position.orientation.value - 1) % 8)
            new_position = Position(position.x, position.y, new_orientation)
            cost = 1

            return new_position, cost

    def is_position_valid(self, position: Position) -> bool:
        """
        Return True if the position is valid otherwise False.
        :param position: position of the robot
        :return: True if the position is within the map
        """

        return 0 <= position.x < len(self.matrix) and 0 <= position.y < len(self.matrix[0])

    def get_actions(self, position: Position) -> List[Action]:
        """
        Return the list of valid actions for the given position.
        :param position: position of the robot
        :return: list of valid actions
        """

        actions = [Action.ROTATE_CLOCKWISE, Action.ROTATE_COUNTERCLOCKWISE]

        possible_position, _ = self.update_position(position, Action.MOVE)

        if self.is_position_valid(possible_position):
            actions.append(Action.MOVE)

        return actions

    def is_finished(self, position: Position) -> bool:
        """
        Return True if the robot is in the end position otherwise False.
        :param position: position of the robot
        :return: True if the robot is in the end position
        """
        if self.end.orientation != Orientation.IRRELEVANT:
            return position == self.end

        return position.x == self.end.x and position.y == self.end.y


