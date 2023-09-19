from dataclasses import dataclass
from enum import Enum


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
@dataclass
class Position:
    x: int
    y: int
    orientation: Orientation = Orientation.IRRELEVANT

class Map:
    matrix: list[list[int]]
    start: Position
    end: Position

    def __init__(self, filename: str):

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









